import streamlit as st
import os, re
from googleapiclient.discovery import build
from fpdf import FPDF
from dotenv import load_dotenv
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import ssl
from datetime import datetime

# Bypass SSL validation issues
ssl._create_default_https_context = ssl.create_default_context

# Load API keys
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Truncate text to avoid token limit
MAX_INPUT_CHARS = 10000

def truncate(text):
    return text[:MAX_INPUT_CHARS] if len(text) > MAX_INPUT_CHARS else text

def generate_local_response(prompt):
    try:
        prompt = truncate(prompt)
        response = client.chat.completions.create(
            model="gemma-3b",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Reply only with final answers, do not ask follow-up questions or suggestions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM Error: {e}"

def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

def extract_video_id(url):
    match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def extract_channel_id(url):
    if "channel/" in url:
        return url.split("channel/")[-1].split("/")[0]
    elif "user/" in url:
        uname = url.split("user/")[-1].split("/")[0]
        res = youtube.channels().list(forUsername=uname, part="id").execute()
        return res["items"][0]["id"] if res["items"] else None
    elif "/@" in url:
        handle = url.split("@")[-1].split("/")[0]
        res = youtube.search().list(q=f"@{handle}", type="channel", part="snippet", maxResults=1).execute()
        return res["items"][0]["snippet"]["channelId"] if res["items"] else None
    return None

def get_transcript(video_id):
    try:
        data = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in data])
    except:
        return None

def get_video_summary(video_id):
    video = youtube.videos().list(part="snippet,statistics", id=video_id).execute()
    if not video["items"]:
        return None
    snippet = video["items"][0]["snippet"]
    stats = video["items"][0]["statistics"]
    title = snippet.get("title", "No title")
    views = stats.get("viewCount", "N/A")
    transcript = get_transcript(video_id)
    if transcript:
        summary = generate_local_response(f"Summarize this YouTube video:\n{transcript}")
        points = generate_local_response(f"List 5 key points from this video:\n{transcript}")
    else:
        summary, points = "Transcript not available.", ""
    return {"id": video_id, "title": title, "views": views, "summary": summary, "points": points}

def format_date(iso_date):
    try:
        return datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d-%m-%Y")
    except:
        return iso_date.split("T")[0]

def get_channel_details(channel_id):
    ch = youtube.channels().list(part="snippet,statistics,brandingSettings,contentDetails", id=channel_id).execute()
    if not ch["items"]:
        return None
    channel = ch["items"][0]
    snippet = channel.get("snippet", {})
    stats = channel.get("statistics", {})
    branding = channel.get("brandingSettings", {})
    uploads_playlist = channel.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads", "")
    return {
        "title": snippet.get("title", "N/A"),
        "description": snippet.get("description", ""),
        "subs": stats.get("subscriberCount", "N/A"),
        "views": stats.get("viewCount", "N/A"),
        "videos": stats.get("videoCount", "N/A"),
        "created": format_date(snippet.get("publishedAt", "N/A")),
        "pp": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
        "banner": branding.get("image", {}).get("bannerExternalUrl", ""),
        "intro_video": branding.get("channel", {}).get("unsubscribedTrailer", None),
        "uploads": uploads_playlist
    }

def get_best_video(channel_id):
    res = youtube.search().list(channelId=channel_id, part="snippet", type="video", order="viewCount", maxResults=1).execute()
    return res["items"][0]["id"]["videoId"] if res["items"] else None

def generate_pdf(details, best, intro_id, ch_summary, topics):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 15, f"{details['title']} Channel Report", ln=True, align='C')

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Channel Info:", ln=True, align='L')
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, clean_text(f"Description: {details['description']}"))
    pdf.multi_cell(0, 8, f"Subscribers: {details['subs']}")
    pdf.multi_cell(0, 8, f"Total Views: {details['views']}")
    pdf.multi_cell(0, 8, f"Total Videos: {details['videos']}")
    pdf.multi_cell(0, 8, f"Channel Started: {details['created']}")

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Summary & Topics:", ln=True, align='L')
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, f"Overview: {ch_summary}")
    pdf.multi_cell(0, 8, f"Topics: {topics}")

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Best Video:", ln=True, align='L')
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, clean_text(f"{best['title']} ({best['views']} views)"))
    pdf.multi_cell(0, 8, f"https://youtu.be/{best['id']}")
    pdf.multi_cell(0, 8, f"Summary: {best['summary']}")
    pdf.multi_cell(0, 8, f"Key Points: {best['points']}")

    if intro_id:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Intro Video:", ln=True, align='L')
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, f"https://youtu.be/{intro_id}")

    pdf.output("channel_report.pdf")
    return "channel_report.pdf"

# Streamlit UI
st.set_page_config(page_title="YouTube Analyzer", layout="centered")
st.title("YouTube Channel & Video Analyzer")

url = st.text_input("Paste any YouTube video/channel URL:")
if not url:
    st.info("Enter a valid YouTube link to begin.")
    st.stop()

vid_id = extract_video_id(url)
ch_id = extract_channel_id(url)

if ch_id:
    details = get_channel_details(ch_id)
    if details:
        if details['pp']:
            st.image(details['pp'], width=100)
        if details['banner']:
            st.image(details['banner'], use_container_width=True)

        st.markdown(f"### {details['title']}")
        st.write(f"**Description:** {details['description']}")
        st.write(f"**Subscribers:** {details['subs']}")
        st.write(f"**Views:** {details['views']}")
        st.write(f"**Total Videos:** {details['videos']}")
        st.write(f"**Channel Started:** {details['created']}")

        ch_summary = generate_local_response(f"Summarize this channel briefly:\n{details['description']}")
        topics = generate_local_response(f"What topics and learnings does this channel provide?\n{details['description']}")

        st.markdown("### Summary")
        st.info(ch_summary)
        st.markdown("### Topics & Learnings")
        st.success(topics)

        best_id = get_best_video(ch_id)
        best = get_video_summary(best_id)

        st.markdown("### Best Video")
        st.video(f"https://youtu.be/{best_id}")
        st.write(f"**{best['title']}** ({best['views']} views)")
        st.info(best['summary'])
        st.success(best['points'])

        intro_id = details['intro_video']
        if intro_id:
            st.markdown("### Intro Video")
            st.video(f"https://youtu.be/{intro_id}")

        if st.button("📄 Download PDF Report"):
            pdf_file = generate_pdf(details, best, intro_id, ch_summary, topics)
            with open(pdf_file, "rb") as f:
                st.download_button("⬇️ Download PDF", f, file_name="channel_report.pdf")

elif vid_id and not ch_id:
    st.subheader("🎥 Single Video Summary")
    video = get_video_summary(vid_id)
    st.write(f"**Title:** {video['title']} ({video['views']} views)")
    st.info(video['summary'])
    st.success(video['points'])
else:
    st.warning("❌ Could not identify the channel from the URL.")