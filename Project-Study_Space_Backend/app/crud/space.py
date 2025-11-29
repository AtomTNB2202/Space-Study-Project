# app/crud/space.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app.models.booking import Booking

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

    # Only check booking conflict if changing capacity or status
    changing_capacity = "capacity" in data
    changing_status = "status" in data

    # Query active bookings
    active_bookings = db.query(Booking).filter(
        Booking.space_id == db_space.id,
        Booking.status.in_(["pending", "confirmed", "checked_in"])
    ).count()

    if changing_capacity:
        new_cap = data["capacity"]
        if new_cap < active_bookings:
            raise HTTPException(
                409,
                f"Cannot reduce capacity below current active bookings ({active_bookings})."
            )
    if changing_status:
        new_status = data["status"]
        if new_status == "unavailable" and active_bookings > 0:
            raise HTTPException(
                409,
                "Cannot set space to unavailable while it has active bookings."
            )

    for key, value in data.items():
        setattr(db_space, key, value)

    db.commit()
    db.refresh(db_space)
    return db_space



def soft_delete_space(db: Session, db_space: Space) -> Space:
    # Check active bookings
    active_bookings = db.query(Booking).filter(
        Booking.space_id == db_space.id,
        Booking.status.in_(["pending", "confirmed", "checked_in"])
    ).count()

    if active_bookings > 0:
        raise HTTPException(
            409,
            "Cannot delete space with active bookings."
        )

    db_space.is_active = False
    db.commit()
    db.refresh(db_space)
    return db_space

