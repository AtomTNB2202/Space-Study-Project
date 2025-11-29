from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core import deps

from app.crud import user as crud_user
from app.crud import booking as crud_reservation
from app.crud import penalty as crud_penalty

from app.models.user import User

from app.schemas.user import UserResponse
from app.schemas.booking import BookingResponse
from app.schemas.penalty import PenaltyOut
from app.services.no_show import process_no_show_bookings
# ======================================================================

router = APIRouter(prefix="/admin", tags=["admin"])

# ================================
# USERS
# ================================
@router.get("/users", response_model=List[UserResponse])
def list_users(
    page: int = 1,
    limit: int = 20,
    role: str | None = None,
    active: bool | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(deps.get_current_admin),
):
    return crud_user.get_users_filtered(db, page, limit, role, active)

@router.patch("/users/{user_id}/ban", response_model=UserResponse)
def ban_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(deps.get_current_admin),
):
    return crud_user.set_active(db, user_id, False)

@router.patch("/users/{user_id}/unban", response_model=UserResponse)
def unban_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(deps.get_current_admin),
):
    return crud_user.set_active(db, user_id, True)

# ================================
# BOOKINGS (reservations)
# ================================
@router.get("/bookings", response_model=List[BookingResponse])
def list_bookings(
    db: Session = Depends(get_db),
    admin: User = Depends(deps.get_current_admin),
):
    return crud_reservation.list_reservations(db)

# ================================
# PENALTIES
# ================================
@router.get("/penalties", response_model=List[PenaltyOut])
def list_penalties(
    db: Session = Depends(get_db),
    admin: User = Depends(deps.get_current_admin),
):
    return crud_penalty.list_penalties(db)

@router.post("/run-no-show", summary="Force check no-show bookings")
def run_no_show(
    db: Session = Depends(get_db),
    admin: User = Depends(deps.get_current_admin),
):
    count = process_no_show_bookings(db)
    return {"processed": count}
