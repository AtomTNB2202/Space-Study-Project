from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

def __repr__(self):
    return f"<Booking id={self.id} user={self.user_id} space={self.space_id}>"

booking_status_enum = ENUM(
    "pending",
    "confirmed",
    "checked_in",
    "completed",
    "cancelled",
    "no_show",
    name="booking_status_enum",
    create_type=False,  # nếu không dùng Alembic -> đổi thành True
)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    space_id = Column(Integer, ForeignKey("spaces.id", ondelete="CASCADE"), nullable=False)

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    status = Column(
        booking_status_enum,
        nullable=False,
        server_default="pending"
    )

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

    # 🔥 Relationship
    user = relationship("User", back_populates="bookings")
    space = relationship("Space", back_populates="bookings")
    penalties = relationship("Penalty", back_populates="booking", cascade="all, delete-orphan")
