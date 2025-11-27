# app/schemas/utility.py
from pydantic import BaseModel
from typing import Optional


class UtilityBase(BaseModel):
    key: str
    label: str
    description: Optional[str] = None


class UtilityCreate(UtilityBase):
    pass


class UtilityUpdate(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None


class UtilityResponse(UtilityBase):
    id: int

    class Config:
        from_attributes = True  # cho phép đọc từ ORM model
