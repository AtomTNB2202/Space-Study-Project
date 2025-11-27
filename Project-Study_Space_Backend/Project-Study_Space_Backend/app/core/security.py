# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

# GIỮ NGUYÊN SECRET_KEY NÀY GIỮA CÁC LẦN CHẠY
# (sau này bạn có thể chuyển sang đọc từ env)
SECRET_KEY = "very-secret-key-change-me-once-and-keep"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 giờ

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------------ PASSWORD ------------------------ #

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ------------------------ JWT TOKEN ------------------------ #

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Tạo JWT từ payload `data`.
    Mặc định hết hạn sau ACCESS_TOKEN_EXPIRE_MINUTES.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode JWT, nếu lỗi thì trả None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        # tạm thời in lỗi ra console để debug nếu cần
        print("JWT decode error:", e)
        return None
