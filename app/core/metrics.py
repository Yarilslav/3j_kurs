from __future__ import annotations

from time import perf_counter

from fastapi import Depends, FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_product, crud_user
from app.db.session import get_db

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests.",
    ("method", "path", "status_code"),
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds.",
    ("method", "path"),
)
USER_COUNT = Gauge(
    "users_total",
    "Current number of users in the database.",
)
PRODUCT_COUNT = Gauge(
    "products_total",
    "Current number of products in the database.",
)


def setup_metrics(app: FastAPI) -> None:
    @app.middleware("http")
    async def prometheus_middleware(request: Request, call_next):
        start = perf_counter()
        response = await call_next(request)

        route = request.scope.get("route")
        path = getattr(route, "path", request.url.path)
        method = request.method
        status_code = str(response.status_code)
        elapsed = perf_counter() - start

        REQUEST_COUNT.labels(method=method, path=path, status_code=status_code).inc()
        REQUEST_LATENCY.labels(method=method, path=path).observe(elapsed)
        return response

    @app.get("/metrics", include_in_schema=False)
    async def metrics(db: AsyncSession = Depends(get_db)) -> Response:
        USER_COUNT.set(await crud_user.get_user_count(db))
        PRODUCT_COUNT.set(await crud_product.get_product_count(db))
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
