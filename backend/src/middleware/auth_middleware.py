from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from uuid import UUID
from ..services.auth_service import AuthService
from ..database.database import get_session
from contextlib import contextmanager
from functools import lru_cache


class AuthMiddleware:
    def __init__(self):
        self.security = HTTPBearer()

    def get_session(self):
        """Get a database session."""
        session = next(get_session())
        try:
            yield session
        finally:
            session.close()

    async def get_current_user_id(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """Extract and verify the current user ID from the token."""
        try:
            token = credentials.credentials
            # Create a session for this request
            session_gen = get_session()
            session = next(session_gen)

            try:
                auth_service = AuthService(session)
                user_id = auth_service.verify_token(token)
                if not user_id:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid or expired token",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

                return user_id
            finally:
                session.close()
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )


# Create a global instance of the auth middleware
auth_middleware = AuthMiddleware()