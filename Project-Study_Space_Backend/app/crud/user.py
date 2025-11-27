from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

from app.core.security import verify_password
from app.core.security import hash_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db: Session, user_id: int):
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str):
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def get_users(db: Session, skip=0, limit=100):
    stmt = select(User).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def create_user(db: Session, user_in: UserCreate):
    hashed = hash_password(user_in.password)

    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed,
        full_name=user_in.full_name,
        role=user_in.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, db_user: User, updates: UserUpdate):
    data = updates.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()



def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user