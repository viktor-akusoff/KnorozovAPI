from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from jose import exceptions as jwt_exc
from pydantic import ValidationError
from models.users import User
from schemas import UserSerializer
from database import db_users

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/users/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> User:
    try:
        token_data = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )

        if datetime.fromtimestamp(token_data['exp']) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (jwt_exc.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[dict[str, Any], None] = UserSerializer.serialize(
        db_users.find_one({"login": token_data['sub']})
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return User(**user)
