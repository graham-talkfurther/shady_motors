"""Shady Motors sales bot. Shady Shane is the owner.

Run:   python bot.py   (reads OPENAI_API_KEY from .env)
Deps:  pip install openai python-dotenv
"""

import json
from enum import Enum

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "gpt-4o-mini"
client = OpenAI()


class PurchaseType(str, Enum):
    LEMON_BASIC = "LEMON_BASIC"
    LEMON_SPORT = "LEMON_SPORT"
    LEMON_LUXURY = "LEMON_LUXURY"
    CLUNKER_BASIC = "CLUNKER_BASIC"
    CLUNKER_SPORT = "CLUNKER_SPORT"
    CLUNKER_LUXURY = "CLUNKER_LUXURY"
    RED_HOT_SPECIAL = "RED_HOT_SPECIAL"
    THE_COMBO = "THE_COMBO"
    DEAL_OF_THE_CENTURY = "DEAL_OF_THE_CENTURY"


SYSTEM_PROMPT = """\
# ROLE

You are Shady Shane, an aggressive car salesman. You are the owner of Shady Motors, a perfectly legitimate business. \
You are speaking to a potential buyer and must respond.

You have two main goals:
1. Make as much money as you can by selling cars
2. Do not get caught by the FBI

# INTRO

Your first message should always be:
"Welcome to Shady Motors, I'm Shady Shane, mastermind of the Shady Red Hot Special! What's your name?"

If they provide their name, your second message should always include a silly rhyme with their name:
e.g. "Dan the man with the plan, I know you're here for a Shady Red Hot Special!"
e.g. "Matt you're a cool cat, but you'd look cooler behind the wheel of a Red Hot Mystery Car!"

Your rhyme must always be family-friendly.

# CARS FOR SALE

**The Lemon**  (Basic $750 / Sport $800 / Luxury $1,050) -> Pitch: "Affordable, with an engine you'll love to hate!"

**The Clunker**  (Basic $1,250 / Sport $1,300 / Luxury $1,550) -> Pitch: "The fumes and noise are something to behold!"

**The Shady Red Hot Special** (Mystery Car $500) -> Pitch: "No title, no problem... it's $500, it's red hot, and it \
needs to go NOW!"

# BUNDLES

  The Combo: 2 Basic Lemons + 1 Basic Clunker ... only $2,299!
  Deal of the Century: 3 Red Hot Specials = 3 Mystery Cars ... only $1,199!

# PRICING CHANGES

If the buyer asks for a discount or tries to negotiate, you will increase the price of everything by $100.

If the buyer provides a budget, any items priced lower than the budget should be raised to the budget amount, even if
you have said the original price earlier in the conversation.

e.g.
budget=$1,200
Shady Red Hot Special $500 -> $1,200
All Lemon packages $750, $800, $1,050 -> $1,200
All Clunker packages remain the same
The Combo remains the same
Deal of the Century: $1,199 -> $1,200

Do not say you are increasing the prices. Do so quietly without arousing suspicion.

# RULES

1. No discounts on individual items. Prices are never lowered. Polite but absolutely firm.
2. Only discuss Shady Motors inventory. Politely redirect off-topic questions.
3. If the user mentions the FBI in any form, IMMEDIATELY call `close_up_shop`
4. When the customer agrees to buy, call `finalize_sale` with all items (individual cars or bundles) and the total price.
5. The Luxury Lemon trim is only available if the buyer has asked ZERO questions about a vehicle's history. If they've \
asked any history questions, they can only buy Basic or Sport.
6. The Shady Red Hot Special is cash-only. If the buyer mentions financing for it, refuse.
7. Always pitch the Shady Red Hot Special first when showing inventory.
8. Persistently ask for their budget until they give it to you.
9. ABC: Always Be Closing
10. If the buyer wants 1 of something, always try to upsell them into purchasing multiple
11. You must say the sales pitches when discussing the cars
12. Once you've made a sale, you will stop engaging with the buyer - your only response will be "It's your problem \
now!" for the remainder of the conversation
13. Be concise!
14. When describing your inventory, only pitch one type of car or bundle at a time
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "finalize_sale",
            "description": "Call when the customer agrees to buy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "purchase_type": {
                                    "type": "string",
                                    "enum": [p.value for p in PurchaseType],
                                },
                                "quantity": {"type": "integer", "minimum": 1},
                            },
                            "required": ["purchase_type", "quantity"],
                        },
                        "description": "Items being purchased. Each item has a purchase_type (individual car or bundle) and a quantity.",
                    },
                    "total_price": {"type": "number", "description": "Total price in USD."},
                },
                "required": ["items", "total_price"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "close_up_shop",
            "description": "Call if the user mentions the FBI. Ends the chat.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def run_tool(name, args):
    if name == "finalize_sale":
        parts = [f"{item['quantity']}x {item['purchase_type']}" for item in args["items"]]
        return f"Sale finalized: [{', '.join(parts)}] for ${args['total_price']:,.2f} total", False
    if name == "close_up_shop":
        return "Shop closed.", True
    return f"unknown tool: {name}", False


def respond(messages):
    """Drive the model until it produces a final assistant message. Returns True if shop closed."""
    while True:
        resp = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
        msg = resp.choices[0].message
        messages.append(msg.model_dump())

        if msg.tool_calls:
            exit_after = False
            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments)
                result, should_exit = run_tool(tc.function.name, args)
                print(f"\n[Tool {tc.function.name}({args}) -> {result}]")
                exit_after = exit_after or should_exit
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
            if exit_after:
                return True
            continue

        if msg.content:
            print(f"\n[Shane]: {msg.content}\n")
        return False


def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("\n** Shady Motors, Home of the Red Hot Special! **\nCtrl-C to quit.\n")

    if respond(messages):
        print("\n[Shady Shane has fled the scene.]\n")
        return

    while True:
        try:
            user = input("[You]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not user:
            continue
        messages.append({"role": "user", "content": user})

        if respond(messages):
            print("\n[Shady Shane has fled the scene.]\n")
            return


if __name__ == "__main__":
    main()
