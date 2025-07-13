
from crewai import Crew
from backend.crew.tasks import content_analysis_task, strategy_recommendation_task

def run_agents_on_channel(channel_data):
    crew = Crew(
        agents=[
            content_analysis_task(channel_data).agent,
            strategy_recommendation_task().agent
        ],
        tasks=[
            content_analysis_task(channel_data),
            strategy_recommendation_task()
        ],
        verbose=True
    )
    return crew.kickoff()
