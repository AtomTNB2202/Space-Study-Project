from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime


class UserRole(str, Enum):
    admin = "admin"
    student = "student"
    tutor = "tutor"


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: UserRole = UserRole.student
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
