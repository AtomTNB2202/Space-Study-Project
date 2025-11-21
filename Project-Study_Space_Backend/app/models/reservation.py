# app/models/reservation.py
from sqlalchemy import Column, Integer, DateTime, String, func, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM

from app.core.database import Base

# Enum status (đảm bảo trùng với enum trong schema.sql)
reservation_status_enum = ENUM(
    "pending",
    "confirmed",
    "cancelled",
    "completed",
    "no_show",
    name="reservation_status_enum",
    create_type=False,  # enum đã tạo trong DB, không tạo lại
)


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)

    # KHÔNG dùng ForeignKey ở ORM cho users (vì mình chưa có model User)
    user_id = Column(Integer, nullable=False)

    # spaces đã có model Space, nên dùng FK được
    space_id = Column(Integer, ForeignKey("spaces.id", ondelete="CASCADE"), nullable=False)

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    status = Column(reservation_status_enum, nullable=False, default="pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Reservation id={self.id} user_id={self.user_id} space_id={self.space_id}>"
