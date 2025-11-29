# app/schemas/rating.py
from pydantic import BaseModel, Field
from typing import Optional


class RatingBase(BaseModel):
    score: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class RatingCreate(RatingBase):
    space_id: int = Field(..., gt=0)

    class Config:
        extra = "forbid"


class RatingUpdate(BaseModel):
    comment: Optional[str] = None

    class Config:
        extra = "forbid"


class RatingResponse(BaseModel):
    id: int
    user_id: int
    space_id: int
    score: int
    comment: Optional[str]
    
    class Config:
        from_attributes = True
