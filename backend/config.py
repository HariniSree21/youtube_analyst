# backend/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

    PGUSER = os.getenv("PGUSER")
    PGPASSWORD = os.getenv("PGPASSWORD")
    PGHOST = os.getenv("PGHOST")
    PGDATABASE = os.getenv("PGDATABASE")
    PGSSLMODE = os.getenv("PGSSLMODE", "require")

    # Construct the SQLAlchemy-compatible URL
    DATABASE_URL = (
        f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}"
        f"?sslmode={PGSSLMODE}"
    )
