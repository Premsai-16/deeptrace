
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.auth import create_access_token
from backend.app.core.security import hash_password, verify_password
from backend.app.models.user import User
from backend.app.schemas.user import (
    UserCreate,
    LoginRequest,
    UserUpdate,
    PasswordChange,
    AccountDeactivation,
)


def register_user(db: Session, user_data: UserCreate) -> User:
    email = str(user_data.email).lower().strip()

    existing_user = db.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise ValueError("Email is already registered")

    new_user = User(
        full_name=user_data.full_name.strip(),
        email=email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, login_data: LoginRequest) -> str:
    email = str(login_data.email).lower().strip()

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if not user or not verify_password(
        login_data.password,
        user.hashed_password,
    ):
        raise ValueError("Invalid email or password")

    if not user.is_active:
        raise ValueError("Account is inactive")

    return create_access_token(subject=str(user.id))


def update_user_profile(
    db: Session,
    current_user: User,
    user_data: UserUpdate,
) -> User:
    if user_data.full_name is not None:
        current_user.full_name = user_data.full_name.strip()

    if user_data.email is not None:
        new_email = str(user_data.email).lower().strip()

        existing_user = db.scalar(
            select(User).where(
                User.email == new_email,
                User.id != current_user.id,
            )
        )

        if existing_user:
            raise ValueError("Email is already registered")

        current_user.email = new_email

    db.commit()
    db.refresh(current_user)

    return current_user


def change_user_password(
    db: Session,
    current_user: User,
    password_data: PasswordChange,
) -> None:
    if not verify_password(
        password_data.current_password,
        current_user.hashed_password,
    ):
        raise ValueError("Current password is incorrect")

    if password_data.current_password == password_data.new_password:
        raise ValueError(
            "New password must be different from current password"
        )

    current_user.hashed_password = hash_password(
        password_data.new_password
    )

    db.commit()


def deactivate_user(
    db: Session,
    current_user: User,
    deactivation_data: AccountDeactivation,
) -> None:
    if not verify_password(
        deactivation_data.password,
        current_user.hashed_password,
    ):
        raise ValueError("Password is incorrect")

    current_user.is_active = False

    db.commit()
