# app/models/space.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base


class Space(Base):
    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True, index=True)

    # Core info
    name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)      # individual / group / meeting / quiet
    status = Column(String(20), nullable=False, default="available")
    location = Column(String, nullable=False)

    # Optional metadata
    description = Column(String, nullable=True)
    equipment = Column(JSONB, nullable=True)       # map JSONB

    # Rating summary
    average_rating = Column(Float, nullable=False, server_default="0")
    total_ratings = Column(Integer, nullable=False, server_default="0")

    # Active flag
    is_active = Column(Boolean, nullable=False, server_default="true")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
