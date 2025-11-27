# app/schemas/rating.py
from pydantic import BaseModel, Field
from typing import Optional


class RatingBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class RatingCreate(RatingBase):
    booking_id: int
    user_id: int   # lấy từ token thì khỏi gửi từ client → mình sẽ override trong router


class RatingUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class RatingResponse(RatingBase):
    id: int
    booking_id: int
    user_id: int

    class Config:
        from_attributes = True
