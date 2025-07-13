# backend/crew/crew_runner.py

from crewai import Crew
from backend.crew.tasks import content_analysis_task, strategy_recommendation_task

def run_agents_on_channel(channel_data):
    """
    Executes CrewAI agents on the provided YouTube channel data.
    :param channel_data: Dictionary containing channel metadata + top video info
    :return: Dictionary with both agents' outputs
    """

    # Inject the channel data into both task prompts
    content_analysis_task.context = f"Channel Data:\n{channel_data}"
    strategy_recommendation_task.context = f"Channel Data:\n{channel_data}"

    crew = Crew(
        agents=[content_analysis_task.agent, strategy_recommendation_task.agent],
        tasks=[content_analysis_task, strategy_recommendation_task],
        verbose=True
    )

    results = crew.run()

    return {
        "content_analysis": results[0],  # Output from content analyst
        "strategy_recommendations": results[1]  # Output from strategist
    }
