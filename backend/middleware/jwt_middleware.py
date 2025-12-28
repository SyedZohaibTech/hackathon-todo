"""
JWT middleware for authentication
References: Task T202, Spec §X
"""
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from backend.auth import verify_jwt_token

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verify JWT token from Authorization header
    Args:
        credentials: HTTP authorization credentials
    Returns:
        User ID if token is valid
    Raises:
        HTTPException: If token is invalid or missing
    """
    token = credentials.credentials
    user_id = verify_jwt_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id