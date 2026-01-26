from sqlmodel import SQLModel  # ✅ add this

from .task import Task, TaskCreate, TaskRead, TaskUpdate
from .user import User, UserCreate, UserRead, UserUpdate, UserLogin, UserPublic
from .conversation import Conversation, ConversationCreate, ConversationRead, ConversationUpdate
from .event import Event, EventCreate, EventRead, EventUpdate

__all__ = [
    "SQLModel",  # ✅ add this
    "Task",
    "TaskCreate",
    "TaskRead",
    "TaskUpdate",
    "User",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "UserLogin",
    "UserPublic",
    "Conversation",
    "ConversationCreate",
    "ConversationRead",
    "ConversationUpdate",
    "Event",
    "EventCreate",
    "EventRead",
    "EventUpdate"
]
