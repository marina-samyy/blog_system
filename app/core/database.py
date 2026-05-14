import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator

# ---------------- Load environment variables ----------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# ❗ Fail fast if missing config
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

# ---------------- Create engine ----------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False,
    future=True  # modern SQLAlchemy behavior
)

# ---------------- Session factory ----------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------- Base model ----------------
Base = declarative_base()

# ---------------- DB Dependency ----------------
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  