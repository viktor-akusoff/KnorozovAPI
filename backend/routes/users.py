import config
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.users import User, UserAuth, Tokens, UserUpdate, RolesUpdate
from schemas import UserSerializer, SafeUserSerializer, LanguageSerializer
from database import db_users, db_languages
from utils import hash_password, verify_hash, create_jwt_token
from deps import get_current_user


router = APIRouter(prefix='/users')

tag = 'User manipulation methods'


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary='Creates access and refresh tokens for user.',
    tags=[tag]
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    login = form_data.username

    check_users = UserSerializer.list_serialize(
        db_users.find({"login": login})
    )

    if not len(check_users):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong password or user doesn't exists."
        )

    password = form_data.password
    user = check_users[0]

    if not verify_hash(password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong password or user doesn't exists."
        )

    return dict(Tokens(
        refresh_token=create_jwt_token(
            login,
            config.REFRESH_TOKEN_EXPIRE_MINUTES,
            config.JWT_REFRESH_SECRET_KEY
        ),
        access_token=create_jwt_token(
            login,
            config.ACCESS_TOKEN_EXPIRE_MINUTES,
            config.JWT_SECRET_KEY
        ),
    ))


@router.post(
    "/signup",
    status_code=status.HTTP_200_OK,
    summary='Creates new user',
    tags=[tag]
)
async def signup(user_auth: UserAuth):

    no_users = not len(UserSerializer.list_serialize(db_users.find({})))

    check_users = UserSerializer.list_serialize(
        db_users.find({"login": user_auth.login})
    )

    if len(check_users) > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists."
        )

    if no_users:
        user = User(
            login=user_auth.login,
            password_hash=hash_password(user_auth.password),
            roles=["admin"]
        )
    else:
        user = User(
            login=user_auth.login,
            password_hash=hash_password(user_auth.password)
        )

    db_users.insert_one(dict(user))

    return {"message": "User was created!"}


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary='Returns the list of all users.',
    tags=[tag]
)
async def get_users(user: User = Depends(get_current_user)):

    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin rights are required."
        )

    users = SafeUserSerializer.list_serialize(
        db_users.find()
    )

    return users


@router.get(
    "/{login}",
    status_code=status.HTTP_200_OK,
    summary='Gets user by its login.',
    tags=[tag]
)
async def get_user(login: str):

    user = SafeUserSerializer.serialize(
        db_users.find_one({"login": login})
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist."
        )

    return user


@router.put(
    "/update_password",
    status_code=status.HTTP_200_OK,
    summary="Updates user's password.",
    tags=[tag]
)
async def update_password(
    update: UserUpdate,
    user: User = Depends(get_current_user)
):

    db_users.update_one(
        {"login": user.login},
        {"$set": {"password_hash": hash_password(update.password)}}
    )

    return {"message": "User's password was updated!"}


@router.delete(
    "/{login}/delete",
    status_code=status.HTTP_200_OK,
    summary='Deletes a user from the list.',
    tags=[tag]
)
async def remove_user(login: str, user: User = Depends(get_current_user)):

    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin rights are required."
        )

    user_to_delete = UserSerializer.serialize(
        db_users.find_one({"login": login})
    )

    if user_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist."
        )

    if "admin" in user_to_delete["roles"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Admin can't delete himself! " +
                "Use a command line tools to do such a thing"
            )
        )

    db_users.delete_one({"login": login})

    return {"message": "User was removed!"}


@router.put(
    "/{login}/set_roles",
    status_code=status.HTTP_200_OK,
    summary="Sets user's roles.",
    tags=[tag]
)
async def set_roles(
    login: str,
    update: RolesUpdate,
    user: User = Depends(get_current_user)
):

    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin rights are required."
        )

    user_to_update = SafeUserSerializer.serialize(
        db_users.find_one({"login": login})
    )

    if user_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist."
        )

    if "admin" in user_to_update["roles"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't add new roles to admin."
        )

    codes = [
        lang["code"] for lang in LanguageSerializer.list_serialize(
            db_languages.find()
        )
    ]

    for code in update.codes:
        if code not in codes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"There's no such a language with code '{code}' yet."
            )

    new_codes = list(set(update.codes))

    db_users.update_one({"login": login}, {"$set": {"roles": new_codes}})

    return {"message": "New roles were set to a user's roles."}


@router.put(
    "/{login}/add_roles",
    status_code=status.HTTP_200_OK,
    summary="Adds user's roles.",
    tags=[tag]
)
async def add_roles(
    login: str,
    update: RolesUpdate,
    user: User = Depends(get_current_user)
):

    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin rights are required."
        )

    user_to_update = SafeUserSerializer.serialize(
        db_users.find_one({"login": login})
    )

    if user_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist."
        )

    if "admin" in user_to_update["roles"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't add new roles to admin."
        )

    codes = [
        lang["code"] for lang in LanguageSerializer.list_serialize(
            db_languages.find()
        )
    ]

    for code in update.codes:
        if code not in codes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"There's no such a language with code '{code}' yet."
            )

    new_codes = list(set(user_to_update["roles"] + update.codes))

    db_users.update_one({"login": login}, {"$set": {"roles": new_codes}})

    return {"message": "New roles were added to a user's roles."}


@router.put(
    "/{login}/delete_roles",
    status_code=status.HTTP_200_OK,
    summary="Deletes user's roles.",
    tags=[tag]
)
async def delete_role(
    login: str,
    update: RolesUpdate,
    user: User = Depends(get_current_user)
):

    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin rights are required."
        )

    user_to_update = SafeUserSerializer.serialize(
        db_users.find_one({"login": login})
    )

    if user_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist."
        )

    if "admin" in user_to_update["roles"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't delete roles from admin."
        )

    codes = [
        lang["code"] for lang in LanguageSerializer.list_serialize(
            db_languages.find()
        )
    ]

    for code in update.codes:
        if code not in codes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"There's no such a language with code '{code}' yet."
            )

    new_codes = list(set(user_to_update["roles"]) - set(update.codes))

    db_users.update_one({"login": login}, {"$set": {"roles": new_codes}})

    return {"message": "Roles were deleted from a user's roles."}
