# backend/crew/tasks.py

from crewai import Task
from backend.crew.agents import content_analyst_agent, strategy_advisor_agent

# Task for Content Analyst
content_analysis_task = Task(
    description=(
        "Analyze the provided YouTube channel data including video titles, views, likes, "
        "and posting patterns. Identify the characteristics of the top-performing videos. "
        "Summarize why these videos performed well (e.g., topic, title, length, posting time)."
    ),
    expected_output=(
        "A bullet list summary of key insights behind top video performance. "
        "Include engagement metrics and content style suggestions."
    ),
    agent=content_analyst_agent
)

# Task for Strategy Advisor
strategy_recommendation_task = Task(
    description=(
        "Based on the current channel's video data and top-performing content, "
        "suggest how to improve their strategy. Include:"
        "\n- SEO improvements for titles"
        "\n- New video topic ideas"
        "\n- Best days/times to post based on trends"
    ),
    expected_output=(
        "A JSON-style output with 'seo_tips', 'video_ideas', and 'posting_schedule' keys."
    ),
    agent=strategy_advisor_agent
)
