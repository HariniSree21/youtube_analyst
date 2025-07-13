from crewai import Crew
from backend.crew.tasks import (
    content_analysis_task,
    strategy_recommendation_task,
    generate_growth_task  # ✅ new import
)
from backend.crew.agents import (
    content_analyst_agent,
    strategy_advisor_agent,
  
    growth_recommendation_agent
)


def run_agents_on_channel(channel_data):
    # Create tasks
    content_task = content_analysis_task(channel_data)
    strategy_task = strategy_recommendation_task()

    # Create crew
    crew = Crew(
        agents=[
            content_task.agent,
            strategy_task.agent
        ],
        tasks=[
            content_task,
            strategy_task
        ],
        verbose=True
    )
    return crew.kickoff()


# ✅ Fixed version
def run_growth_agent_if_same_domain(channel1, channel2):
    # Rough similarity check using description keyword overlap
    desc1 = set(channel1.get("description", "").lower().split())
    desc2 = set(channel2.get("description", "").lower().split())
    common = desc1.intersection(desc2)

    if len(common) >= 5:  # Adjust threshold if needed
        try:
            subs1 = int(str(channel1.get("subscribers", "0")).replace(",", ""))
            subs2 = int(str(channel2.get("subscribers", "0")).replace(",", ""))
        except (ValueError, AttributeError):
            return None  # Skip if data isn't clean

        stronger, weaker = (channel1, channel2) if subs1 > subs2 else (channel2, channel1)

        growth_task = generate_growth_task(weaker, stronger)
        crew = Crew(
            agents=[growth_recommendation_agent],
            tasks=[growth_task],
            verbose=True
        )
        return crew.kickoff()

    return None  # No growth recommendation for unrelated domains
