from datetime import datetime, timedelta
from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship

from app.core.database import Base

class PenaltyType(str, PyEnum):
    no_show = "no_show"
    late_checkout = "late_checkout"
    damage = "damage"
    unauthorized_use = "unauthorized_use"


class Penalty(Base):
    __tablename__ = "penalties"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 💥 FIXED: dùng booking_id, không còn reservation
    booking_id = Column(
        Integer,
        ForeignKey("bookings.id", ondelete="SET NULL"),
        nullable=True,
    )

    penalty_type = Column(
        SQLEnum(PenaltyType, name="penalty_type_enum", create_type=True),
        nullable=False,
    )

    points = Column(Integer, nullable=False, default=1)
    reason = Column(Text, nullable=True)

    expires_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # relationships
    user = relationship("User", back_populates="penalties")
    booking = relationship("Booking", back_populates="penalties")
