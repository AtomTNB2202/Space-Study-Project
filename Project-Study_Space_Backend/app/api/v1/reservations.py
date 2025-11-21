# app/api/v1/reservations.py
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_db
from app.schemas.reservation import (
    ReservationResponse,
    ReservationCreate,
    ReservationUpdate,
)
from app.crud import reservation as crud_reservation

router = APIRouter()


@router.get("/", response_model=List[ReservationResponse])
def list_reservations(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    space_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return crud_reservation.get_reservations(
        db, skip=skip, limit=limit, user_id=user_id, space_id=space_id
    )


@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
):
    db_res = crud_reservation.get_reservation(db, reservation_id)
    if not db_res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found"
        )
    return db_res


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_new_reservation(
    res_in: ReservationCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud_reservation.create_reservation(db, res_in)
    except SQLAlchemyError as e:
        print("DB ERROR:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig) if hasattr(e, "orig") else str(e),
        )


@router.patch("/{reservation_id}", response_model=ReservationResponse)
def update_existing_reservation(
    reservation_id: int,
    res_in: ReservationUpdate,
    db: Session = Depends(get_db),
):
    db_res = crud_reservation.get_reservation(db, reservation_id)
    if not db_res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found"
        )
    return crud_reservation.update_reservation(db, db_res, res_in)


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
):
    db_res = crud_reservation.get_reservation(db, reservation_id)
    if not db_res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found"
        )
    crud_reservation.delete_reservation(db, db_res)
    return
