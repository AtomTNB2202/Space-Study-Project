# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1 import bookings, spaces, users, auth, utilities, ratings
from app.api.v1 import penalties as penalties_router
from app.api.v1 import admin as admin_router

api_router = APIRouter()

api_router.include_router(spaces.router, prefix="/spaces", tags=["Spaces"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(utilities.router, prefix="/utilities", tags=["Utilities"])
api_router.include_router(ratings.router, prefix="/ratings", tags=["Ratings"])
api_router.include_router(penalties_router.router, prefix="/api/v1")
api_router.include_router(admin_router.router, prefix="/api/v1")