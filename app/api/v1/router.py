from fastapi import APIRouter

from app.api.v1.endpoints import auth, orders, posts, products, reservations, users

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(products.router)
api_router.include_router(auth.router)
api_router.include_router(posts.router)
api_router.include_router(orders.router)
api_router.include_router(reservations.router)
