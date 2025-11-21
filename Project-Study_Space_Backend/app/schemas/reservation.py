from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ReservationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"
    no_show = "no_show"


class ReservationBase(BaseModel):
    user_id: int = Field(..., gt=0)
    space_id: int = Field(..., gt=0)
    start_time: datetime
    end_time: datetime
    status: ReservationStatus = ReservationStatus.pending


class ReservationCreate(ReservationBase):
    """Body dùng cho POST /reservations"""
    pass


class ReservationUpdate(BaseModel):
    """Body dùng cho PATCH /reservations/{id}"""

    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[ReservationStatus] = None


class ReservationResponse(ReservationBase):
    """Schema trả về cho client"""

    id: int
    created_at: Optional[datetime] = None      # cho phép None
    updated_at: Optional[datetime] = None      # cho phép None

    class Config:
        from_attributes = True

