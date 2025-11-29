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
from sqlalchemy.orm import relationship

from app.core.database import Base


class Space(Base):
    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="available")
    location = Column(String, nullable=False)

    description = Column(String, nullable=True)
    equipment = Column(JSONB, nullable=True)

    average_rating = Column(Float, nullable=False, server_default="0")
    total_ratings = Column(Integer, nullable=False, server_default="0")

    is_active = Column(Boolean, nullable=False, server_default="true")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Booking relationship
    bookings = relationship(
        "Booking",
        back_populates="space",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # ⭐ ADD THIS (bạn bị thiếu)
    ratings = relationship(
        "Rating",
        back_populates="space",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

