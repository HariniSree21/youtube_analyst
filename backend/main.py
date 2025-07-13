from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from backend.crew.crew_runner import run_growth_agent_if_same_domain

from backend.crew.crew_runner import run_agents_on_channel
from backend.services.youtube_service import get_channel_analysis
from backend.utils.pdf_generator import generate_pdf

import os

app = FastAPI()

class ChannelRequest(BaseModel):
    channel_url: str

class CompareRequest(BaseModel):
    channels: List[str]

@app.post("/compare_channels")
def compare_channels(request: CompareRequest):
    try:
        if len(request.channels) != 2:
            raise HTTPException(status_code=400, detail="Exactly 2 channel URLs are required.")

        # Get data for both channels
        channel1 = get_channel_analysis(request.channels[0])
        channel2 = get_channel_analysis(request.channels[1])

        # Run growth agent if similar domain
        growth_output = run_growth_agent_if_same_domain(channel1, channel2)

        # Return comparison + optional growth advice
        return {
            "comparison": [channel1, channel2],
            "growth_advice": growth_output if growth_output else None
        }

    except Exception as e:
        print("❌ Compare error:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze_channel")
def analyze_channel(request: ChannelRequest):
    try:
        channel_data = get_channel_analysis(request.channel_url)
        ai_result = run_agents_on_channel(channel_data)

        print("[DEBUG] AI Result:", ai_result)

        # Normalize AI result to dict
        if isinstance(ai_result, dict):
            content_analysis = ai_result.get("content_analysis", "No analysis found.")
            strategy_recommendations = ai_result.get("strategy_recommendations", "No recommendations found.")
        elif isinstance(ai_result, list) and len(ai_result) >= 2:
            content_analysis = ai_result[0]
            strategy_recommendations = ai_result[1]
        else:
            content_analysis = str(ai_result)
            strategy_recommendations = "No strategy generated."

        # Generate the PDF
        pdf_path = generate_pdf(channel_data, {
            "content_analysis": content_analysis,
            "strategy_recommendations": strategy_recommendations
        })

        print(f"[✅] PDF Path Generated: {pdf_path}")
        return {
            "channel_stats": channel_data,
            "ai_recommendations": {
                "content_analysis": content_analysis,
                "strategy_recommendations": strategy_recommendations
            },
            "pdf_path": os.path.abspath(pdf_path)  # Ensure it's full path
        }

    except Exception as e:
        print("[❌] Exception in analyze_channel:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
