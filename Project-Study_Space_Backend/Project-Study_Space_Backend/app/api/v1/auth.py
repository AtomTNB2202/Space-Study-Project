# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import (
    UserCreate,
    UserRole,
    UserResponse,
    UserUpdate,
)
from app.core.database import get_db
from app.core.security import create_access_token
from app.core.deps import get_current_user
from app.crud import user as crud_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


# -------------------------------
# POST /auth/register
# -------------------------------
@router.post("/register", response_model=UserResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if crud_user.get_user_by_email(db, data.email):
        raise HTTPException(400, "Email already registered")

    # Tạo UserCreate từ RegisterRequest, role mặc định = student
    user_in = UserCreate(
        email=data.email,
        username=data.username,
        full_name=data.full_name,
        password=data.password,
        role=UserRole.student,
    )

    created_user = crud_user.create_user(db, user_in)
    return created_user


# -------------------------------
# POST /auth/login
# -------------------------------
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # Ở đây Swagger truyền "username" → mình dùng nó như "email"
    user = crud_user.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)


# -------------------------------
# GET /auth/me
# -------------------------------
@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user


# -------------------------------
# PATCH /auth/me
# -------------------------------
@router.patch("/me", response_model=UserResponse)
def update_me(
    update: UserUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updated = crud_user.update_user(db, current_user, update)
    return updated
