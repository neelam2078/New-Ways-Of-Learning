from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import JWTError
from jose import jwt

from passlib.context import CryptContext

from app.config import get_settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    password: str,
    password_hash: str,
) -> bool:

    return pwd_context.verify(
        password,
        password_hash,
    )


def create_access_token(
    user_id: int,
) -> str:

    settings = get_settings()

    expiration = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expiration,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> int | None:

    settings = get_settings()

    try:

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )

        subject = payload.get("sub")

        if not subject:
            return None

        return int(subject)

    except (
        JWTError,
        ValueError,
        TypeError,
    ):
        return None