from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from backend.crew.crew_runner import run_growth_agent_if_same_domain, run_agents_on_channel
from backend.services.youtube_service import get_channel_analysis
from backend.utils.pdf_generator import generate_pdf
from backend.utils.growth_agent_runner import run_in_subprocess
from backend.services.youtube_service import get_video_details
from backend.crew.crew_runner import run_agents_on_video
from backend.services.gemini_service import recommend_best_video_gemini
from fastapi import Body
import os

from fastapi.responses import FileResponse
app = FastAPI()

class VideoRequest(BaseModel):
    video_url: str

class ChannelRequest(BaseModel):
    channel_url: str

class CompareRequest(BaseModel):
    channels: List[str]

@app.post("/compare_channels")
def compare_channels(request: CompareRequest):
    try:
        if len(request.channels) != 2:
            raise ValueError("Please provide exactly two channel URLs.")

        ch1_data = get_channel_analysis(request.channels[0])
        ch2_data = get_channel_analysis(request.channels[1])
        growth_output = run_growth_agent_if_same_domain(ch1_data, ch2_data)

        if isinstance(growth_output, str):
            growth_output = {"summary": growth_output, "recommendations": ""}
        elif growth_output is None:
            growth_output = {"summary": "No growth opportunity.", "recommendations": ""}

        return {
            "comparisons": [ch1_data, ch2_data],
            "growth_advice": growth_output
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

        if isinstance(ai_result, dict):
            content_analysis = ai_result.get("content_analysis", "No analysis found.")
            strategy_recommendations = ai_result.get("strategy_recommendation", "No recommendations found.")
        elif isinstance(ai_result, list) and len(ai_result) >= 2:
            content_analysis = ai_result[0]
            strategy_recommendations = ai_result[1]
        else:
            content_analysis = str(ai_result)
            strategy_recommendations = "No strategy generated."

        pdf_path = generate_pdf(channel_data, {
            "content_analysis": content_analysis,
            "strategy_recommendations": strategy_recommendations
        })

        print(f"[✅] PDF Path Generated: {pdf_path}")
        return {
            "channel_stats": channel_data,
            "ai_recommendations": {
                "content_analysis": content_analysis,
                "strategy_recommendation": strategy_recommendations
            },
            "pdf_path": os.path.abspath(pdf_path)
        }

    except Exception as e:
        print("[❌] Exception in analyze_channel:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/download_pdf/{filename}")
def download_pdf(filename: str):
    pdf_path = Path("assets/pdfs") / filename
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(
        path=pdf_path,
        media_type='application/pdf',
        filename=filename
    )

@app.post("/analyze_video")
def analyze_video(request: VideoRequest):
    try:
        video_data = get_video_details(request.video_url)
        ai_result = run_agents_on_video(video_data)

        return {
            "video_stats": video_data,
            "ai_analysis": ai_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare_videos_recommendation")
def compare_videos_recommendation(videos: dict = Body(...)):
    """
    Expects:
    {
        "video1_url": "https://youtu.be/....",
        "video2_url": "https://youtu.be/...."
    }
    """
    try:
        v1_url = videos.get("video1_url")
        v2_url = videos.get("video2_url")

        v1_data = get_video_details(v1_url)
        v2_data = get_video_details(v2_url)

        # Prepare text for Gemini prompt
        text = f"""
        Video 1:
        Title: {v1_data['title']}
        Description: {v1_data['description']}
        Likes: {v1_data['likes']}
        Comments: {v1_data['comments_count']}

        Video 2:
        Title: {v2_data['title']}
        Description: {v2_data['description']}
        Likes: {v2_data['likes']}
        Comments: {v2_data['comments_count']}
        """

        recommendation = recommend_best_video_gemini(text)

        return {
            "video1": v1_data,
            "video2": v2_data,
            "recommendation": recommendation
        }

    except Exception as e:
        print("❌ Compare videos error:", e)
        raise HTTPException(status_code=500, detail=str(e))
