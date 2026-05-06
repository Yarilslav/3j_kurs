from __future__ import annotations

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.router import api_router
from app.core.bootstrap import ensure_root_admin
from app.core.config import settings
from app.core.metrics import setup_metrics
from app.db.session import AsyncSessionLocal, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with AsyncSessionLocal() as session:
        await ensure_root_admin(session)
    yield


app = FastAPI(
    title="Praktychni 3j Kurs API",
    version="0.1.0",
    description="Basic FastAPI setup for course practicals.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_metrics(app)
app.include_router(api_router)


@app.get("/", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/healthz", tags=["health"])
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz", tags=["health"])
async def readyz() -> dict[str, str]:
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
    return {"status": "ready"}


def main() -> None:
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.app_port,
        reload=settings.APP_RELOAD,
    )


if __name__ == "__main__":
    main()
