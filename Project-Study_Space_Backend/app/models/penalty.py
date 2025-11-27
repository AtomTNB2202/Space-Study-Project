from datetime import datetime
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
    reservation_id = Column(
        Integer,
        ForeignKey("reservations.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Khớp với schema.sql: penalty_type ENUM penalty_type_enum NOT NULL
    penalty_type = Column(
        SQLEnum(PenaltyType, name="penalty_type_enum", create_type=False),
        nullable=False,
    )

    points = Column(Integer, nullable=False, default=1)
    reason = Column(Text, nullable=True)

    # Khớp với schema.sql: expires_at TIMESTAMPTZ NOT NULL
    expires_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    user = relationship("User", back_populates="penalties")
    reservation = relationship("Reservation", back_populates="penalties")
