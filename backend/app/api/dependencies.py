
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from sqlalchemy.orm import Session

from backend.app.core.auth import decode_access_token
from backend.app.database.connection import get_db
from backend.app.models.user import User


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_exception

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = UUID(payload.get("sub", ""))

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise credentials_exception

    user = db.get(User, user_id)

    if user is None or not user.is_active:
        raise credentials_exception

    return user
