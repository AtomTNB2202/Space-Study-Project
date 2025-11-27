# app/api/v1/ratings.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.rating import RatingResponse, RatingCreate, RatingUpdate
from app.crud import rating as crud_rating
from app.crud import reservation as crud_booking  # để kiểm tra user owns booking

router = APIRouter()


@router.get("/", response_model=list[RatingResponse])
def list_ratings(db: Session = Depends(get_db)):
    return crud_rating.list_ratings(db)


@router.post("/", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
def create_rating(
    data: RatingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # User chỉ được rate booking của họ
    booking = crud_booking.get_booking(db, data.booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")

    if booking.user_id != current_user.id:
        raise HTTPException(403, "Not allowed to rate this booking")

    # Override user_id để client không fake user khác
    data.user_id = current_user.id

    return crud_rating.create_rating(db, data)


@router.patch("/{rating_id}", response_model=RatingResponse)
def update_rating(
    rating_id: int,
    updates: RatingUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_obj = crud_rating.get_rating(db, rating_id)
    if not db_obj:
        raise HTTPException(404, "Rating not found")

    if db_obj.user_id != current_user.id:
        raise HTTPException(403, "Not allowed")

    return crud_rating.update_rating(db, db_obj, updates)


@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(
    rating_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_obj = crud_rating.get_rating(db, rating_id)
    if not db_obj:
        raise HTTPException(404, "Rating not found")

    if db_obj.user_id != current_user.id:
        raise HTTPException(403, "Not allowed")

    crud_rating.delete_rating(db, db_obj)
    return
