# app/schemas/penalty.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.penalty import PenaltyType


# ---------- Base ----------
class PenaltyBase(BaseModel):
    penalty_type: PenaltyType
    points: int = 1
    reason: Optional[str] = None


# ---------- Create (ADMIN ONLY) ----------
class PenaltyCreate(PenaltyBase):
    user_id: int
    booking_id: Optional[int] = None

    class Config:
        extra = "forbid"


# ---------- Update (ADMIN ONLY) ----------
class PenaltyUpdate(BaseModel):
    points: Optional[int] = None
    reason: Optional[str] = None

    class Config:
        extra = "forbid"


# ---------- Output ----------
class PenaltyOut(BaseModel):
    id: int
    user_id: int
    booking_id: Optional[int]
    penalty_type: PenaltyType
    points: int
    reason: Optional[str]
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
