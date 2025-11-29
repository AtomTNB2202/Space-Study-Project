from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User

from app.crud import booking as crud_booking
from app.schemas.booking import BookingResponse, BookingCreate, BookingUpdate

router = APIRouter()

@router.get("/", response_model=List[BookingResponse])
def list_bookings(
    userId: Optional[int] = None,
    spaceId: Optional[int] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud_booking.get_bookings(
        db,
        user_id=userId,
        space_id=spaceId,
        status=status_filter
    )

@router.get("/{bookingId}", response_model=BookingResponse)
def get_booking(bookingId: int, db: Session = Depends(get_db)):
    booking = crud_booking.get_booking(db, bookingId)
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking

@router.post("/", response_model=BookingResponse, status_code=201)
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_booking.create_booking(db, data, current_user.id)

@router.patch("/{bookingId}", response_model=BookingResponse)
def update_booking(
    bookingId: int,
    data: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = crud_booking.get_booking(db, bookingId)
    if booking.user_id != current_user.id:
        raise HTTPException(403, "Not your booking")
    return crud_booking.update_booking(db, booking, data)

@router.delete("/{bookingId}", status_code=204)
def delete_booking(
    bookingId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = crud_booking.get_booking(db, bookingId)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.user_id != current_user.id:
        raise HTTPException(403, "Not your booking")
    crud_booking.delete_booking(db, booking)


@router.post("/{bookingId}/check-in", response_model=BookingResponse)
def check_in(
    bookingId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = crud_booking.get_booking(db, bookingId)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.user_id != current_user.id:
        raise HTTPException(403, "Not your booking")
    return crud_booking.check_in(db, booking)

@router.post("/{bookingId}/check-out", response_model=BookingResponse)
def check_out(
    bookingId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = crud_booking.get_booking(db, bookingId)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.user_id != current_user.id:
        raise HTTPException(403, "Not your booking")
    return crud_booking.check_out(db, booking)
