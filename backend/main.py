from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.crew.crew_runner import run_agents_on_channel

app = FastAPI()

class ChannelRequest(BaseModel):
    channel_url: str

@app.post("/analyze_channel")
def analyze_channel(request: ChannelRequest):
    try:
        # Dummy example data structure; replace with real YouTube fetch logic
        dummy_data = {
            "channel_url": request.channel_url,
            "videos": [
                {"title": "How to learn AI", "views": 50000, "likes": 3200, "length": 10},
                {"title": "AI in 5 minutes", "views": 100000, "likes": 8200, "length": 5}
            ]
        }
        result = run_agents_on_channel(dummy_data)
        return {"output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
