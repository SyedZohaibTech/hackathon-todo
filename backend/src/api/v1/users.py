from fastapi import APIRouter, HTTPException, status, Form, Depends
from sqlmodel import Session
from ...database.database import get_session
from ...services.user_service import UserService
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["users"])

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """Register a new user securely"""
    user_service = UserService(session)

    # Check if username/email already exists
    if user_service.get_user_by_username(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    if user_service.get_user_by_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password before saving
    hashed_password = pwd_context.hash(password)

    # Create user in DB
    new_user = user_service.create_user(
        username=username,
        email=email,
        password=hashed_password
    )

    return {"message": "Registration successful", "user_id": str(new_user.id)}
