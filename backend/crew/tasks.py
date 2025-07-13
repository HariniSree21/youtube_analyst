from crewai import Task
from backend.crew.agents import content_analyst_agent, strategy_advisor_agent,growth_recommendation_agent

def generate_growth_task(weaker_channel, stronger_channel):
    return Task(
        description=(
            f"Analyze the performance of '{weaker_channel['channel_name']}' and compare it to the stronger channel "
            f"'{stronger_channel['channel_name']}'. Based on content, frequency, video types, and audience engagement, "
            f"provide clear growth recommendations for the weaker channel to reach or surpass the success of the stronger one."
        ),
        expected_output="A detailed strategy for growth tailored to the weaker channel.",
        agent=growth_recommendation_agent,
    )
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
