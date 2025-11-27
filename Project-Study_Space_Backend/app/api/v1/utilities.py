# app/api/v1/utilities.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.schemas.utility import (
    UtilityResponse,
    UtilityCreate,
    UtilityUpdate,
)
from app.crud import utility as crud_utility

router = APIRouter()


# -------------------------------
# GET /utilities
# -------------------------------
@router.get("/", response_model=List[UtilityResponse])
def list_utilities(db: Session = Depends(get_db)):
    return crud_utility.list_utilities(db)


# -------------------------------
# POST /utilities  (admin)
# -------------------------------
@router.post(
    "/", response_model=UtilityResponse, status_code=status.HTTP_201_CREATED
)
def create_utility(
    data: UtilityCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    existing = crud_utility.get_utility_by_key(db, data.key)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utility key already exists",
        )
    return crud_utility.create_utility(db, data)


# -------------------------------
# PATCH /utilities/{utility_id} (admin)
# -------------------------------
@router.patch("/{utility_id}", response_model=UtilityResponse)
def update_utility(
    utility_id: int,
    data: UtilityUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    db_utility = crud_utility.get_utility(db, utility_id)
    if not db_utility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utility not found",
        )
    return crud_utility.update_utility(db, db_utility, data)


# -------------------------------
# DELETE /utilities/{utility_id} (admin)
# -------------------------------
@router.delete("/{utility_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_utility(
    utility_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    db_utility = crud_utility.get_utility(db, utility_id)
    if not db_utility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utility not found",
        )
    crud_utility.delete_utility(db, db_utility)
