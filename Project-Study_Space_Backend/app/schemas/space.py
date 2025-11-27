# app/schemas/space.py
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class SpaceType(str, Enum):
    individual = "individual"
    group = "group"
    meeting = "meeting"
    quiet = "quiet"


class SpaceStatus(str, Enum):
    available = "available"
    unavailable = "unavailable"
    maintenance = "maintenance"


class SpaceBase(BaseModel):
    name: str = Field(..., max_length=100)
    capacity: int = Field(..., gt=0)
    type: SpaceType
    status: SpaceStatus = SpaceStatus.available
    location: str
    description: Optional[str] = None
    equipment: Optional[Dict[str, Any]] = None  # map JSONB


class SpaceCreate(SpaceBase):
    pass


class SpaceUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0)
    type: Optional[SpaceType] = None
    status: Optional[SpaceStatus] = None
    location: Optional[str] = None
    description: Optional[str] = None
    equipment: Optional[Dict[str, Any]] = None


class SpaceResponse(SpaceBase):
    id: int
    average_rating: float = 0.0
    total_ratings: int = 0
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
