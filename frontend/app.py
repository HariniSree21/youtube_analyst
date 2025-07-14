import streamlit as st
import requests
import os
import pandas as pd
from frontend_utils import plot_bar_comparison

API_URL = "http://localhost:8000"  # Change if deployed remotely

st.set_page_config(page_title="YouTube Analyzer", page_icon="📊", layout="centered")

st.title("📊 YouTube Channel Analyzer")
st.write("Enter a YouTube channel URL below to get AI-powered insights from your favorite creators!")

# --- Analyze Single Channel ---
st.subheader("🔍 Analyze a Channel")

channel_url = st.text_input("YouTube Channel URL")
email = st.text_input("Your Email (optional)", value="anonymous@example.com")

if st.button("Analyze"):
    if not channel_url:
        st.warning("Please enter a valid YouTube channel URL.")
    else:
        with st.spinner("Analyzing channel..."):
            response = requests.post(f"{API_URL}/analyze_channel", json={
                "channel_url": channel_url,
                "user_email": email
            })

        if response.status_code == 200:
            data = response.json()
            stats = data.get("channel_stats", {})
            ai = data.get("ai_recommendations", {})

            st.success("✅ Analysis complete!")

            st.write(f"**Channel Name:** {stats.get('channel_name', '-')}")
            st.write(f"**Subscribers:** {stats.get('subscribers', '-')}")
            st.write(f"**Total Views:** {stats.get('total_views', '-')}")
            st.write(f"**Video Count:** {stats.get('video_count', '-')}")

            st.write("### 🏆 Top Videos")
            for v in stats.get("top_videos", []):
                video_link = v.get("url", "#")
                title = v.get("title", "Untitled")
                views = v.get("views", "0")
                likes = v.get("likes", "0")
                comments = v.get("comments", "0")

                st.markdown(f"""
                <div style="border:1px solid #ddd; padding:10px; border-radius:5px; margin-bottom:10px;">
                    <div style="font-size:16px; font-weight:bold; background-color:#f0f8ff; padding:5px; border-radius:3px;">
                        {title}
                    </div>
                    <div style="margin-top:5px;">
                        {views} views, {likes} likes, {comments} comments
                    </div>
                    <a href="{video_link}" target="_blank">
                        <button style="background-color:#4CAF50;border:none;color:white;padding:5px 10px;text-align:center;text-decoration:none;display:inline-block;font-size:14px;border-radius:5px;cursor:pointer;margin-top:5px;">
                            ▶️ Watch
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)


            st.write("### 🧠 Content Analysis")
            st.markdown(ai.get("content_analysis", "No content analysis available."))

            st.write("### 🚀 Strategy Recommendations")
            st.markdown(ai.get("strategy_recommendation", "No recommendations available."))

            # PDF Download
            pdf_path = data.get("pdf_path")
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📄 Download Report as PDF",
                        data=f,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )
            else:
                st.warning("⚠️ PDF report not found or not generated.")
        else:
            st.error(f"❌ Error: {response.status_code} - {response.json().get('detail')}")

# --- Compare Two Channels ---
st.divider()
st.subheader("⚔️ Compare Two Channels")

col1, col2 = st.columns(2)
with col1:
    ch1 = st.text_input("Channel 1 URL")
with col2:
    ch2 = st.text_input("Channel 2 URL")

if st.button("Compare Channels"):
    if not ch1 or not ch2:
        st.warning("Please enter both channel URLs.")
    else:
        with st.spinner("Comparing channels..."):
            comp_response = requests.post(f"{API_URL}/compare_channels", json={
                "channels": [ch1, ch2]
            })

        if comp_response.status_code == 200:
            result = comp_response.json()
            comps = result.get("comparisons", [])
            growth_tip = result.get("growth_advice", {})

            st.success("✅ Comparison Ready!")

            st.write("### 📊 Channel Comparison Table")

            # Convert to DataFrame with list/dict columns as strings to avoid ArrowTypeError
            comps_cleaned = []
            for item in comps:
                cleaned_item = {}
                for k, v in item.items():
                    if isinstance(v, (list, dict)):
                        cleaned_item[k] = str(v)
                    else:
                        cleaned_item[k] = v
                comps_cleaned.append(cleaned_item)

            df = pd.DataFrame(comps_cleaned)
            st.dataframe(df)

            st.write("### 📈 Subscribers")
            plot_bar_comparison(comps, metric="subscribers")

            st.write("### 🎥 Total Views")
            plot_bar_comparison(comps, metric="total_views")

            st.write("### 📹 Video Count")
            plot_bar_comparison(comps, metric="video_count")

            if growth_tip:
                st.write("### 💡 Growth Opportunity (AI)")

                summary = growth_tip.get("summary", "")
                recommendations = growth_tip.get("recommendations", "")

                if summary:
                    st.write(f"**Summary:** {summary}")

                if recommendations:
                    st.markdown(recommendations)

        else:
            st.error("❌ Failed to compare channels. Please check both URLs and try again.")
