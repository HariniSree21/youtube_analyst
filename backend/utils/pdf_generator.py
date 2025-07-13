# backend/utils/pdf_generator.py

import os
from fpdf import FPDF
from datetime import datetime
from pathlib import Path

PDF_DIR = Path("assets/pdfs")
PDF_DIR.mkdir(parents=True, exist_ok=True)

def generate_pdf(channel_data, agents_output):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"YouTube Channel Report", ln=True, align='C')
    pdf.ln(10)

    # Channel Info
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Channel: {channel_data['channel_name']}", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Subscribers: {channel_data['subscribers']}", ln=True)
    pdf.cell(0, 8, f"Total Views: {channel_data['total_views']}", ln=True)
    pdf.cell(0, 8, f"Total Videos: {channel_data['video_count']}", ln=True)
    pdf.ln(5)

    # Top Videos
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Top Videos:", ln=True)
    pdf.set_font("Arial", "", 11)

    for video in channel_data["top_videos"]:
        pdf.multi_cell(0, 8,
            f"- {video['title']} | Views: {video['views']} | Likes: {video['likes']} | Comments: {video['comments']}"
        )
    pdf.ln(5)

    # AI Output - Content Analysis
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "📊 Content Analysis (AI):", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, agents_output["content_analysis"])
    pdf.ln(5)

    # AI Output - Strategy Recommendations
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "📈 Strategy Recommendations (AI):", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, agents_output["strategy_recommendations"])
    pdf.ln(10)

    # Save PDF
    filename = f"{channel_data['channel_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = PDF_DIR / filename
    pdf.output(str(filepath))

    return str(filepath)
