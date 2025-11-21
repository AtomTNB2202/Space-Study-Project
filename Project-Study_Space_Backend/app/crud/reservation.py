# app/crud/reservation.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate


def get_reservation(db: Session, reservation_id: int) -> Optional[Reservation]:
    return db.get(Reservation, reservation_id)


def get_reservations(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    space_id: Optional[int] = None,
) -> List[Reservation]:
    stmt = select(Reservation)

    if user_id is not None:
        stmt = stmt.where(Reservation.user_id == user_id)
    if space_id is not None:
        stmt = stmt.where(Reservation.space_id == space_id)

    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def create_reservation(db: Session, res_in: ReservationCreate) -> Reservation:
    db_res = Reservation(
        user_id=res_in.user_id,
        space_id=res_in.space_id,
        start_time=res_in.start_time,
        end_time=res_in.end_time,
        status=res_in.status.value,
    )
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return db_res


def update_reservation(
    db: Session,
    db_res: Reservation,
    res_in: ReservationUpdate,
) -> Reservation:
    data = res_in.model_dump(exclude_unset=True)

    for field, value in data.items():
        if hasattr(value, "value"):  # enum -> string
            value = value.value
        setattr(db_res, field, value)

    db.commit()
    db.refresh(db_res)
    return db_res


def delete_reservation(db: Session, db_res: Reservation) -> None:
    db.delete(db_res)
    db.commit()
