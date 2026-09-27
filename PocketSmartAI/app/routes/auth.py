from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import create_access_token
from app.auth import hash_password
from app.auth import verify_password

from app.database import get_db

from app.dependencies import get_current_user

from app.models import User

from app.schemas import LoginRequest
from app.schemas import RegisterRequest
from app.schemas import UserOut


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserOut,
    status_code=201,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):

    email = data.email.strip().lower()

    existing = db.scalar(
        select(User).where(
            User.email == email
        )
    )

    if existing:

        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists.",
        )

    user = User(
        email=email,
        full_name=data.full_name.strip(),
        password_hash=hash_password(
            data.password
        ),
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=UserOut,
)
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):

    email = data.email.strip().lower()

    user = db.scalar(
        select(User).where(
            User.email == email
        )
    )

    if not user or not verify_password(
        data.password,
        user.password_hash,
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token = create_access_token(
        user.id
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=60 * 60 * 24,
    )

    return user


@router.post("/logout")
def logout(response: Response):

    response.delete_cookie(
        "access_token"
    )

    return {
        "message": "Logged out successfully."
    }


@router.get(
    "/me",
    response_model=UserOut,
)
def me(
    user: User = Depends(
        get_current_user
    ),
):

    return user