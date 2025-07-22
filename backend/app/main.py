from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from . import database, crud, schemas
from .models import Base

app = FastAPI(title="Order‑Scanner API")

# ---------------------------------------------------------------
# 🔗  Serve the UI  (root‑level frontend is copied to /app/frontend)
# ---------------------------------------------------------------
FRONT_DIR = Path("/app/frontend")           # absolute path ✔
if not FRONT_DIR.exists():
    raise RuntimeError(f"Frontend directory missing: {FRONT_DIR}")

app.mount("/", StaticFiles(directory=FRONT_DIR, html=True), name="frontend")

# ---------------------------------------------------------------
# CORS
# ---------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------
# DB dependency
# ---------------------------------------------------------------
async def get_db() -> AsyncSession:
    async with database.AsyncSessionLocal() as session:
        yield session

# ---------------------------------------------------------------
# On startup: auto‑create tables
# ---------------------------------------------------------------
@app.on_event("startup")
async def on_startup() -> None:
    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ---------------------------------------------------------------
# REST endpoints
# ---------------------------------------------------------------
@app.post("/scan", response_model=schemas.ScanOut)
async def scan(data: schemas.ScanIn, db: AsyncSession = Depends(get_db)):
    return await crud.append_scan(db, data)

@app.get("/tags/summary")
async def tags_summary(db: AsyncSession = Depends(get_db)):
    return await crud.tag_summary(db)
