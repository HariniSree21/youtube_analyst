# 📊 YouTube Channel Analyzer

An AI-powered tool that analyzes YouTube channels using the YouTube Data API. It uses FastAPI for backend, Streamlit for frontend, and generates downloadable PDF reports with AI-generated insights.

---

## 🚀 Features

- 🔍 Analyze YouTube channels by URL
- 📈 Extract subscriber count, views, video stats, and top videos
- 🤖 AI-generated content & strategy analysis (Gemini/GPT API)
- 📝 PDF report generation
- ⚙️ Built with FastAPI, Streamlit, Docker
- ✅ Easily compare two channels

---

## 🗂️ Project Structure
📁 backend/
├── db/
├── services/
├── utils/
├── main.py
├── Dockerfile
└── requirements.txt

📁 frontend/
├── app.py
├── Dockerfile
└── requirements.txt

📁 assets/
📁 reports/
📄 .env
📄 docker-compose.yml
📄 README.md
✅ backend/requirements.txt
txt
Copy code
fastapi
uvicorn
pydantic
python-dotenv
google-api-python-client
fpdf
openai  # or use 'google-generativeai' if you're using Gemini
✅ frontend/requirements.txt
txt
Copy code
streamlit
requests
pandas
matplotlib  # (if you’re using charts)

## 🧪 Requirements

- Docker & Docker Compose installed
- Google Developer API Key for YouTube Data API v3
- Gemini/GPT API Key (if using AI features)

- ## 🔑 Environment Configuration

Create a `.env` file in the project root:

```env
YOUTUBE_API_KEY=your_youtube_api_key
GEMINI_API_KEY=your_gemini_api_key
PGUSER=your_pg_user
PGPASSWORD=your_pg_password
PGHOST=your_pg_host
PGDATABASE=your_database_name
PGSSLMODE=require
🐳 Run with Docker
bash
Copy code
docker-compose up --build
##Run Locally Without Docker
Backend (FastAPI)
bash
Copy code
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
## Frontend (Streamlit)
bash
Copy code
cd frontend
pip install -r requirements.txt
streamlit run app.py
📄 PDF Reports
Automatically saved to: assets/pdfs/

Include AI insights, top videos, and strategy
🔧 Troubleshooting
502 Bad Gateway or Connection Refused
➤ Ensure the backend is running before launching frontend.
➤ Check port mappings in docker-compose.yml.

No module named 'backend'
➤ Ensure you’re using relative imports (not from backend...)
➤ Set ENV PYTHONPATH=/app in the Dockerfile.

PDF not generating?
➤ Make sure assets/pdfs/ exists and has write permissions.
🔄 API Endpoints (FastAPI)
Method	Endpoint	Description
POST	/analyze_channel	Analyze a single channel
POST	/compare_channels	Compare two channels
POST	/generate_report	Download PDF for a channel



