from __future__ import annotations

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.bootstrap import ensure_root_admin
from app.core.metrics import setup_metrics
from app.db.session import AsyncSessionLocal


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

setup_metrics(app)
app.include_router(api_router)


@app.get("/", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


def main() -> None:
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
