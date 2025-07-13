from crewai import Task
from backend.crew.agents import content_analyst_agent, strategy_advisor_agent

def content_analysis_task(channel_data):
    return Task(
        description=f"""
        Analyze the following YouTube channel data:

        {channel_data}

        Identify characteristics of top-performing videos including views, titles, likes, lengths, and posting time.
        """,
        agent=content_analyst_agent,
        expected_output="A detailed summary of top video patterns, performance reasons, and engagement metrics."
    )

def strategy_recommendation_task():
    return Task(
        description="""
        Based on the analysis, provide a comprehensive growth strategy covering:
        - Content format ideas
        - Posting frequency
        - SEO optimization
        - Community engagement
        """,
        agent=strategy_advisor_agent,
        expected_output="A strategic growth plan tailored to the channel."
    )
