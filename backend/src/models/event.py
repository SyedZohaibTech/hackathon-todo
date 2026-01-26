from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4


class EventBase(SQLModel):
    event_type: str = Field(nullable=False)
    # payload ko JSON column me store karenge
    payload: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    user_id: Optional[UUID] = Field(default=None)
    correlation_id: Optional[UUID] = Field(default=None)
    processed: bool = Field(default=False)


class Event(EventBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key to User (optional)
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id")


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: UUID
    timestamp: datetime


class EventUpdate(SQLModel):
    processed: Optional[bool] = None
    # Agar update me payload change karna ho
    payload: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
