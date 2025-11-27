from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core import deps

from app.crud import user as crud_user
from app.crud import reservation as crud_reservation
from app.crud import penalty as crud_penalty

from app.models.user import User

from app.schemas.user import UserResponse
from app.schemas.booking import BookingResponse
from app.schemas.penalty import PenaltyOut
# ======================================================================

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(deps.get_current_admin),
):
    return crud_user.get_users(db)


@router.get("/reservations", response_model=List[BookingResponse])
def list_reservations(
    db: Session = Depends(get_db),
    current_admin: User = Depends(deps.get_current_admin),
):
    return crud_reservation.list_reservations(db)


@router.get("/penalties", response_model=List[PenaltyOut])
def list_all_penalties(
    db: Session = Depends(get_db),
    current_admin: User = Depends(deps.get_current_admin),
):
    return crud_penalty.list_penalties(db)
