# app/schemas/space.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum


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
    equipment: Optional[Dict[str, Any]] = None


class SpaceCreate(SpaceBase):
    """Body cho POST /spaces"""
    pass


class SpaceUpdate(BaseModel):
    """Body cho PATCH /spaces/{id}"""

    name: Optional[str] = Field(None, max_length=100)
    capacity: Optional[int] = Field(None, gt=0)
    type: Optional[SpaceType] = None
    status: Optional[SpaceStatus] = None
    location: Optional[str] = None
    description: Optional[str] = None
    equipment: Optional[Dict[str, Any]] = None


class SpaceResponse(SpaceBase):
    """Schema trả về client"""

    id: int
    average_rating: float
    total_ratings: int
    is_active: bool

    class Config:
        from_attributes = True  # cho phép trả trực tiếp SQLAlchemy object
