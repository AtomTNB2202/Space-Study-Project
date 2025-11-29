from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import penalty as crud_penalty
from app.schemas.penalty import PenaltyOut, PenaltyCreate, PenaltyUpdate
from app.models.user import User
from app.core import deps     # import đúng

router = APIRouter(prefix="/penalties", tags=["penalties"])


@router.post("/", response_model=PenaltyOut, status_code=status.HTTP_201_CREATED)
def create_penalty(
    data: PenaltyCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(deps.get_current_admin),
):
    """Admin tạo penalty cho một user."""
    return crud_penalty.create_penalty(db, data)


@router.get("/", response_model=List[PenaltyOut])
def list_penalties(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: User = Depends(deps.get_current_admin),
):
    """Admin xem toàn bộ penalties."""
    return crud_penalty.list_penalties(db, skip=skip, limit=limit)


@router.get("/me", response_model=List[PenaltyOut])
def list_my_penalties(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """User xem các penalty của chính mình."""
    return crud_penalty.list_user_penalties(db, user_id=current_user.id)


@router.patch("/{penalty_id}", response_model=PenaltyOut)
def update_penalty(
    penalty_id: int,
    data: PenaltyUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(deps.get_current_admin),
):
    penalty = crud_penalty.get_penalty(db, penalty_id)
    if not penalty:
        raise HTTPException(status_code=404, detail="Penalty not found")
    return crud_penalty.update_penalty(db, penalty, data)


@router.delete("/{penalty_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_penalty(
    penalty_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(deps.get_current_admin),
):
    penalty = crud_penalty.get_penalty(db, penalty_id)
    if not penalty:
        raise HTTPException(status_code=404, detail="Penalty not found")
    crud_penalty.delete_penalty(db, penalty)
    return
