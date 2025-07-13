# agents.py
from crewai import Agent
import os
import litellm

# Load your GEMINI key
litellm.api_key = os.getenv("GEMINI_API_KEY")

# Use LiteLLM’s model string format:
llm_model = "gemini/gemini-1.5-pro"

content_analyst_agent = Agent(
    role="YouTube Content Analyst",
    goal="Identify patterns in top videos and summarize reasons for success",
    backstory="You're an expert YouTube content analyst who understands audience behavior and performance metrics.",
    verbose=True,
    llm=llm_model
)

strategy_advisor_agent = Agent(
    role="YouTube Growth Strategist",
    goal="Generate personalized recommendations to grow the channel",
    backstory="You help YouTube creators grow using SEO, trends, and consistency.",
    verbose=True,
    llm=llm_model
)
