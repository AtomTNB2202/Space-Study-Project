# app/crud/rating.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.rating import Rating
from app.schemas.rating import RatingCreate, RatingUpdate

from fastapi import HTTPException
from app.models.booking import Booking
from app.models.space import Space


def list_ratings(db: Session) -> List[Rating]:
    return db.query(Rating).order_by(Rating.id.desc()).all()


def get_rating(db: Session, rating_id: int) -> Optional[Rating]:
    return db.get(Rating, rating_id)


def create_rating(db: Session, data: RatingCreate, current_user_id: int):
    # 1. Check Space tồn tại và active
    space = db.query(Space).filter(Space.id == data.space_id, Space.is_active == True).first()
    if not space:
        raise HTTPException(404, "Space not found or inactive.")

    # 2. Check user đã từng completed booking không
    completed = db.query(Booking).filter(
        Booking.user_id == current_user_id,
        Booking.space_id == data.space_id,
        Booking.status == "completed"
    ).first()

    if not completed:
        raise HTTPException(403, "You can rate only after completing a booking.")

    # 3. Check user đã rating phòng này chưa
    existing = db.query(Rating).filter(
        Rating.user_id == current_user_id,
        Rating.space_id == data.space_id,
    ).first()

    if existing:
        raise HTTPException(409, "You have already rated this space.")

    # 4. Tạo rating
    obj = Rating(
        user_id=current_user_id,
        space_id=data.space_id,
        score=data.score,
        comment=data.comment,
    )
    db.add(obj)

    # 5. Cập nhật lại average_rating của Space
    space.total_ratings += 1
    space.average_rating = (
        (space.average_rating * (space.total_ratings - 1)) + data.score
    ) / space.total_ratings

    db.commit()
    db.refresh(obj)
    return obj


def update_rating(db: Session, db_obj: Rating, updates: RatingUpdate, current_user_id: int):
    if db_obj.user_id != current_user_id:
        raise HTTPException(403, "You cannot edit someone else's rating.")

    data = updates.model_dump(exclude_unset=True)

    # Không cho sửa điểm (score) sau khi rating
    if "score" in data:
        raise HTTPException(400, "You cannot change rating score.")

    for k, v in data.items():
        setattr(db_obj, k, v)

    db.commit()
    db.refresh(db_obj)
    return db_obj



def delete_rating(db: Session, db_obj: Rating, current_user_id: int):
    if db_obj.user_id != current_user_id:
        raise HTTPException(403, "You cannot delete others' rating.")

    db.delete(db_obj)
    db.commit()

