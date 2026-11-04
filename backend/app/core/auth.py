
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from backend.app.core.config import settings


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Generate a signed JWT access token."""

    now = datetime.now(timezone.utc)
    expires = now + (
        expires_delta
        or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": expires,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """Verify and decode a JWT access token."""

    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
