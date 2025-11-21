# app/crud/space.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.space import Space
from app.schemas.space import SpaceCreate, SpaceUpdate


def get_space(db: Session, space_id: int) -> Optional[Space]:
    return db.get(Space, space_id)


def get_spaces(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 100,
) -> List[Space]:
    stmt = select(Space).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def create_space(db: Session, space_in: SpaceCreate) -> Space:
    db_space = Space(
        name=space_in.name,
        capacity=space_in.capacity,
        type=space_in.type.value,
        status=space_in.status.value,
        location=space_in.location,
        description=space_in.description,
        equipment=space_in.equipment,
    )
    db.add(db_space)
    db.commit()
    db.refresh(db_space)
    return db_space


def update_space(db: Session, db_space: Space, space_in: SpaceUpdate) -> Space:
    data = space_in.model_dump(exclude_unset=True)

    for field, value in data.items():
        # Enum -> string
        if hasattr(value, "value"):
            value = value.value
        setattr(db_space, field, value)

    db.commit()
    db.refresh(db_space)
    return db_space


def soft_delete_space(db: Session, db_space: Space) -> Space:
    db_space.is_active = False
    db.commit()
    db.refresh(db_space)
    return db_space
