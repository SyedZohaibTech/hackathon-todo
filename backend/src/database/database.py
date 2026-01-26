from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from ..models import Task, User, Conversation, Event, SQLModel  # Import all models here
import os

# Get database URL from environment, fallback to default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)