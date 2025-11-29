from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.penalty import Penalty, PenaltyType
from app.models.user import User
from app.models.booking import Booking
from app.schemas.penalty import PenaltyCreate, PenaltyUpdate


def create_penalty(db: Session, data: PenaltyCreate) -> Penalty:
    # 1. Check user tồn tại
    user = db.get(User, data.user_id)
    if not user:
        raise HTTPException(404, "User not found")
    # 2. Check booking (nếu có)
    booking = None
    if data.booking_id:
        booking = db.get(Booking, data.booking_id)
        if not booking:
            raise HTTPException(404, "Booking not found")
     # 3. Check trùng penalty cho cùng booking
    if booking:
        exists = db.query(Penalty).filter(
            Penalty.user_id == data.user_id,
            Penalty.booking_id == data.booking_id,
            Penalty.penalty_type == data.penalty_type
        ).first()

        if exists:
            raise HTTPException(409, "Penalty already exists for this booking.")
    # 4. Tính ngày hết hạn (mặc định 30 ngày)
    expires_at = datetime.utcnow() + timedelta(days=30)

    penalty = Penalty(
        user_id=data.user_id,
        booking_id=data.booking_id,
        penalty_type=data.penalty_type,
        points=data.points,
        reason=data.reason,
        expires_at=expires_at
    )

    db.add(penalty)

    # 5. Cập nhật penalty_count của user
    user.penalty_count += data.points

    db.commit()
    db.refresh(penalty)

    return penalty


def get_penalty(db: Session, penalty_id: int) -> Optional[Penalty]:
    return db.get(Penalty, penalty_id)


def list_penalties(db: Session, skip: int = 0, limit: int = 100) -> List[Penalty]:
    stmt = select(Penalty).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def list_user_penalties(db: Session, user_id: int) -> List[Penalty]:
    stmt = select(Penalty).where(Penalty.user_id == user_id)
    return db.execute(stmt).scalars().all()


def update_penalty(db: Session, penalty: Penalty, data: PenaltyUpdate) -> Penalty:
    update_data = data.model_dump(exclude_unset=True)

    # Không được đổi user_id, booking_id, penalty_type
    disallowed = ["user_id", "booking_id", "penalty_type"]
    for key in disallowed:
        if key in update_data:
            raise HTTPException(400, f"Cannot modify {key}")

    for field, value in update_data.items():
        setattr(penalty, field, value)

    db.commit()
    db.refresh(penalty)
    return penalty


def delete_penalty(db: Session, penalty: Penalty) -> None:
    user = penalty.user

    # Trả lại penalty_count cho user
    user.penalty_count -= penalty.points
    if user.penalty_count < 0:
        user.penalty_count = 0

    db.delete(penalty)
    db.commit()
