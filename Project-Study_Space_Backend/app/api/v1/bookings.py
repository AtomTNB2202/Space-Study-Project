# app/api/v1/bookings.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import reservation as crud_reservation
from app.schemas.booking import (
    BookingResponse,
    BookingCreate,
    BookingUpdate
)

router = APIRouter()


# GET /bookings (filter by userId, spaceId, status)
@router.get("/", response_model=List[BookingResponse])
def list_bookings(
    userId: Optional[int] = None,
    spaceId: Optional[int] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud_reservation.get_bookings(
        db,
        user_id=userId,
        space_id=spaceId,
        status=status_filter
    )


# GET /bookings/{bookingId}
@router.get("/{bookingId}", response_model=BookingResponse)
def get_booking(bookingId: int, db: Session = Depends(get_db)):
    booking = crud_reservation.get_booking(db, bookingId)
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking


# POST /bookings
@router.post("/", response_model=BookingResponse, status_code=201)
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):
    return crud_reservation.create_booking(db, data)


# PATCH /bookings/{bookingId}
@router.patch("/{bookingId}", response_model=BookingResponse)
def update_booking(
    bookingId: int,
    data: BookingUpdate,
    db: Session = Depends(get_db)
):
    booking = crud_reservation.get_booking(db, bookingId)
    if not booking:
        raise HTTPException(404, "Booking not found")
    return crud_reservation.update_booking(db, booking, data)


# DELETE /bookings/{bookingId}
@router.delete("/{bookingId}", status_code=204)
def delete_booking(bookingId: int, db: Session = Depends(get_db)):
    booking = crud_reservation.get_booking(db, bookingId)
    if not booking:
        raise HTTPException(404, "Booking not found")
    crud_reservation.delete_booking(db, booking)
    return


# POST /bookings/{bookingId}/check-in
@router.post("/{bookingId}/check-in", response_model=BookingResponse)
def check_in(bookingId: int, db: Session = Depends(get_db)):
    booking = crud_reservation.get_booking(db, bookingId)
    if not booking:
        raise HTTPException(404, "Booking not found")

    return crud_reservation.check_in(db, booking)


# POST /bookings/{bookingId}/check-out
@router.post("/{bookingId}/check-out", response_model=BookingResponse)
def check_out(bookingId: int, db: Session = Depends(get_db)):
    booking = crud_reservation.get_booking(db, bookingId)
    if not booking:
        raise HTTPException(404, "Booking not found")

    return crud_reservation.check_out(db, booking)
