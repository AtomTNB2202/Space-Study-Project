# app/api/v1/spaces.py
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.schemas.space import SpaceResponse, SpaceCreate, SpaceUpdate
from app.crud import space as crud_space

router = APIRouter()


@router.get("/", response_model=List[SpaceResponse])
def list_spaces(
    search: Optional[str] = None,
    minCapacity: Optional[int] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud_space.get_spaces(
        db,
        search=search,
        min_capacity=minCapacity,
        status=status_filter,
    )


@router.get("/{space_id}", response_model=SpaceResponse)
def get_space(
    space_id: int,
    db: Session = Depends(get_db),
):
    db_space = crud_space.get_space(db, space_id)
    if not db_space or not db_space.is_active:
        raise HTTPException(404, "Space not found")
    return db_space


@router.post("/", response_model=SpaceResponse, status_code=201)
def create_new_space(
    space_in: SpaceCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin),
):
    return crud_space.create_space(db, space_in)


@router.patch("/{space_id}", response_model=SpaceResponse)
def update_existing_space(
    space_id: int,
    space_in: SpaceUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin),
):
    db_space = crud_space.get_space(db, space_id)
    if not db_space:
        raise HTTPException(404, "Space not found")
    return crud_space.update_space(db, db_space, space_in)


@router.delete("/{space_id}", response_model=SpaceResponse)
def delete_space(
    space_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin),
):
    db_space = crud_space.get_space(db, space_id)
    if not db_space:
        raise HTTPException(404, "Space not found")
    return crud_space.soft_delete_space(db, db_space)
