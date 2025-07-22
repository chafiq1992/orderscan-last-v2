from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path

from . import database, crud, schemas
from .models import Base

app = FastAPI(title="Order‑Scanner API")

# ------------------------------------------------------------------
# 🔑  Static UI mount  (frontend lives at project‑root/frontend)
# In the Docker image:  /app/frontend/scan.html
# ------------------------------------------------------------------
FRONT_DIR = Path("/app/frontend")                  # absolute path is safest
if not FRONT_DIR.exists():
    raise RuntimeError(f"Frontend directory not found: {FRONT_DIR}")

app.mount("/", StaticFiles(directory=FRONT_DIR, html=True), name="frontend")

# ------------------------------------------------------------------
# CORS ‑ allow everything (adjust if you lock down origins later)
# ------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# DB dependency
# ------------------------------------------------------------------
async def get_db() -> AsyncSession:
    async with database.AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# ------------------------------------------------------------------
# Start‑up: auto‑create tables if they don’t exist
# ------------------------------------------------------------------
@app.on_event("startup")
async def on_startup() -> None:
    try:
        async with database.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except SQLAlchemyError as exc:
        # Log and crash so Cloud Run restart will surface error
        import logging
        logging.exception("DB connection failed at startup: %s", exc)
        raise

# ------------------------------------------------------------------
# REST endpoints
# ------------------------------------------------------------------
@app.post("/scan", response_model=schemas.ScanOut)
async def scan(data: schemas.ScanIn, db: AsyncSession = Depends(get_db)):
    return await crud.append_scan(db, data)

@app.get("/tags/summary")
async def tags_summary(db: AsyncSession = Depends(get_db)):
    return await crud.tag_summary(db)
