from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.penalty import PenaltyType


class PenaltyBase(BaseModel):
    user_id: int
    reservation_id: Optional[int] = None
    penalty_type: PenaltyType
    points: int = 1
    reason: Optional[str] = None
    expires_at: datetime


class PenaltyCreate(PenaltyBase):
    # Khi tạo mới penalty, admin truyền đủ thông tin ở trên
    pass


class PenaltyUpdate(BaseModel):
    penalty_type: Optional[PenaltyType] = None
    points: Optional[int] = None
    reason: Optional[str] = None
    expires_at: Optional[datetime] = None


class PenaltyOut(PenaltyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
