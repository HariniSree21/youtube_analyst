# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ .


# Default run command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
