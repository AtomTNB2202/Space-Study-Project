# app/models/reservation.py
from sqlalchemy import (
    Column, Integer, DateTime, Text, ForeignKey
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func

from app.core.database import Base
from sqlalchemy.orm import relationship

reservation_status_enum = ENUM(
    "pending",
    "confirmed",
    "checked_in",
    "completed",
    "cancelled",
    "no_show",
    name="reservation_status_enum",
    create_type=False,
)


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)
    space_id = Column(Integer, ForeignKey("spaces.id", ondelete="CASCADE"), nullable=False)

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    status = Column(reservation_status_enum, nullable=False, default="pending")

    check_in_time = Column(DateTime(timezone=True), nullable=True)
    check_out_time = Column(DateTime(timezone=True), nullable=True)

    qr_code_data = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    penalties = relationship(
        "Penalty",
        back_populates="reservation",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
