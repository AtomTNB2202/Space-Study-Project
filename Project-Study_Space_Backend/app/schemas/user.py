# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime
from typing import Optional


class UserRole(str, Enum):
    admin = "admin"
    student = "student"
    lecturer = "lecturer"


# ------------ BASE (FE không được gửi role/is_active) ------------
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str


# ------------ CREATE USER ------------
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str

    class Config:
        extra = "forbid"


# ------------ UPDATE USER (chỉ cho phép đổi một số field) ------------
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None

    class Config:
        extra = "forbid"


# ------------ RESPONSE (không trả về password, không trả về bookings) ------------
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
