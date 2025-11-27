# app/crud/rating.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.rating import Rating
from app.schemas.rating import RatingCreate, RatingUpdate


def list_ratings(db: Session) -> List[Rating]:
    return db.query(Rating).order_by(Rating.id.desc()).all()


def get_rating(db: Session, rating_id: int) -> Optional[Rating]:
    return db.get(Rating, rating_id)


def create_rating(db: Session, data: RatingCreate) -> Rating:
    obj = Rating(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_rating(db: Session, db_obj: Rating, updates: RatingUpdate) -> Rating:
    data = updates.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(db_obj, k, v)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_rating(db: Session, db_obj: Rating):
    db.delete(db_obj)
    db.commit()
