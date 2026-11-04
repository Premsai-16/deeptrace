
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.database.connection import get_db
from backend.app.models.user import User

from backend.app.schemas.user import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
    UserUpdate,
    PasswordChange,
    AccountDeactivation,
)

from backend.app.services.user_service import (
    register_user,
    login_user,
    update_user_profile,
    change_user_password,
    deactivate_user,
)


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        return register_user(db, user_data)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        access_token = login_user(db, login_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        ) from error


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_my_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return update_user_profile(
            db,
            current_user,
            user_data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
)
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        change_user_password(
            db,
            current_user,
            password_data,
        )

        return {
            "message": "Password changed successfully"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.post(
    "/deactivate",
    status_code=status.HTTP_200_OK,
)
def deactivate_my_account(
    deactivation_data: AccountDeactivation,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        deactivate_user(
            db,
            current_user,
            deactivation_data,
        )

        return {
            "message": "Account deactivated successfully"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
