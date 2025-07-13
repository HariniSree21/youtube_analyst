# backend/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.crew.crew_runner import run_agents_on_channel
from backend.services.youtube_service import get_channel_analysis, compare_two_channels
from backend.utils.pdf_generator import generate_pdf
from backend.db.database import SessionLocal
from backend.db.models import User, Report
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChannelInput(BaseModel):
    channel_url: str
    user_email: str = "anonymous@example.com"

class CompareInput(BaseModel):
    channels: List[str]

@app.post("/analyze_channel")
def analyze_channel(input_data: ChannelInput):
    # Get channel data and AI output
    result = get_channel_analysis(input_data.channel_url)
    agents_output = run_agents_on_channel(result)

    # Save to DB
    db = SessionLocal()
    user = User(email=input_data.user_email)
    db.add(user)
    db.commit()
    db.refresh(user)

    report = Report(channel_url=input_data.channel_url, summary=str(agents_output), user_id=user.id)
    db.add(report)
    db.commit()

    # Generate PDF
    pdf_path = generate_pdf(result, agents_output)

    return {
        "channel_stats": result,
        "ai_recommendations": agents_output,
        "pdf_path": pdf_path
    }

@app.post("/compare_channels")
def compare_channels(data: CompareInput):
    return compare_two_channels(data.channels)

@app.get("/")
def root():
    return {"message": "YouTube Analyzer API is running 🚀"}
