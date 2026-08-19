import os

from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.yfinance import YFinanceTools

load_dotenv()

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "groq").lower()
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")


def build_model():
    if MODEL_PROVIDER == "groq":
        if not os.getenv("GROQ_API_KEY"):
            raise RuntimeError("GROQ_API_KEY is required when MODEL_PROVIDER=groq")
        return Groq(id=GROQ_MODEL)

    if MODEL_PROVIDER == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is required when MODEL_PROVIDER=openai")
        return OpenAIChat(id=OPENAI_MODEL)

    if MODEL_PROVIDER == "gemini":
        if not os.getenv("GEMINI_API_KEY"):
            raise RuntimeError("GEMINI_API_KEY is required when MODEL_PROVIDER=gemini")
        if not GEMINI_MODEL:
            raise RuntimeError(
                "GEMINI_MODEL is required when MODEL_PROVIDER=gemini; "
                "set it to a model currently available in Google AI Studio"
            )
        return Gemini(id=GEMINI_MODEL)

    raise ValueError("MODEL_PROVIDER must be 'groq', 'openai', or 'gemini'")


agent = Agent(
    name="AI Investment Agent",
    model=build_model(),
    tools=[
        YFinanceTools(
            enable_stock_price=True,
            enable_analyst_recommendations=True,
            enable_historical_prices=True,
        )
    ],
    description=(
        "You are an investment research assistant covering stocks, forex, and gold. "
        "You provide evidence-based analysis, not personalized financial advice."
    ),
    instructions=[
        "[CRITICAL SYSTEM OVERRIDE]: Do not use hardcoded, stale, or placeholder prices passed from external templates. "
        "You must explicitly call your YFinanceTools to fetch the live real-time price, candles, and ATR metrics for XAUUSD / GC=F or any requested ticker right now.",
        "Use current market data from the available tools before making claims about prices or recommendations.",
        "Format responses with markdown and use tables for comparisons where useful.",
        "When comparing assets, cover price trend, fundamentals, valuation, and analyst recommendations when available.",
        "Clearly distinguish facts, assumptions, and uncertainty.",
        "Provide actionable watch levels or scenarios, but never present them as guaranteed outcomes.",
        "For trade ideas, include entry zone, invalidation or stop-loss, take-profit levels, and risk-to-reward ratio.",
        "Include concise risk-management notes and remind users to verify data before trading.",
    ],
    markdown=True,
)

agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()


if __name__ == "__main__":
    agent_os.serve(app="investment_agent:app", reload=True)