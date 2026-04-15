from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from app.api.v1.router import api_router

app = FastAPI(
    title="Praktychni 3j Kurs API",
    version="0.1.0",
    description="Basic FastAPI setup for course practicals.",
)

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
