from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.crud import user as crud_user
from app.core.security import get_current_user, get_current_admin

router = APIRouter()


# 🔐 ADMIN: xem toàn bộ user
@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    return crud_user.get_users(db)


# 🛡 REGISTER: public nhưng check conflict đúng
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Email conflict
    if crud_user.get_user_by_email(db, user_in.email):
        raise HTTPException(409, "Email already registered")

    # Username conflict (giống CRUD)
    if db.query(crud_user.User).filter(
        crud_user.User.username == user_in.username
    ).first():
        raise HTTPException(409, "Username already taken")

    return crud_user.create_user(db, user_in)


# 👤 USER: lấy thông tin chính mình
@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user


# 🔐 ADMIN OR OWNER: xem user theo id
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    # Only admin or owner
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(403, "Not allowed to view other users")

    return user


# 🔐 ADMIN OR OWNER: update user
@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    # Only admin or owner
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(403, "Not allowed to update other users")

    return crud_user.update_user(db, user, data)

# 🔐 ADMIN ONLY: xoá user
@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    crud_user.delete_user(db, user)
