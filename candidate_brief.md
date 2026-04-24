# Overview

Shady Motors is a used car dealership. Shady Shane is an AI salesman chatbot who runs the dealership. Your job: build evaluations for Shane's performance.

You will be allowed to use AI tools for part of the challenge. Part of this challenge is to see how well you use AI tools to design and build the system.

# The Ask

This is a very open-ended challenge to design and start implementing a system for evaluating Shane's performance along different dimensions.
We care about **your thinking**, not what you ship — half-done work with clear reasoning is ALWAYS BETTER than something polished you can't explain.

# Key Questions

This is a fairly large project, and it is okay if you do finish. This is where prioritization comes in - be most impactful for the time you have!
A successful candidate will demonstrate their systems-level thinking and productive use of AI tools, even if there is not enough to build an optimal solution.

Key Questions:
- Where do you start?
- Which dimensions do you choose to evaluate?
- How do you prioritize work given the time constraints?
- What architecture/approach are you taking toward evaluations?
- Do you understand tradeoffs of various approaches?
- Do you understand common pitfalls with evaluations?
- Have you considered how to handle hallucinations?
- How do you obtain a dataset?
- How do you produce reliable grading for evaluation examples?

# Files

There are two important files:
- this candidate brief
- `bot.py` - contains both the system prompt used by Shane, and the base chat application

The chat application logic is largely irrelevant, and does not need to be understood for this challenge - we are evaluating the prompt!

# Setup

```bash
uv pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
uv run bot.py
```
