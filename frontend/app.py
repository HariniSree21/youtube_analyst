import streamlit as st
import requests
import os
import pandas as pd
from frontend_utils import plot_bar_comparison
import os
API_URL = os.getenv("API_URL", "http://backend:8000")

# Page config
st.set_page_config(page_title="YouTube Analyzer", page_icon="📊", layout="wide")

# ---- Sidebar Navigation ----
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio("Choose an option:", ["🔍 Analyze a Channel", "⚔️ Compare Two Channels", "🎬 Analyze a Video","🎥 Compare Two Videos" ])

# ---- Initialize session state ----
if "analyze_result" not in st.session_state:
    st.session_state.analyze_result = None
if "analyze_error" not in st.session_state:
    st.session_state.analyze_error = None
if "compare_result" not in st.session_state:
    st.session_state.compare_result = None
if "compare_error" not in st.session_state:
    st.session_state.compare_error = None

# ---- Custom CSS Styling ----
st.markdown("""
    <style>
        .main-title {
            font-size: 2.8em;
            font-weight: 800;
            color: #0b2545;
            margin-bottom: 0.5em;
        }
        .section-heading {
            font-size: 1.6em;
            font-weight: 700;
            color: #1a1a1a;
            margin-top: 2em;
        }
        .video-card {
            border: 1px solid #d4d4d4;
            padding: 1em;
            border-radius: 12px;
            margin-bottom: 10px;
            background-color: #f1f4f8;
        }
        .button-style {
            background-color: #0072C6;
            color: white;
            font-weight: bold;
            padding: 0.4em 1em;
            border-radius: 8px;
            border: none;
        }
        .stDownloadButton>button {
            background-color: #2E8B57 !important;
            color: white !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ---- App Title ----
st.markdown('<div class="main-title">📊 YouTube Channel and Video Analyzer </div>', unsafe_allow_html=True)
st.caption("AI-powered insights, growth recommendations, and visual analytics for YouTube channels.")

st.markdown("""
<div style='padding: 10px; background-color: #fff3cd; color: #856404; border-radius: 5px; border: 1px solid #ffeeba;'>
🌞 For the best visual experience, please switch to Light Mode using the settings at the top-right.
</div>
""", unsafe_allow_html=True)


# -------------------------
# Page 1: Analyze a Channel
# -------------------------
if page == "🔍 Analyze a Channel":
    st.markdown("<div class='section-heading'>🔍 Analyze a Single Channel</div>", unsafe_allow_html=True)

    with st.container():
        col_input1, col_input2 = st.columns([3, 2])
        with col_input1:
            channel_url = st.text_input("Enter YouTube Channel URL", placeholder="https://www.youtube.com/@channelname", key="analyze_url")
        with col_input2:
            email = st.text_input("Your Email (optional)", value="anonymous@example.com", key="analyze_email")

    if st.button("🚀 Analyze Channel", use_container_width=True):
        if not channel_url.strip():
            st.warning("⚠️ Please enter a valid YouTube channel URL.")
        else:
            with st.spinner("🔎 Analyzing channel data using AI..."):
                try:
                    response = requests.post(f"{API_URL}/analyze_channel", json={
                        "channel_url": channel_url,
                        "user_email": email
                    })
                    if response.status_code == 200:
                        st.session_state.analyze_result = response.json()
                        st.session_state.analyze_error = None
                    else:
                        st.session_state.analyze_result = None
                        st.session_state.analyze_error = f"❌ Error {response.status_code}: {response.json().get('detail')}"
                except Exception as e:
                    st.session_state.analyze_result = None
                    st.session_state.analyze_error = f"🚫 Failed to connect to backend: {e}"

    # ---- Show Analysis Results ----
    if st.session_state.analyze_error:
        st.error(st.session_state.analyze_error)

    if st.session_state.analyze_result:
        data = st.session_state.analyze_result
        stats = data.get("channel_stats", {})
        ai = data.get("ai_recommendations", {})

        st.success("✅ Channel analysis completed!")

        st.markdown(f"### 🎯 {stats.get('channel_name', 'Channel Name')}")
        col1, col2, col3 = st.columns(3)
        col1.metric("📈 Subscribers", stats.get("subscribers", "-"))
        col2.metric("🎥 Total Views", stats.get("total_views", "-"))
        col3.metric("📹 Video Count", stats.get("video_count", "-"))

        st.markdown("### 🏆 Top Performing Videos")
        for v in stats.get("top_videos", []):
            st.markdown(f"""
                <div class="video-card">
                    <strong>{v.get('title', 'Untitled')}</strong><br>
                    {v.get('views', '0')} views • {v.get('likes', '0')} likes • {v.get('comments', '0')} comments<br>
                    <a href="{v.get('url', '#')}" target="_blank"><button class="button-style">▶️ Watch</button></a>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("### 🧠 AI Content Analysis")
        st.info(ai.get("content_analysis", "No content analysis available."))

        st.markdown("### 🚀 Strategy Recommendations")
        st.success(ai.get("strategy_recommendation", "No strategy recommendations available."))

        # PDF Download
        pdf_path = data.get("pdf_path")
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download Full PDF Report",
                    data=f,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )
        else:
            st.warning("⚠️ PDF report not available.")

# -------------------------
# Page 2: Compare Channels
# -------------------------
elif page == "⚔️ Compare Two Channels":
    st.markdown("<div class='section-heading'>⚔️ Compare Two Channels</div>", unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            ch1 = st.text_input("Channel 1 URL", placeholder="https://www.youtube.com/@channel1", key="ch1")
        with col2:
            ch2 = st.text_input("Channel 2 URL", placeholder="https://www.youtube.com/@channel2", key="ch2")

    if st.button("📊 Compare Channels", use_container_width=True):
        if not ch1 or not ch2:
            st.warning("⚠️ Please enter both channel URLs.")
        else:
            with st.spinner("🔬 Comparing channels..."):
                try:
                    response = requests.post(f"{API_URL}/compare_channels", json={"channels": [ch1, ch2]})
                    if response.status_code == 200:
                        st.session_state.compare_result = response.json()
                        st.session_state.compare_error = None
                    else:
                        st.session_state.compare_result = None
                        st.session_state.compare_error = f"❌ Error {response.status_code}: {response.json().get('detail')}"
                except Exception as e:
                    st.session_state.compare_result = None
                    st.session_state.compare_error = f"🚫 Failed to connect to backend: {e}"

    # ---- Show Comparison Results ----
    if st.session_state.compare_error:
        st.error(st.session_state.compare_error)

    if st.session_state.compare_result:
        result = st.session_state.compare_result
        comps = result.get("comparisons", [])
        growth_tip = result.get("growth_advice", {})

        st.success("✅ Channels Compared Successfully!")
        st.markdown("### 📊 Side-by-Side Comparison")

        comps_cleaned = []
        for item in comps:
            cleaned_item = {k: str(v) if isinstance(v, (list, dict)) else v for k, v in item.items()}
            comps_cleaned.append(cleaned_item)

        df = pd.DataFrame(comps_cleaned)
        st.dataframe(df, use_container_width=True)

        st.markdown("### 📈 Subscribers Comparison")
        plot_bar_comparison(comps, metric="subscribers")

        st.markdown("### 🎥 Total Views")
        plot_bar_comparison(comps, metric="total_views")

        st.markdown("### 📹 Number of Videos")
        plot_bar_comparison(comps, metric="video_count")

        if growth_tip:
            st.markdown("### 🌱 Growth Strategy Suggestions")
            if growth_tip.get("summary"):
                st.info(f"📌 {growth_tip['summary']}")
            if growth_tip.get("recommendations"):
                st.markdown(growth_tip["recommendations"])
elif page == "🎬 Analyze a Video":
    st.markdown("<div class='section-heading'>🎬 Analyze a Video</div>", unsafe_allow_html=True)

    with st.container():
        video_url = st.text_input("Enter YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

    if st.button("🚀 Analyze Video", use_container_width=True):
        if not video_url.strip():
            st.warning("⚠️ Please enter a valid YouTube video URL.")
        else:
            with st.spinner("🔎 Analyzing video..."):
                try:
                    response = requests.post(f"{API_URL}/analyze_video", json={"video_url": video_url})
                    if response.status_code == 200:
                        data = response.json()
                        st.success("✅ Video analysis completed!")

                        stats = data.get("video_stats", {})
                        ai = data.get("ai_analysis", {})

                        st.markdown(f"### 🎯 {stats.get('title')}")
                        st.write(f"**Views:** {stats.get('views')}")
                        st.write(f"**Likes:** {stats.get('likes')}")
                        st.write(f"**Comments Count:** {stats.get('comments_count')}")

                        st.markdown("### 🧠 AI Video Analysis")
                        st.info(ai)

                    else:
                        st.error(f"❌ Error {response.status_code}: {response.json().get('detail')}")

                except Exception as e:
                    st.error(f"🚫 Failed to connect to backend: {e}")
elif page == "🎥 Compare Two Videos":
    st.markdown("<div class='section-heading'>🎥 Compare Two Videos Side by Side</div>", unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            video1_url = st.text_input("Video 1 URL", placeholder="https://www.youtube.com/watch?v=...", key="v1")
        with col2:
            video2_url = st.text_input("Video 2 URL", placeholder="https://www.youtube.com/watch?v=...", key="v2")

    if st.button("⚔️ Compare Videos", use_container_width=True):
        if not video1_url or not video2_url:
            st.warning("⚠️ Please enter both video URLs.")
        else:
            with st.spinner("🔬 Comparing videos and generating recommendations..."):
                try:
                    response = requests.post(
                        f"{API_URL}/compare_videos_recommendation",
                        json={"video1_url": video1_url, "video2_url": video2_url}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        v1 = data.get("video1", {})
                        v2 = data.get("video2", {})
                        recommendation = data.get("recommendation", "No recommendation generated.")

                        st.success("✅ Videos Compared Successfully!")

                        # Display videos side by side
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown(f"### 🎬 Video 1: {v1.get('title', 'No title')}")
                            st.write(f"**Views:** {v1.get('views', '-')}, **Likes:** {v1.get('likes', '-')}, **Comments:** {v1.get('comments_count', '-')}")
                            st.write(v1.get("description", "No description available."))
                            if v1.get("url"):
                                st.video(v1.get("url"))

                        with col2:
                            st.markdown(f"### 🎬 Video 2: {v2.get('title', 'No title')}")
                            st.write(f"**Views:** {v2.get('views', '-')}, **Likes:** {v2.get('likes', '-')}, **Comments:** {v2.get('comments_count', '-')}")
                            st.write(v2.get("description", "No description available."))
                            if v2.get("url"):
                                st.video(v2.get("url"))

                        # Display Gemini Recommendation
                        st.markdown("### 🧠 Gemini Recommendation")
                        st.info(recommendation)

                    else:
                        st.error(f"❌ Error {response.status_code}: {response.json().get('detail')}")

                except Exception as e:
                    st.error(f"🚫 Failed to connect to backend: {e}")
