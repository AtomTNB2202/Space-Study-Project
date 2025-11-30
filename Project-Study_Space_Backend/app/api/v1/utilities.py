# app/api/v1/utilities.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.schemas.utility import UtilityResponse, UtilityCreate, UtilityUpdate
from app.crud import utility as crud_utility

router = APIRouter()


# -------------------------------------------------------
# GET /utilities  
# -------------------------------------------------------
@router.get("/", response_model=list[UtilityResponse])
def list_utilities(db: Session = Depends(get_db)):
    return crud_utility.list_utilities(db)


# -------------------------------------------------------
# POST /utilities   (admin only)
# -------------------------------------------------------
@router.post("/", response_model=UtilityResponse, status_code=201)
def create_utility(
    data: UtilityCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin),
):
    # Conflict: key đã tồn tại
    if crud_utility.get_utility_by_key(db, data.key):
        raise HTTPException(409, "Utility key already exists")

    return crud_utility.create_utility(db, data)


# -------------------------------------------------------
# PATCH /utilities/{id}   (admin only)
# -------------------------------------------------------
@router.patch("/{utility_id}", response_model=UtilityResponse)
def update_utility(
    utility_id: int,
    data: UtilityUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin),
):
    db_utility = crud_utility.get_utility(db, utility_id)
    if not db_utility:
        raise HTTPException(404, "Utility not found")

    # Check: không cho sửa key
    if data.key is not None:
        raise HTTPException(400, "Cannot modify key")

    return crud_utility.update_utility(db, db_utility, data)


# -------------------------------------------------------
# DELETE /utilities/{id}   (admin only)
# -------------------------------------------------------
@router.delete("/{utility_id}", status_code=204)
def delete_utility(
    utility_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin),
):
    db_utility = crud_utility.get_utility(db, utility_id)
    if not db_utility:
        raise HTTPException(404, "Utility not found")


    crud_utility.delete_utility(db, db_utility)
    return Response(status_code=204)

