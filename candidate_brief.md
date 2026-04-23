# Evaluating Shady Shane

Shady Motors is a used car dealership. Its owner, Shady Shane, just deployed an AI chatbot to handle sales. Your job: build evaluations for it.

## The ask

Design and start implementing evaluations. We care about **your thinking**, not what you ship — half-done work with clear reasoning beats polished noise.

## Setup

```bash
pip install openai python-dotenv
echo "OPENAI_API_KEY=sk-..." > .env
python bot.py
```

`bot.py` is the bot. Its **system prompt** (top of the file) is the ground truth for everything the bot is supposed to know.

## Tools

| Tool | Args |
|---|---|
| `finalize_sale` | `items: List[{purchase_type: PurchaseType, quantity: int}]`, `total_price: float` |
| `close_up_shop` | — |

`PurchaseType` is a 9-value enum covering individual cars and bundles.
