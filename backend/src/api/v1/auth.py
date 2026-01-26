from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import Session
from uuid import UUID
from ...database.database import get_session
from ...models.user import UserCreate, UserLogin, UserRead
from ...services.user_service import UserService
from ...services.auth_service import AuthService
from ...middleware.auth_middleware import auth_middleware

router = APIRouter(prefix="/auth", tags=["auth"])


def get_current_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(auth_middleware.security)) -> UUID:
    """Dependency to get current user ID from token"""
    return auth_middleware.get_current_user_id(credentials.credentials)


@router.post("/register", response_model=UserRead)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    user_service = UserService(session)

    # Check if user already exists
    existing_user = user_service.get_user_by_username(user_create.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    existing_email = user_service.get_user_by_email(user_create.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create the user
    user = user_service.create_user(user_create)
    return user


@router.post("/login")
def login(user_login: UserLogin, session: Session = Depends(get_session)):
    """Login a user and return access token"""
    auth_service = AuthService(session)
    user = auth_service.authenticate_user(user_login.username, user_login.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login
    user_service = UserService(session)
    user_service.update_last_login(user.id)

    # Create access token
    access_token = auth_service.create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    """Logout a user"""
    # In a stateless JWT system, logout is typically handled on the client side
    # by removing the token. We can add additional logic here if needed.
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserRead)
def get_current_user(
    current_user_id: UUID = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """Get current user information"""
    user_service = UserService(session)
    user = user_service.get_user_by_id(current_user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user