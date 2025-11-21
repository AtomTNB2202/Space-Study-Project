# Backend Development Guide

## 📋 Task Checklist

### Backend

- [ ] **Database Design**
  - Design PostgreSQL database structure (models)
  - Define relationships and constraints
  - Plan indexing strategy with PostgreSQL indexes
  
- [ ] **API Design**
  - Design CRUD endpoints
  - Define input/output schemas (OpenAPI)
  - Map endpoints based on user flows
  
- [ ] **Infrastructure Setup**
  - Configure Docker environment (PostgreSQL + Redis)
  - Set up database migrations with Alembic
  - Implement caching strategy with Redis
  - Configure JWT authentication

---

## 🚀 Quick Start Guide

### 0️⃣ Install UV

First, install `uv` - a fast Python package installer and resolver:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative (using pip):**
```bash
pip install uv
```

**Verify installation:**
```bash
uv --version
```

### 1️⃣ Initial Setup

```bash
# Create project structure
mkdir -p backend/{app/{api/v1,core,crud,models,schemas,utils},alembic,tests}
cd backend

# Create virtual environment using uv
uv venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate    # Windows

# Create requirements.txt
cat > requirements.txt << EOF
fastapi
uvicorn[standard]
sqlalchemy
alembic
pydantic
pydantic-settings
psycopg2-binary
asyncpg
python-jose[cryptography]
passlib[bcrypt]
python-multipart
redis
python-dotenv
pytest
pytest-asyncio
httpx
EOF

# Install dependencies using uv (much faster than pip!)
uv pip install -r requirements.txt

# Or install packages one by one
# uv pip install fastapi uvicorn[standard] sqlalchemy alembic pydantic pydantic-settings psycopg2-binary
```

> 💡 **Why UV?**
> - ⚡ **10-100x faster** than pip
> - 🔒 Better dependency resolution
> - 📦 Compatible with pip and existing tools
> - 🎯 Drop-in replacement for pip

### 2️⃣ Environment Configuration

Create `.env` file:

```bash
# .env
# Database (PostgreSQL)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changeme123
POSTGRES_DB=app_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:changeme123@localhost:5432/app_db

# Test Database
TEST_DATABASE_URL=postgresql://postgres:changeme123@localhost:5432/app_test_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
PROJECT_NAME=MyApp
VERSION=1.0.0
ENVIRONMENT=development
DEBUG=True
API_V1_PREFIX=/api/v1

# Database Connection Pool
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

> 💡 **Generate a secure SECRET_KEY:**
> ```bash
> openssl rand -hex 32
> ```

---

## 🐳 Database Setup with Docker

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: app_postgres
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme123}
      POSTGRES_DB: ${POSTGRES_DB:-app_db}
      POSTGRES_INITDB_ARGS: "-E UTF8 --locale=en_US.UTF-8"
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d  # Optional init scripts
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-app_db}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app_network
    restart: unless-stopped

  postgres_test:
    image: postgres:15-alpine
    container_name: app_postgres_test
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme123}
      POSTGRES_DB: app_test_db
    ports:
      - "5433:5432"
    volumes:
      - postgres_test_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres} -d app_test_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app_network
    restart: unless-stopped

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: app_pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
      PGADMIN_CONFIG_SERVER_MODE: 'False'
    ports:
      - "5050:80"
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    depends_on:
      - postgres
    networks:
      - app_network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: app_redis
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD:-}
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app_network
    restart: unless-stopped

networks:
  app_network:
    driver: bridge

volumes:
  postgres_data:
  postgres_test_data:
  pgadmin_data:
  redis_data:
```

### Optional: PostgreSQL Initialization Script

Create `init-scripts/01-init.sql`:

```sql
-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search
CREATE EXTENSION IF NOT EXISTS "btree_gin"; -- For indexing

-- Create test database
CREATE DATABASE app_test_db;

-- Grant privileges (if needed)
-- GRANT ALL PRIVILEGES ON DATABASE app_db TO postgres;
-- GRANT ALL PRIVILEGES ON DATABASE app_test_db TO postgres;
```

**Start services:**
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f postgres

# Stop services
docker-compose down

# Stop and remove volumes (⚠️ DELETES ALL DATA)
docker-compose down -v
```

**Access pgAdmin:**
- URL: http://localhost:5050
- Email: admin@admin.com
- Password: admin
- Add server:
  - Host: postgres (container name)
  - Port: 5432
  - Username: postgres
  - Password: changeme123

---

## 🔧 Core Configuration Files

### 1. `app/core/config.py` - Settings Management

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import secrets

class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "MyApp"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # PostgreSQL Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    DATABASE_URL: str
    
    # Test Database
    TEST_DATABASE_URL: Optional[str] = None
    
    # Database Connection Pool
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600  # Recycle connections after 1 hour
    DB_ECHO: bool = False  # Set to True to log all SQL queries
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )
    
    @property
    def sync_database_url(self) -> str:
        """PostgreSQL sync connection string"""
        return self.DATABASE_URL.replace("postgresql://", "postgresql://")
    
    @property
    def async_database_url(self) -> str:
        """PostgreSQL async connection string"""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

settings = Settings()
```

### 2. `app/core/database.py` - PostgreSQL Connection

```python
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create PostgreSQL engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    # Connection Pool Settings
    poolclass=QueuePool,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=True,  # Verify connections before using
    
    # Echo SQL queries in debug mode
    echo=settings.DB_ECHO,
    
    # PostgreSQL specific settings
    connect_args={
        "connect_timeout": 10,
        "options": "-c timezone=utc",
    },
)

# Event listeners for connection pool monitoring (optional)
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Log new database connections"""
    logger.debug("New database connection established")

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    """Log connection checkouts from pool"""
    logger.debug("Connection checked out from pool")

# Create SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """
    Database session dependency.
    Yields a SQLAlchemy session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        db.close()


# Health check function
def check_db_connection() -> bool:
    """
    Check if database connection is healthy.
    Returns True if connection is successful, False otherwise.
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


# Get connection pool status (for monitoring)
def get_pool_status() -> dict:
    """
    Get current connection pool status.
    Useful for monitoring and debugging.
    """
    pool = engine.pool
    return {
        "pool_size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "total": pool.size() + pool.overflow(),
    }
```

### 3. `app/core/security.py` - JWT & Password Handling

```python
from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token.
    
    Args:
        subject: User ID or identifier to encode in token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access"
    }
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT refresh token.
    
    Args:
        subject: User ID or identifier to encode in token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT refresh token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh"
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    """
    Verify and decode JWT token.
    
    Args:
        token: JWT token to verify
        token_type: Expected token type (access or refresh)
        
    Returns:
        Subject (user ID) if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        if payload.get("type") != token_type:
            return None
            
        return payload.get("sub")
    except JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password to compare against
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)
```

### 4. `app/api/deps.py` - Authentication Dependencies

```python
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import TokenPayload

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login"
)

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency to get current authenticated user.
    Raises HTTPException if token is invalid or user not found.
    
    Usage:
        @router.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"user": current_user.email}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if token_data.sub is None:
            raise credentials_exception
            
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = db.query(User).filter(User.id == token_data.sub).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to ensure current user is a superuser.
    Raises HTTPException if user is not a superuser.
    
    Usage:
        @router.get("/admin")
        def admin_route(current_user: User = Depends(get_current_active_superuser)):
            return {"message": "Admin access granted"}
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_user_optional(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme)
) -> Optional[User]:
    """
    Get current user but don't raise error if not authenticated.
    Returns None if no valid token is provided.
    
    Usage:
        @router.get("/optional")
        def optional_route(current_user: Optional[User] = Depends(get_current_user_optional)):
            if current_user:
                return {"message": f"Hello {current_user.email}"}
            return {"message": "Hello guest"}
    """
    if not token:
        return None
    
    try:
        return get_current_user(db, token)
    except HTTPException:
        return None
```

---

## 📦 Models & Schemas

### `app/models/base.py` - Base Model with PostgreSQL Features

```python
from sqlalchemy import Column, Integer, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class BaseModel(Base):
    """
    Base model with common fields and PostgreSQL-specific features.
    All models should inherit from this class.
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # UUID field (optional alternative to integer ID)
    # uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)
    
    # Timestamps with timezone support
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        index=True
    )
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now(),
        nullable=True
    )
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
```

### `app/models/user.py` - User Model with PostgreSQL Features

```python
from sqlalchemy import Column, String, Boolean, Index, Text
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    # Basic fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    
    # Status fields
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # PostgreSQL specific fields (optional)
    # preferences = Column(JSONB, nullable=True, default={})
    # roles = Column(ARRAY(String), nullable=True, default=[])
    # bio = Column(Text, nullable=True)
    
    # Composite indexes for better query performance
    __table_args__ = (
        Index('ix_users_email_active', 'email', 'is_active'),
        Index('ix_users_username_active', 'username', 'is_active'),
        # Full-text search index (requires pg_trgm extension)
        # Index('ix_users_username_trgm', 'username', postgresql_using='gin', postgresql_ops={'username': 'gin_trgm_ops'}),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
```

### `app/models/__init__.py`

```python
from app.models.user import User
from app.models.base import BaseModel

__all__ = ["User", "BaseModel"]
```

### `app/schemas/auth.py` - Auth Schemas

```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    """Response model for login endpoint"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int  # seconds

class TokenPayload(BaseModel):
    """Token payload data"""
    sub: int | None = None
    type: str = "access"  # access or refresh

class LoginRequest(BaseModel):
    """Login request body"""
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str
```

### `app/schemas/user.py` - User Schemas

```python
from pydantic import BaseModel, EmailStr, Field, ConfigDict, validator
from datetime import datetime
from typing import Optional
import re

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username must contain only letters, numbers, hyphens, and underscores')
        return v

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def password_strength(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v

# Properties to receive via API on update
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if v and not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username must contain only letters, numbers, hyphens, and underscores')
        return v

# Properties to return via API
class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_verified: bool
    
    model_config = ConfigDict(from_attributes=True)

# Properties stored in DB
class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_verified: bool
    
    model_config = ConfigDict(from_attributes=True)

# List response with pagination
class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    size: int
    pages: int
```

---

## 🔨 CRUD Operations

### `app/crud/base.py` - Generic CRUD Base Class

```python
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD operations base class.
    
    Args:
        model: SQLAlchemy model class
    """
    
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get a single record by ID"""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def get_count(self, db: Session) -> int:
        """Get total count of records"""
        return db.query(self.model).count()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record"""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing record"""
        obj_data = jsonable_encoder(db_obj)
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """Delete a record"""
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
```

### `app/crud/crud_user.py` - User CRUD with PostgreSQL Optimizations

```python
from typing import Optional, List
from sqlalchemy import or_, func
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD operations for User model"""
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Get user by email (case-insensitive using PostgreSQL)"""
        return db.query(User).filter(
            func.lower(User.email) == func.lower(email)
        ).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """Get user by username (case-insensitive using PostgreSQL)"""
        return db.query(User).filter(
            func.lower(User.username) == func.lower(username)
        ).first()
    
    def search_users(
        self, 
        db: Session, 
        *, 
        query: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """
        Search users by email or username using PostgreSQL ILIKE.
        For better performance, consider using pg_trgm extension.
        """
        search_pattern = f"%{query}%"
        return db.query(User).filter(
            or_(
                User.email.ilike(search_pattern),
                User.username.ilike(search_pattern),
                User.full_name.ilike(search_pattern)
            )
        ).offset(skip).limit(limit).all()

    def get_active_users(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """Get only active users"""
        return db.query(User).filter(
            User.is_active == True
        ).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create new user with hashed password"""
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, 
        db: Session, 
        *, 
        db_obj: User, 
        obj_in: UserUpdate
    ) -> User:
        """Update user (hashes password if provided)"""
        update_data = obj_in.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, 
        db: Session, 
        *, 
        email: str, 
        password: str
    ) -> Optional[User]:
        """Authenticate user by email and password"""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        """Check if user is active"""
        return user.is_active
    
    def is_superuser(self, user: User) -> bool:
        """Check if user is superuser"""
        return user.is_superuser

# Create instance
user_crud = CRUDUser(User)
```

---

## 🛣️ API Routes

### `app/api/v1/auth.py` - Authentication Endpoints

```python
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.crud.crud_user import user_crud
from app.schemas.auth import Token, LoginRequest, RefreshTokenRequest
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register new user.
    
    - **email**: Valid email address (unique)
    - **username**: Alphanumeric username (unique, 3-50 chars)
    - **password**: Strong password (min 8 chars, uppercase, lowercase, digit)
    - **full_name**: Optional full name
    """
    # Check if user exists
    if user_crud.get_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    if user_crud.get_by_username(db, username=user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    user = user_crud.create(db, obj_in=user_in)
    return user

@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login to get access token and refresh token.
    
    Returns JWT tokens for authentication.
    """
    user = user_crud.authenticate(
        db, 
        email=login_data.email, 
        password=login_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, 
        expires_delta=access_token_expires
    )
    
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        subject=user.id,
        expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Get new access token using refresh token.
    """
    user_id = verify_token(refresh_data.refresh_token, token_type="refresh")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user = user_crud.get(db, id=int(user_id))
    if not user or not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id,
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

# OAuth2 compatible endpoint (for Swagger UI)
@router.post("/token", response_model=Token)
def login_oauth2(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login (for Swagger UI authentication).
    Use email as username.
    """
    user = user_crud.authenticate(
        db, 
        email=form_data.username,  # OAuth2 uses 'username' field
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
```

### `app/api/v1/users.py` - User Endpoints

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.config import settings
from app.core.database import get_db
from app.api.deps import get_current_user, get_current_active_superuser
from app.crud.crud_user import user_crud
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserListResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user profile.
    """
    return current_user

@router.patch("/me", response_model=UserResponse)
def update_user_me(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update current user profile.
    """
    # Check if email is being changed and already exists
    if user_in.email and user_in.email != current_user.email:
        existing_user = user_crud.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Check if username is being changed and already exists
    if user_in.username and user_in.username != current_user.username:
        existing_user = user_crud.get_by_username(db, username=user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    return user_crud.update(db, db_obj=current_user, obj_in=user_in)

@router.get("/search", response_model=list[UserResponse])
def search_users(
    q: str = Query(..., min_length=2, description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search users by email, username, or full name.
    Uses PostgreSQL ILIKE for case-insensitive search.
    """
    users = user_crud.search_users(db, query=q, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user by ID.
    Requires authentication.
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return user

@router.get("/", response_model=UserListResponse)
def read_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Get list of users with pagination.
    Requires superuser privileges.
    """
    users = user_crud.get_multi(db, skip=skip, limit=limit)
    total = user_crud.get_count(db)
    
    return {
        "items": users,
        "total": total,
        "page": skip // limit + 1,
        "size": limit,
        "pages": (total + limit - 1) // limit
    }

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Delete user.
    Requires superuser privileges.
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    # Prevent deleting yourself
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself"
        )
    
    user_crud.remove(db, id=user_id)
```

### `app/api/v1/health.py` - Health Check Endpoints

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db, check_db_connection, get_pool_status
from app.core.config import settings
import redis

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

@router.get("/db")
def database_health(db: Session = Depends(get_db)):
    """
    Database health check.
    Returns database connection status and pool information.
    """
    try:
        # Execute simple query
        db.execute("SELECT 1")
        
        pool_status = get_pool_status()
        
        return {
            "status": "healthy",
            "database": "postgresql",
            "connection": "active",
            "pool": pool_status
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "postgresql",
            "connection": "failed",
            "error": str(e)
        }

@router.get("/redis")
def redis_health():
    """Redis health check"""
    try:
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        info = r.info()
        
        return {
            "status": "healthy",
            "cache": "redis",
            "version": info.get("redis_version"),
            "connected_clients": info.get("connected_clients"),
            "used_memory_human": info.get("used_memory_human")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "cache": "redis",
            "error": str(e)
        }

@router.get("/full")
def full_health_check(db: Session = Depends(get_db)):
    """
    Comprehensive health check of all services.
    """
    db_status = check_db_connection()
    
    try:
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        redis_status = True
    except:
        redis_status = False
    
    overall_status = "healthy" if (db_status and redis_status) else "degraded"
    
    return {
        "status": overall_status,
        "services": {
            "api": "healthy",
            "database": "healthy" if db_status else "unhealthy",
            "cache": "healthy" if redis_status else "unhealthy"
        },
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }
```

### `app/api/v1/__init__.py` - Combine Routers

```python
from fastapi import APIRouter
from app.api.v1 import auth, users, health

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(health.router)
```

---

## 🎯 Main Application

### `app/main.py` - FastAPI Application

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import engine, Base, check_db_connection
from app.api.v1 import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for FastAPI application.
    Handles startup and shutdown tasks.
    """
    # Startup
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} API v{settings.VERSION}")
    logger.info(f"🔧 Environment: {settings.ENVIRONMENT}")
    logger.info(f"📚 Documentation: http://localhost:8000/docs")
    
    # Create database tables (for development only)
    if settings.ENVIRONMENT == "development":
        logger.info("📦 Creating database tables...")
        Base.metadata.create_all(bind=engine)
    
    # Check database connection
    if check_db_connection():
        logger.info("✅ Database connection successful")
    else:
        logger.error("❌ Database connection failed")
    
    yield
    
    # Shutdown
    logger.info(f"👋 Shutting down {settings.PROJECT_NAME} API")
    engine.dispose()

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="FastAPI Backend with PostgreSQL",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Root endpoint
@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": f"{settings.API_V1_PREFIX}/health"
    }
```

---

## 🗃️ Database Migrations with Alembic

### Initialize Alembic

```bash
# Initialize Alembic
alembic init alembic
```

### Configure `alembic.ini`

```ini
[alembic]
# Path to migration scripts
script_location = alembic

# Template used to generate migration files
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# Prepend sys.path
prepend_sys_path = .

# PostgreSQL connection string (will be overridden in env.py)
# sqlalchemy.url = postgresql://postgres:changeme123@localhost:5432/app_db

# Timezone
timezone = UTC

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

### Update `alembic/env.py`

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import settings and models
from app.core.config import settings
from app.core.database import Base
from app.models import *  # Import all models

# Alembic Config object
config = context.config

# Set PostgreSQL connection string from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    This configures the context with just a URL and not an Engine.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Compare column types
        compare_server_default=True,  # Compare server defaults
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    In this scenario we need to create an Engine and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Compare column types
            compare_server_default=True,  # Compare server defaults
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Migration Commands

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration - create users table"

# Apply migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1

# Rollback to base (empty database)
alembic downgrade base

# View current version
alembic current

# View migration history
alembic history --verbose

# View SQL without executing
alembic upgrade head --sql

# Create empty migration (for data migrations)
alembic revision -m "Add default admin user"

# Specific revision
alembic upgrade +1
alembic upgrade abc123
```

---

## 🧪 Testing with PostgreSQL

### `tests/conftest.py` - Test Configuration

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings

# Use test database (PostgreSQL)
TEST_DATABASE_URL = settings.TEST_DATABASE_URL or "postgresql://postgres:changeme123@localhost:5433/app_test_db"

# Create test engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    """Create database engine for tests"""
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db(db_engine):
    """Create database session for each test"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    """Create test client with overridden database"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture
def test_user_data():
    """Sample user data for tests"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "Test@123",
        "full_name": "Test User"
    }


@pytest.fixture
def test_admin_data():
    """Sample admin user data for tests"""
    return {
        "email": "admin@example.com",
        "username": "admin",
        "password": "Admin@123",
        "full_name": "Admin User",
        "is_superuser": True
    }
```

### `tests/test_auth.py`

```python
import pytest
from fastapi import status

def test_register_user(client, test_user_data):
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json=test_user_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client, test_user_data):
    """Test registration with duplicate email"""
    # Register first user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Try to register with same email
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email already registered" in response.json()["detail"].lower()


def test_login(client, test_user_data):
    """Test user login"""
    # Register user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, test_user_data):
    """Test login with invalid credentials"""
    # Register user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Try login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user_data["email"],
            "password": "WrongPassword123"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_token(client, test_user_data):
    """Test token refresh"""
    # Register and login
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Refresh token
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run and show print statements
pytest -s
```

---

## 🚀 PostgreSQL Performance Optimization

### 1. Add `app/core/cache.py` - Redis Caching

```python
import redis
import json
from typing import Optional, Any
from functools import wraps
from app.core.config import settings

# Redis client
redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    encoding="utf-8"
)


def get_cache(key: str) -> Optional[Any]:
    """Get value from Redis cache"""
    try:
        value = redis_client.get(key)
        return json.loads(value) if value else None
    except Exception as e:
        print(f"Cache get error: {e}")
        return None


def set_cache(key: str, value: Any, expire: int = 300) -> bool:
    """Set value in Redis cache with expiration (default 5 minutes)"""
    try:
        redis_client.setex(
            key,
            expire,
            json.dumps(value, default=str)
        )
        return True
    except Exception as e:
        print(f"Cache set error: {e}")
        return False


def delete_cache(key: str) -> bool:
    """Delete value from Redis cache"""
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        print(f"Cache delete error: {e}")
        return False


def clear_cache_pattern(pattern: str) -> bool:
    """Delete all keys matching pattern"""
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
        return True
    except Exception as e:
        print(f"Cache clear error: {e}")
        return False


def cached(expire: int = 300, key_prefix: str = ""):
    """
    Decorator to cache function results.
    
    Usage:
        @cached(expire=600, key_prefix="user")
        def get_user(user_id: int):
            return user_crud.get(db, id=user_id)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{args}:{kwargs}"
            
            # Try to get from cache
            cached_value = get_cache(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            set_cache(cache_key, result, expire)
            
            return result
        return wrapper
    return decorator
```

### 2. PostgreSQL Indexes

Add to your models:

```python
from sqlalchemy import Index

class User(BaseModel):
    # ... existing fields ...
    
    __table_args__ = (
        # B-tree indexes (default, good for equality and range queries)
        Index('ix_users_email_active', 'email', 'is_active'),
        Index('ix_users_created_at_desc', 'created_at', postgresql_using='btree', postgresql_order_by='DESC'),
        
        # GIN index for full-text search (requires pg_trgm extension)
        Index('ix_users_username_gin', 'username', postgresql_using='gin', postgresql_ops={'username': 'gin_trgm_ops'}),
        Index('ix_users_fullname_gin', 'full_name', postgresql_using='gin', postgresql_ops={'full_name': 'gin_trgm_ops'}),
        
        # Partial index (only index active users)
        Index('ix_users_active_only', 'email', postgresql_where=sa.text('is_active = true')),
    )
```

---

## 🐳 Production Deployment

### `Dockerfile`

```dockerfile
FROM python:3.11-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install PostgreSQL client
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini .
COPY .env .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Start command
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

---

## 🎯 Development Workflow Summary

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Start PostgreSQL and Redis
docker-compose up -d postgres redis

# 3. Create and activate virtual environment using uv
uv venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate    # Windows

# 4. Install dependencies using uv (fast!)
uv pip install -r requirements.txt

# 5. Run migrations
alembic upgrade head

# 6. Start development server
uvicorn app.main:app --reload --port 8000

# 7. Access API documentation
open http://localhost:8000/docs

# 8. Access pgAdmin
open http://localhost:5050

# 9. Make changes and create migration
alembic revision --autogenerate -m "Add new feature"
alembic upgrade head

# 10. Run tests
pytest --cov=app

# 11. Add new packages using uv
uv pip install package-name

# 12. Update requirements.txt
uv pip freeze > requirements.txt

# 13. Check database status
docker-compose exec postgres psql -U postgres -d app_db -c "\dt"
```

---

## 📦 UV Command Reference

### Package Management

```bash
# Install packages
uv pip install package-name
uv pip install -r requirements.txt
uv pip install -e .  # Editable install

# Uninstall packages
uv pip uninstall package-name

# List installed packages
uv pip list

# Show package info
uv pip show package-name

# Freeze requirements
uv pip freeze > requirements.txt

# Install with extras
uv pip install "fastapi[all]"
uv pip install "uvicorn[standard]"

# Upgrade packages
uv pip install --upgrade package-name
uv pip install --upgrade -r requirements.txt

# Install from git
uv pip install git+https://github.com/user/repo.git

# Install specific version
uv pip install "package-name>=1.0.0,<2.0.0"
```

### Virtual Environments

```bash
# Create virtual environment
uv venv

# Create with specific Python version
uv venv --python 3.11

# Create with custom name
uv venv myenv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Deactivate
deactivate
```

### Performance Comparison

```bash
# UV is significantly faster than pip:
# pip install -r requirements.txt    → ~45 seconds
# uv pip install -r requirements.txt → ~2-5 seconds
```

---

## 🛠️ PostgreSQL Management Commands

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d app_db

# Inside psql:
\dt                    # List tables
\d users              # Describe users table
\di                   # List indexes
\dx                   # List extensions
\l                    # List databases
\du                   # List users
\q                    # Quit

# Backup database
docker-compose exec postgres pg_dump -U postgres app_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U postgres app_db < backup.sql

# Create database backup with Docker
docker-compose exec postgres pg_dump -U postgres -F c app_db > backup.dump

# Restore from backup
docker-compose exec -T postgres pg_restore -U postgres -d app_db < backup.dump

# View active connections
docker-compose exec postgres psql -U postgres -c "SELECT * FROM pg_stat_activity;"

# Kill connections to database
docker-compose exec postgres psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='app_db' AND pid <> pg_backend_pid();"
```

---

## 📖 Additional Resources

- [UV Documentation](https://github.com/astral-sh/uv)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [PostgreSQL Performance Tips](https://wiki.postgresql.org/wiki/Performance_Optimization)
