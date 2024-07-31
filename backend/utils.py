import config
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_hash(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_jwt_token(
    subject: Union[str, Any],
    expire: int,
    secret: str
) -> str:

    expires_delta = (
        datetime.now() +
        timedelta(minutes=expire)
    )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret, config.ALGORITHM)

    return encoded_jwt
