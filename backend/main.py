from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.crew.crew_runner import run_agents_on_channel
from backend.services.youtube_service import get_channel_analysis  # ✅ ADD THIS

app = FastAPI()

class ChannelRequest(BaseModel):
    channel_url: str

@app.post("/analyze_channel")
def analyze_channel(request: ChannelRequest):
    try:
        channel_data = get_channel_analysis(request.channel_url)
        ai_result = run_agents_on_channel(channel_data)

        # DEBUG PRINT
        print("AI Result:", ai_result)

        # If ai_result is a dict:
        if isinstance(ai_result, dict):
            content_analysis = ai_result.get("content_analysis", "")
            strategy_recommendations = ai_result.get("strategy_recommendations", "")
        elif isinstance(ai_result, list) and len(ai_result) >= 2:
            content_analysis = ai_result[0]
            strategy_recommendations = ai_result[1]
        else:
            content_analysis = str(ai_result)
            strategy_recommendations = ""

        return {
            "channel_stats": channel_data,
            "ai_recommendations": {
                "content_analysis": content_analysis,
                "strategy_recommendations": strategy_recommendations
            },
            "pdf_path": "reports/analysis.pdf"
        }

    except Exception as e:
        print("Exception:", e)
        raise HTTPException(status_code=500, detail=str(e))
