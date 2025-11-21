# app/api/v1/spaces.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.space import SpaceResponse, SpaceCreate, SpaceUpdate
from app.crud import space as crud_space

router = APIRouter()


@router.get("/", response_model=List[SpaceResponse])
def list_spaces(
    db: Session = Depends(get_db),
):
    return crud_space.get_spaces(db)


@router.get("/{space_id}", response_model=SpaceResponse)
def get_space(
    space_id: int,
    db: Session = Depends(get_db),
):
    db_space = crud_space.get_space(db, space_id)
    if not db_space or not db_space.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Space not found")
    return db_space


@router.post("/", response_model=SpaceResponse, status_code=status.HTTP_201_CREATED)
def create_new_space(
    space_in: SpaceCreate,
    db: Session = Depends(get_db),
):
    return crud_space.create_space(db, space_in)


@router.patch("/{space_id}", response_model=SpaceResponse)
def update_existing_space(
    space_id: int,
    space_in: SpaceUpdate,
    db: Session = Depends(get_db),
):
    db_space = crud_space.get_space(db, space_id)
    if not db_space:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Space not found")
    return crud_space.update_space(db, db_space, space_in)


@router.delete("/{space_id}", response_model=SpaceResponse)
def delete_space(
    space_id: int,
    db: Session = Depends(get_db),
):
    db_space = crud_space.get_space(db, space_id)
    if not db_space:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Space not found")
    return crud_space.soft_delete_space(db, db_space)
