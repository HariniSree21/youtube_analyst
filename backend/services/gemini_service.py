#to compare two videos
# backend/services/gemini_service.py

import os
import litellm

# Load Gemini API key from env
litellm.api_key = os.getenv("GEMINI_API_KEY")

def recommend_best_video_gemini(text):
    """
    Uses Gemini to compare two videos and recommend which is better, for whom, and when to watch.
    """
    prompt = f"""
    Compare the following two YouTube videos teaching the same topic.

    For each video, analyze:
    - Content depth and clarity
    - Teaching style and suitability (beginner, intermediate, advanced)
    - Engagement (likes, views, comments)

    Then, recommend:
    1. Which video is better overall and why.
    2. For whom each video is best suited.
    3. When is the best time to watch each (morning, evening, anytime) if relevant.

    Input:

    {text}

    Provide a structured, clear, actionable recommendation.
    """

    response = litellm.completion(
        model="gemini/gemini-1.5-pro",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
