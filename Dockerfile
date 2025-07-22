# order-scanner/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# 1) install deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) copy backend code
COPY backend/app       ./app

# 3) copy frontend (now inside backend)
COPY backend/frontend  ./frontend

# 4) run FastAPI
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port", "8080"]
