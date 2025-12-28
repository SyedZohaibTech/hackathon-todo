"""
Authentication routes
References: Task T215, Spec §X
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from backend.db import get_session
from backend.models import User, UserCreate, UserRead
from backend.auth import create_jwt_token
from backend.utils import create_success_response, create_error_response
from passlib.context import CryptContext
import uuid

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password
    """
    return pwd_context.hash(password)

@router.post("/signup", response_model=dict)
def signup(user: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user
    Args:
        user: User creation data (email, password, name)
        session: Database session
    Returns:
        Success response with user information
    Raises:
        HTTPException: If email already exists
    """
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create new user
    db_user = User(
        email=user.email,
        name=user.name,
        password_hash=hashed_password
    )

    # Add to database
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Return success response with user data
    user_data = UserRead.from_orm(db_user) if hasattr(User, "from_orm") else UserRead(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name
    )
    return create_success_response(user_data)

@router.post("/login", response_model=dict)
def login(email: str, password: str, session: Session = Depends(get_session)):
    """
    Authenticate user and return JWT token
    Args:
        email: User's email address
        password: User's password
        session: Database session
    Returns:
        Success response with JWT token and user info
    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create JWT token
    token = create_jwt_token(str(user.id))

    # Return success response with token and user info
    user_data = UserRead.from_orm(user) if hasattr(User, "from_orm") else UserRead(
        id=user.id,
        email=user.email,
        name=user.name
    )
    return create_success_response({
        "token": token,
        "user": user_data
    })