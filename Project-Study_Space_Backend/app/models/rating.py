# app/models/rating.py
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, func
from app.core.database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)

    # CHÚ Ý: FK phải trỏ đúng tên bảng trong Reservation.__tablename__
    booking_id = Column(
        Integer,
        ForeignKey("reservations.id", ondelete="CASCADE"),  # hoặc "bookings.id" nếu bạn đã đổi tên bảng
        nullable=False,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    rating = Column(Integer, nullable=False)  # 1–5
    comment = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ⚠️ TẠM THỜI BỎ HẾT RELATIONSHIP ĐỂ ĐỠ RỐI
    # from sqlalchemy.orm import relationship
    # booking = relationship("Reservation")
    # user = relationship("User")
