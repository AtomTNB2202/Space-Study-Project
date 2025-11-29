# app/schemas/utility.py
from pydantic import BaseModel
from typing import Optional


class UtilityBase(BaseModel):
    key: str
    label: str
    description: Optional[str] = None

# CREATE: FE được gửi key + label + description
class UtilityCreate(BaseModel):
    key: str
    label: str
    description: Optional[str] = None

    class Config:
        extra = "forbid"


# UPDATE: chỉ cho sửa label + description
class UtilityUpdate(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None

    class Config:
        extra = "forbid"


# RESPONSE: gửi thêm id
class UtilityResponse(UtilityBase):
    id: int

    class Config:
        from_attributes = True
