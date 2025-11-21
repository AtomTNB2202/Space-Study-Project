# app/models/space.py
from sqlalchemy import Column, Integer, String, Boolean, Text, Numeric
from sqlalchemy.dialects.postgresql import JSONB, ENUM

from app.core.database import Base

# Map tới ENUM đã tạo trong schema.sql
space_type_enum = ENUM(
    "individual",
    "group",
    "meeting",
    "quiet",
    name="space_type_enum",
    create_type=False,  # KHÔNG tạo lại enum trong DB
)

space_status_enum = ENUM(
    "available",
    "unavailable",
    "maintenance",
    name="space_status_enum",
    create_type=False,
)


class Space(Base):
    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    type = Column(space_type_enum, nullable=False)
    status = Column(space_status_enum, nullable=False, default="available")
    location = Column(String(255), nullable=False)
    description = Column(Text)
    equipment = Column(JSONB)
    average_rating = Column(Numeric(3, 2), nullable=False, default=0.0)
    total_ratings = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<Space id={self.id} name='{self.name}'>"
