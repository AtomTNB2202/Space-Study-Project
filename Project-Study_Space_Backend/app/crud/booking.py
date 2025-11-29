# app/crud/booking.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from fastapi import HTTPException, status

from app.models.space import Space
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate


def get_booking(db: Session, booking_id: int):
    return db.get(Booking, booking_id)


def get_bookings(db: Session, *, user_id=None, space_id=None, status=None):
    stmt = select(Booking)

    if user_id is not None:
        stmt = stmt.where(Booking.user_id == user_id)

    if space_id is not None:
        stmt = stmt.where(Booking.space_id == space_id)

    if status is not None:
        stmt = stmt.where(Booking.status == status)

    return db.execute(stmt).scalars().all()


def create_booking(db: Session, data: BookingCreate, current_user_id: int):

    # time check
    if data.start_time >= data.end_time:
        raise HTTPException(400, "Invalid time range.")

    # space check
    space = db.query(Space).filter(Space.id == data.space_id).first()
    if not space:
        raise HTTPException(404, "Space not found.")

    if not space.is_active or space.status != "available":
        raise HTTPException(409, "Space is not available.")
    
    user_overlap = db.query(Booking).filter(
        Booking.user_id == current_user_id,
        Booking.space_id == data.space_id,
        Booking.status.in_(["pending", "confirmed"]),
        Booking.start_time < data.end_time,
        Booking.end_time > data.start_time,
    ).count()

    if user_overlap >= 1:
        raise HTTPException(409, "You already have a booking in this time range.")

    # overlap
    active_bookings = db.query(Booking).filter(
        Booking.space_id == data.space_id,
        Booking.status.in_(["pending", "confirmed"]),
        Booking.start_time < data.end_time,
        Booking.end_time > data.start_time,
    ).count()

    if active_bookings >= space.capacity:
        raise HTTPException(409, "Space is fully booked in this time range.")

    booking = Booking(
        user_id=current_user_id,
        space_id=data.space_id,
        start_time=data.start_time,
        end_time=data.end_time,
        status="pending",
        qr_code_data=data.qr_code_data,
        notes=data.notes,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def update_booking(db, booking: Booking, updates: BookingUpdate):

    data = updates.model_dump(exclude_unset=True)

    if booking.status in ["checked_in", "completed", "cancelled", "no_show"]:
        raise HTTPException(400, "Cannot modify a finished or cancelled booking.")

    if "status" in data:
        raise HTTPException(400, "Status cannot be updated manually.")
    
    if "space_id" in data:
        raise HTTPException(400, "Cannot change space for an existing booking.")
    
    if "start_time" in data or "end_time" in data:
        new_start = data.get("start_time", booking.start_time)
        new_end = data.get("end_time", booking.end_time)

        if new_start >= new_end:
            raise HTTPException(400, "Invalid time range.")
    
        overlap = db.query(Booking).filter(
            Booking.id != booking.id,
            Booking.space_id == booking.space_id,
            Booking.status.in_(["pending", "confirmed"]),
            Booking.start_time < new_end,
            Booking.end_time > new_start,
        ).count()

        if overlap >= 1:
            raise HTTPException(409, "This time range is already booked.")
    
    for k, v in data.items():
        if hasattr(v, "value"):
            v = v.value
        setattr(booking, k, v)

    db.commit()
    db.refresh(booking)
    return booking



def delete_booking(db, booking: Booking):
    db.delete(booking)
    db.commit()


def check_in(db, booking: Booking):

    if booking.status != "pending":
        raise HTTPException(400, "Booking cannot be checked in now.")

    booking.status = "checked_in"
    booking.check_in_time = datetime.utcnow()
    db.commit()
    db.refresh(booking)
    return booking


def check_out(db, booking: Booking):

    if booking.status != "checked_in":
        raise HTTPException(400, "Booking must be checked in before checking out.")

    booking.status = "completed"
    booking.check_out_time = datetime.utcnow()
    db.commit()
    db.refresh(booking)
    return booking




