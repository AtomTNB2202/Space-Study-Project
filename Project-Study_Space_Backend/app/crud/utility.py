# app/crud/utility.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.utility import Utility
from app.schemas.utility import UtilityCreate, UtilityUpdate
import re


def list_utilities(db: Session) -> List[Utility]:
    return db.query(Utility).order_by(Utility.id).all()

def get_utility(db: Session, utility_id: int) -> Optional[Utility]:
    return db.get(Utility, utility_id)

def get_utility_by_key(db: Session, key: str) -> Optional[Utility]:
    return db.query(Utility).filter(Utility.key == key).first()


def create_utility(db: Session, data: UtilityCreate) -> Utility:
    # KEY UNIQUE
    if get_utility_by_key(db, data.key):
        raise HTTPException(409, "Utility key already exists")

    # Check key format
    if not re.match(r"^[a-z0-9_]+$", data.key):
        raise HTTPException(400, "Key must be snake_case with no spaces")

    # Label required
    if not data.label:
        raise HTTPException(400, "Label is required")

    utility = Utility(
        key=data.key,
        label=data.label,
        description=data.description
    )

    db.add(utility)
    db.commit()
    db.refresh(utility)
    return utility


def update_utility(db: Session, db_utility: Utility, updates: UtilityUpdate) -> Utility:
    data = updates.model_dump(exclude_unset=True)

    # Không được sửa key
    if "key" in data:
        raise HTTPException(400, "Cannot modify utility key")

    for field, value in data.items():
        setattr(db_utility, field, value)

    db.commit()
    db.refresh(db_utility)
    return db_utility


def delete_utility(db: Session, db_utility: Utility) -> None:
    db.delete(db_utility)
    db.commit()
