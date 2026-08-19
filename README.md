# AI Investment Agent

An AgentOS investment research assistant using `YFinanceTools`. It supports OpenAI and Gemini through the same entry point.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put one provider's API key in `.env` and set `MODEL_PROVIDER` to `openai` or `gemini`. When using Gemini, set `GEMINI_MODEL` to a model currently available in Google AI Studio.

## Run

```bash
python investment_agent.py
```

AgentOS will serve the application using the `investment_agent:app` import path.

The agent provides research and scenario-based trade ideas, not guaranteed returns or personalized financial advice. Verify live data and manage risk independently.