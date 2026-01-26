from typing import Optional
from sqlmodel import Session, select
from uuid import UUID
from ..models.user import User, UserCreate, UserUpdate, get_password_hash
from datetime import datetime


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user with hashed password"""
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=hashed_password
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by ID"""
        statement = select(User).where(User.id == user_id)
        return self.session.execute(statement).scalar()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        statement = select(User).where(User.username == username)
        return self.session.execute(statement).scalar()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        statement = select(User).where(User.email == email)
        return self.session.execute(statement).scalar()

    def update_user(self, user_id: UUID, user_update: UserUpdate) -> Optional[User]:
        """Update a user's information"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        # Update fields that are provided
        for field, value in user_update.model_dump(exclude_unset=True).items():
            if field == "password":
                # If password is being updated, hash it
                setattr(user, "hashed_password", get_password_hash(value))
            else:
                setattr(user, field, value)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def deactivate_user(self, user_id: UUID) -> bool:
        """Deactivate a user account"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        user.is_active = False
        self.session.add(user)
        self.session.commit()
        return True

    def activate_user(self, user_id: UUID) -> bool:
        """Activate a user account"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        user.is_active = True
        self.session.add(user)
        self.session.commit()
        return True

    def update_last_login(self, user_id: UUID) -> Optional[User]:
        """Update the last login time for a user"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        user.last_login_at = datetime.utcnow()
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user