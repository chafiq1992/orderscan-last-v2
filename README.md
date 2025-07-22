# Order Scanner (FastAPI + Cloud Run)

Ready‑to‑deploy rewrite of the Apps Script barcode scanner.

## Quick Start

```bash
docker run --name pg -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=orders -p 5432:5432 -d postgres:15
export DB_USER=postgres DB_PASS=pass DB_NAME=orders INSTANCE_CONNECTION_NAME=local
cd backend && uvicorn app.main:app --reload
```

Open `frontend/scan.html` in your browser, scan a barcode, and watch it hit the FastAPI endpoint.

## Deployment

1. Create a Cloud SQL Postgres instance and note its **connection name**.
2. Create a GitHub repo and add the secrets shown in `.github/workflows/deploy.yml`.
3. Push → GitHub Actions builds the container and deploys to Cloud Run.

