# backend/services/youtube_service.py

import os
import re
from googleapiclient.discovery import build
from backend.config import Config
from google.auth.credentials import AnonymousCredentials

API_KEY = Config.YOUTUBE_API_KEY
youtube = build("youtube", "v3", credentials=AnonymousCredentials(), developerKey=API_KEY)


def extract_channel_id(channel_url):
    """Extracts channel ID from full URL if needed."""
    if "channel/" in channel_url:
        return channel_url.split("channel/")[1].split("/")[0]
    elif "user/" in channel_url or "@":
        # Convert user/@handle to channelId using search
        response = youtube.search().list(
            part="snippet",
            q=channel_url,
            type="channel",
            maxResults=1
        ).execute()
        return response["items"][0]["snippet"]["channelId"]
    return channel_url


def extract_video_id(video_url):
    """Extracts video ID from various YouTube URL formats."""
    # For standard watch URLs
    watch_match = re.search(r"v=([a-zA-Z0-9_-]{11})", video_url)
    if watch_match:
        return watch_match.group(1)

    # For youtu.be short URLs
    short_match = re.search(r"youtu\.be/([a-zA-Z0-9_-]{11})", video_url)
    if short_match:
        return short_match.group(1)

    # If only video ID is passed
    if len(video_url) == 11:
        return video_url

    raise ValueError("Invalid YouTube video URL format.")


def get_channel_analysis(channel_url):
    channel_id = extract_channel_id(channel_url)

    # Get channel stats
    channel_response = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    ).execute()

    channel_info = channel_response["items"][0]
    snippet = channel_info["snippet"]
    stats = channel_info["statistics"]

    channel_data = {
        "channel_name": snippet.get("title"),
        "description": snippet.get("description"),
        "subscribers": stats.get("subscriberCount"),
        "total_views": stats.get("viewCount"),
        "video_count": stats.get("videoCount"),
    }

    # Get top videos by view count
    videos = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="viewCount",
        maxResults=5,
        type="video"
    ).execute()

    top_videos = []
    for item in videos["items"]:
        video_id = item["id"]["videoId"]
        video_stats = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        ).execute()["items"][0]

        video_url = f"https://www.youtube.com/watch?v={video_id}"

        top_videos.append({
            "title": video_stats["snippet"]["title"],
            "views": video_stats["statistics"].get("viewCount", "0"),
            "likes": video_stats["statistics"].get("likeCount", "0"),
            "comments": video_stats["statistics"].get("commentCount", "0"),
            "published": video_stats["snippet"]["publishedAt"],
            "url": video_url
        })

    channel_data["top_videos"] = top_videos
    return channel_data


def compare_two_channels(channel_urls):
    result = []
    for url in channel_urls:
        channel_data = get_channel_analysis(url)
        result.append({
            "channel_name": channel_data["channel_name"],
            "subscribers": channel_data["subscribers"],
            "video_count": channel_data["video_count"],
            "total_views": channel_data["total_views"],
            "top_video_views": channel_data["top_videos"][0]["views"] if channel_data["top_videos"] else "0"
        })
    return result


def get_video_details(video_url):
    video_id = extract_video_id(video_url)

    video_response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()

    if not video_response["items"]:
        raise Exception("Video not found.")

    video_info = video_response["items"][0]
    snippet = video_info["snippet"]
    stats = video_info["statistics"]

    # Get top 20 comments
    comments = []
    try:
        comment_response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=20
        ).execute()

        for item in comment_response["items"]:
            comments.append(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])

    except Exception as e:
        comments.append("No comments fetched or comments disabled.")

    return {
        "video_id": video_id,
        "title": snippet.get("title"),
        "description": snippet.get("description"),
        "views": stats.get("viewCount"),
        "likes": stats.get("likeCount"),
        "comments_count": stats.get("commentCount"),
        "comments": comments
    }
