from typing import TYPE_CHECKING, Optional, Dict, Any
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from datetime import datetime
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .user import User


class ConversationBase(SQLModel):
    title: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    # context_data ko JSON column me store karenge
    context_data: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))


class Conversation(ConversationBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key to User
    user_id: UUID = Field(foreign_key="user.id")


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    user_id: UUID


class ConversationUpdate(SQLModel):
    title: Optional[str] = None
    is_active: Optional[bool] = None
    context_data: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
