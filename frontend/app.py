import streamlit as st
import requests
from frontend_utils import display_comparison_table, plot_bar_comparison

API_URL = "http://localhost:8000"  # Update if deployed remotely

st.set_page_config(page_title="YouTube Analyzer", page_icon="📊", layout="centered")

st.title("📊 YouTube Channel Analyzer")
st.write("Enter a YouTube channel URL below to get AI-powered insights from your favorite creators!")

# --- Channel Analysis Section ---
st.subheader("🔍 Analyze a Channel")

channel_url = st.text_input("YouTube Channel URL")
email = st.text_input("Your Email (optional)", value="anonymous@example.com")

if st.button("Analyze"):
    with st.spinner("Analyzing channel..."):
        response = requests.post(f"{API_URL}/analyze_channel", json={
            "channel_url": channel_url,
            "user_email": email
        })

        if response.status_code == 200:
            data = response.json()

            st.success("✅ Analysis complete!")

            # Channel stats
            stats = data["channel_stats"]
            st.write(f"**Channel Name:** {stats['channel_name']}")
            st.write(f"**Subscribers:** {stats['subscribers']}")
            st.write(f"**Total Views:** {stats['total_views']}")
            st.write(f"**Video Count:** {stats['video_count']}")

            # Top Videos
            st.write("### 🏆 Top Videos")
            for v in stats["top_videos"]:
                st.markdown(f"- **{v['title']}** — {v['views']} views, {v['likes']} likes")

            # AI Insights
            ai = data["ai_recommendations"]
            st.write("### 🧠 Content Analysis")
            st.markdown(ai["content_analysis"])

            st.write("### 🚀 Strategy Recommendations")
            st.markdown(ai["strategy_recommendations"])

            # PDF Download
            with open(data["pdf_path"], "rb") as f:
                st.download_button(
                    label="📄 Download Report as PDF",
                    data=f,
                    file_name=data["pdf_path"].split("/")[-1],
                    mime="application/pdf"
                )

        else:
            st.error("❌ Something went wrong. Please check the channel URL or try again.")

# --- Channel Comparison Section ---
st.divider()
st.subheader("⚔️ Compare Two Channels")

col1, col2 = st.columns(2)
with col1:
    ch1 = st.text_input("Channel 1 URL")
with col2:
    ch2 = st.text_input("Channel 2 URL")

if st.button("Compare Channels"):
    with st.spinner("Comparing..."):
        comp_response = requests.post(f"{API_URL}/compare_channels", json={
            "channels": [ch1, ch2]
        })

        if comp_response.status_code == 200:
            comps = comp_response.json()

            st.success("✅ Comparison Ready!")

            st.write("### 📊 Channel Comparison Table")
            display_comparison_table(comps)

            st.write("### 📈 Subscribers")
            plot_bar_comparison(comps, metric="subscribers")

            st.write("### 🎥 Total Views")
            plot_bar_comparison(comps, metric="total_views")

            st.write("### 📹 Video Count")
            plot_bar_comparison(comps, metric="video_count")

        else:
            st.error("❌ Failed to compare channels. Please check both URLs.")
