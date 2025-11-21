from sqlalchemy import Column, Integer, String, Boolean, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    student = "student"
    tutor = "tutor"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.student)
    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now())
