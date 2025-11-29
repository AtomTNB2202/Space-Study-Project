# app/schemas/booking.py
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ===========================
#   ENUM
# ===========================

class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    checked_in = "checked_in"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"


# ===========================
#   BASE CLASS
# ===========================

class BookingBase(BaseModel):
    space_id: int = Field(..., gt=0)
    start_time: datetime
    end_time: datetime



# ===========================
#   CREATE
# ===========================

class BookingCreate(BookingBase):
    qr_code_data: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        extra = "forbid"



# ===========================
#   UPDATE
# ===========================

class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    qr_code_data: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        extra = "forbid"



# ===========================
#   RESPONSE
# ===========================

class BookingResponse(BaseModel):
    id: int

    user_id: int
    space_id: int

    start_time: datetime
    end_time: datetime
    status: BookingStatus

    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None

    qr_code_data: Optional[str] = None
    notes: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

