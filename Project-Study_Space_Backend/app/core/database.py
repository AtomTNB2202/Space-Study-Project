# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Kết nối tới Postgres docker của bạn
# user: admin, pass: admin123, db: studyspace
DATABASE_URL = "postgresql://admin:admin123@localhost:5432/studyspace"

# engine nói chuyện với Postgres
engine = create_engine(DATABASE_URL, future=True)

# SessionLocal = mỗi request 1 session DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = dùng để khai báo các model
Base = declarative_base()


# Dependency cho FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
