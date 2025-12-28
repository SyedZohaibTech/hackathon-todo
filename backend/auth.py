"""
JWT utilities for authentication
References: Task T202, Spec §X
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-here-32-character-minimum")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60  # 7 days

def create_jwt_token(user_id: str) -> str:
    """
    Create a JWT token for the given user ID
    Args:
        user_id: The user's ID
    Returns:
        JWT token as string
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str) -> Optional[str]:
    """
    Verify a JWT token and return the user ID if valid
    Args:
        token: JWT token to verify
    Returns:
        User ID if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except jwt.PyJWTError:
        return None