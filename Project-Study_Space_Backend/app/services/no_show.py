from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.user import User
from app.models.penalty import Penalty, PenaltyType

GRACE_PERIOD_MINUTES = 15


def process_no_show_bookings(db: Session):
    now = datetime.utcnow()

    # Lấy tất cả booking quá hạn check-in
    overdue = db.query(Booking).filter(
        Booking.status.in_(["pending", "confirmed"]),
        Booking.start_time + timedelta(minutes=GRACE_PERIOD_MINUTES) < now
    ).all()

    for booking in overdue:
        # Nếu đã bị xử lý no-show → bỏ qua
        existing_penalty = db.query(Penalty).filter(
            Penalty.booking_id == booking.id,
            Penalty.type == PenaltyType.no_show,
        ).first()

        if existing_penalty:
            continue

        # 1) Cập nhật trạng thái booking
        booking.status = "no_show"

        # 2) Tạo penalty
        penalty = Penalty(
            user_id=booking.user_id,
            booking_id=booking.id,
            type=PenaltyType.no_show,
            reason="User did not check in on time."
        )
        db.add(penalty)

        # 3) Tăng penalty_count
        user = db.query(User).filter(User.id == booking.user_id).first()
        if user:
            user.penalty_count += 1

    db.commit()

    return len(overdue)
