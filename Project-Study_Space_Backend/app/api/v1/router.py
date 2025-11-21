# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1 import spaces, reservations, users

api_router = APIRouter()

api_router.include_router(spaces.router, prefix="/spaces", tags=["Spaces"])
api_router.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
