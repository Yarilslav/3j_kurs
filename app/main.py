"""FastAPI application entry point.

This module defines the ASGI app object and a simple runner for development.
"""

from __future__ import annotations

# FastAPI provides the web framework and routing primitives.
from fastapi import FastAPI

from app.api.v1.endpoints import auth, posts, products, users

# Uvicorn is the ASGI server used to run the app locally.
import uvicorn

# Create the application instance with minimal metadata.
# These values show up in the automatic docs at /docs.
app = FastAPI(
    title="Praktychni 3j Kurs API",
    version="0.1.0",
    description="Basic FastAPI setup for course practicals.",
)

# Register the users router directly.
app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(posts.router)


@app.get("/", tags=["health"])
def health_check() -> dict[str, str]:
    """Simple health endpoint.

    Keeping this small makes it easy to verify the server is alive.
    """

    # A predictable response is handy for tests and manual checks.
    return {"status": "ok"}


def main() -> None:
    """Run the development server.

    We use `reload=True` so code changes are picked up automatically.
    """

    # Point Uvicorn at the import path so reload works reliably.
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


# Allow `python -m praktychni_3j_kurs.main` in addition to `poetry run`.
if __name__ == "__main__":
    main()
