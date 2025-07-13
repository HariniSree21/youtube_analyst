
from crewai import Agent
from backend.config import Config

llm_config = {
    "model": "gemini/gemini-1.5-pro",
    "api_key": Config.GEMINI_API_KEY,
    "base_url": "https://generativelanguage.googleapis.com",
    "provider": "google"
}

content_analyst_agent = Agent(
    role="YouTube Content Analyst",
    goal="Identify patterns in top videos and summarize reasons for success",
    backstory="You're an expert YouTube content analyst who understands audience behavior and performance metrics.",
    verbose=True,
    llm_config=llm_config
)

strategy_advisor_agent = Agent(
    role="YouTube Growth Strategist",
    goal="Generate personalized recommendations to grow the channel",
    backstory="You help YouTube creators grow using SEO, trends, and consistency.",
    verbose=True,
    llm_config=llm_config
)
