# app/crud/space.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.space import Space
from app.schemas.space import SpaceCreate, SpaceUpdate


def get_spaces(
    db: Session,
    *,
    search: Optional[str] = None,
    min_capacity: Optional[int] = None,
    status: Optional[str] = None,
) -> List[Space]:
    stmt = select(Space).where(Space.is_active.is_(True))

    if search:
        like = f"%{search}%"
        stmt = stmt.where(
            (Space.name.ilike(like)) |
            (Space.location.ilike(like))
        )

    if min_capacity is not None:
        stmt = stmt.where(Space.capacity >= min_capacity)

    if status is not None:
        stmt = stmt.where(Space.status == status)

    return db.execute(stmt).scalars().all()


def get_space(db: Session, space_id: int) -> Optional[Space]:
    return db.get(Space, space_id)


def create_space(db: Session, data: SpaceCreate) -> Space:
    space = Space(**data.model_dump())
    db.add(space)
    db.commit()
    db.refresh(space)
    return space


def update_space(db: Session, db_space: Space, updates: SpaceUpdate) -> Space:
    data = updates.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_space, key, value)

    db.commit()
    db.refresh(db_space)
    return db_space


def soft_delete_space(db: Session, db_space: Space) -> Space:
    db_space.is_active = False
    db.commit()
    db.refresh(db_space)
    return db_space
