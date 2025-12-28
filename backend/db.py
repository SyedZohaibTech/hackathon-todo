"""
Database connection utilities
References: Task T202, Spec §X
"""
from sqlmodel import create_engine, Session
from sqlalchemy import text
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    """
    Get database session
    """
    with Session(engine) as session:
        yield session