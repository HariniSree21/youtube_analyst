# 📊 YouTube Channel Analyzer

An AI-powered tool that analyzes YouTube channels using the YouTube Data API. It uses **FastAPI** for the backend, **Streamlit** for the frontend, and generates downloadable **PDF reports** with AI-generated insights using Gemini or OpenAI GPT.

---

## 🚀 Features

- 🔍 Analyze YouTube channels by URL
- 📈 Extract subscriber count, views, video stats, and top 5 videos
- 🤖 AI-generated content & strategy analysis (Gemini or OpenAI GPT)
- 📝 Downloadable PDF report
- ⚙️ Built with FastAPI, Streamlit, Docker
- ✅ Compare two YouTube channels

---
```
## 🗂️ Project Structure
📁 backend/
│ ├── db/
│ ├── services/
│ ├── utils/
│ ├── main.py
│ ├── Dockerfile
│ └── requirements.txt
📁 frontend/
│ ├── app.py
│ ├── Dockerfile
│ └── requirements.txt
📁 assets/
│ └── pdfs/ # ✅ PDF reports saved here
📁 reports/ # Optional logs/reports
📄 .env # Secrets (API keys, DB config)
📄 docker-compose.yml
📄 README.md
```
---

##✅ backend/requirements.txt
```
txt
Copy code
fastapi
uvicorn
pydantic
python-dotenv
google-api-python-client
fpdf
openai  # or use 'google-generativeai' if you're using Gemini
```
---

##✅ frontend/requirements.txt
```
txt
Copy code
streamlit
requests
pandas
matplotlib  # (if you’re using charts)
```
---

## ✅ Requirements
```
- Docker & Docker Compose installed
- YouTube Data API v3 Key
- Gemini API Key **or** OpenAI API Key
```
---

## 🔑 Environment Configuration

Create a `.env` file in the **project root**:

```env
YOUTUBE_API_KEY=your_youtube_api_key
GEMINI_API_KEY=your_gemini_api_key  # or use OPENAI_API_KEY
PGUSER=your_pg_user
PGPASSWORD=your_pg_password
PGHOST=your_pg_host
PGDATABASE=your_database_name
PGSSLMODE=require"""
```
---

##🐳 Run with Docker
```
bash
docker-compose up --build
```
---

##🧪 Run Locally Without Docker
```
▶️ Backend (FastAPI)
bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
---

🖥️ Frontend (Streamlit)
```
bash

cd frontend
pip install -r requirements.txt
streamlit run app.py
```
---

##📄 PDF Reports
```
Automatically saved to: assets/pdfs/

Includes:

Channel name, stats, and top videos

AI-generated content analysis

Strategy recommendations
```
---

##🔑 How to Get a YouTube Data API Key
```
📌 Step-by-Step:
Go to Google Cloud Console
🔗 https://console.cloud.google.com/

Create a New Project

Click the dropdown at the top

Click “New Project”

Name it something like YouTubeAnalyzer and click Create

Enable the YouTube Data API v3

Inside your project, go to:
🔗 https://console.cloud.google.com/apis/library/youtube.googleapis.com

Click Enable

Create API Credentials

Navigate to:
🔗 https://console.cloud.google.com/apis/credentials

Click “Create Credentials” → API Key

Copy the API key shown. This is your YOUTUBE_API_KEY

(Optional but Recommended): Restrict your API Key

Click on the API key → “Restrict Key”

Set Application Restrictions to "None" or "HTTP referrers"

Set API Restrictions to: ✅ YouTube Data API v3
```
---

##🤖 How to Get a Gemini API Key (Google AI)
```
📌 Step-by-Step:
Go to Google AI Studio
🔗 https://aistudio.google.com/app/apikey

Sign in with your Google account

Click "Create API Key"

A key will be shown. Copy it. This is your GEMINI_API_KEY

(Optional): Read API usage limits
🔗 https://ai.google.dev/pricing
##🛡️ Where to Store These Keys
```
---

Place them in a .env file in your project root:
---
```
YOUTUBE_API_KEY=your_actual_youtube_api_key
GEMINI_API_KEY=your_actual_gemini_api_key
Your backend will load this securely using python-dotenv
```


