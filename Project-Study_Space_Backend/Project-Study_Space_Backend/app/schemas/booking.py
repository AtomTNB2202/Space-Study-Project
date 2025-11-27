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
    """
    Base schema của Booking
    Dùng chung cho cả Create và Response
    """
    user_id: int = Field(..., gt=0)
    space_id: int = Field(..., gt=0)

    start_time: datetime
    end_time: datetime

    status: BookingStatus = BookingStatus.pending


# ===========================
#   CREATE
# ===========================

class BookingCreate(BookingBase):
    """
    Body cho POST /bookings
    qr_code_data & notes là optional
    """
    qr_code_data: Optional[str] = None
    notes: Optional[str] = None


# ===========================
#   UPDATE
# ===========================

class BookingUpdate(BaseModel):
    """
    Body cho PATCH /bookings/{id}
    Các field optional
    """
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[BookingStatus] = None

    qr_code_data: Optional[str] = None
    notes: Optional[str] = None


# ===========================
#   RESPONSE
# ===========================

class BookingResponse(BookingBase):
    """
    Object trả về cho client
    """
    id: int

    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None

    qr_code_data: Optional[str] = None
    notes: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
