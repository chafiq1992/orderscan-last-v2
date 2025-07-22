from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from . import database, crud, schemas
from .models import Base
from fastapi.staticfiles import StaticFiles
import pathlib

app = FastAPI(title="Order‑Scanner API")

FRONT_DIR = pathlib.Path(__file__).parent.parent / "app" / "frontend"
app.mount("/", StaticFiles(directory=FRONT_DIR, html=True), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db() -> AsyncSession:
    async with database.AsyncSessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup() -> None:
    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/scan", response_model=schemas.ScanOut)
async def scan(data: schemas.ScanIn, db: AsyncSession = Depends(get_db)):
    return await crud.append_scan(db, data)

@app.get("/tags/summary")
async def tags_summary(db: AsyncSession = Depends(get_db)):
    return await crud.tag_summary(db)
