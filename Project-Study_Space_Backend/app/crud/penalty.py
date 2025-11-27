from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.penalty import Penalty
from app.schemas.penalty import PenaltyCreate, PenaltyUpdate


def create_penalty(db: Session, data: PenaltyCreate) -> Penalty:
    penalty = Penalty(**data.dict())
    db.add(penalty)
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
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(penalty, field, value)
    db.commit()
    db.refresh(penalty)
    return penalty


def delete_penalty(db: Session, penalty: Penalty) -> None:
    db.delete(penalty)
    db.commit()
