# app/crud/booking.py (đề xuất rename)
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from app.models.reservation import Reservation
from app.schemas.booking import BookingCreate, BookingUpdate


def get_booking(db: Session, booking_id: int):
    return db.get(Reservation, booking_id)


def get_bookings(
    db: Session,
    *,
    user_id: int | None = None,
    space_id: int | None = None,
    status: str | None = None,
):
    stmt = select(Reservation)

    if user_id is not None:
        stmt = stmt.where(Reservation.user_id == user_id)

    if space_id is not None:
        stmt = stmt.where(Reservation.space_id == space_id)

    if status is not None:
        stmt = stmt.where(Reservation.status == status)

    return db.execute(stmt).scalars().all()


def create_booking(db: Session, data: BookingCreate):
    booking = Reservation(
        user_id=data.user_id,
        space_id=data.space_id,
        start_time=data.start_time,
        end_time=data.end_time,
        status=data.status.value
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def update_booking(db: Session, booking: Reservation, updates: BookingUpdate):
    data = updates.model_dump(exclude_unset=True)

    for key, value in data.items():
        if hasattr(value, "value"):
            value = value.value  # Enum → string
        setattr(booking, key, value)

    db.commit()
    db.refresh(booking)
    return booking


def delete_booking(db: Session, booking: Reservation):
    db.delete(booking)
    db.commit()


# ====== NEW: Check-in ======

def check_in(db: Session, booking: Reservation):
    booking.status = "checked_in"
    booking.check_in_time = datetime.utcnow()

    db.commit()
    db.refresh(booking)
    return booking


# ====== NEW: Check-out ======

def check_out(db: Session, booking: Reservation):
    booking.status = "completed"
    booking.check_out_time = datetime.utcnow()

    db.commit()
    db.refresh(booking)
    return booking
