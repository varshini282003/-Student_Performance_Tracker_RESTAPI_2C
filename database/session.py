import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Use Postgres later by setting DATABASE_URL in .env, else default to SQLite file
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:Svarshini%402003@localhost:5432/student_db")
# "postgresql://postgres:Svarshini%402003@localhost:5432/blogsdb"
# "sqlite:///./students.db"
# SQLite specific argument for multithreading issues
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith(
    "sqlite") else {}

# Create SQLAlchemy Engine
engine = create_engine(DATABASE_URL, echo=False,
                       future=True, connect_args=connect_args)

# Create SessionLocal class for session instances
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, future=True)

# Base class for ORM models
Base = declarative_base()

# Dependency function for FastAPI routes to get a DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
