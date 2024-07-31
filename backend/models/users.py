from pydantic import BaseModel
from typing import List


class User(BaseModel):
    login: str
    password_hash: str
    roles: List[str] = []


class UserAuth(BaseModel):
    login: str
    password: str


class UserUpdate(BaseModel):
    password: str


class RolesUpdate(BaseModel):
    codes: List[str]


class Tokens(BaseModel):
    refresh_token: str
    access_token: str
