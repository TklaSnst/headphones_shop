from authx import AuthX, AuthXConfig
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
import hashlib
import database
import os


load_dotenv()
config = AuthXConfig()
config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = "jwt_access_token"
config.JWT_REFRESH_COOKIE_NAME = "jwt_refresh_cookie"

security = AuthX(config=config)

router = APIRouter(tags=["auth"],
                   prefix="/auth")


async def create_tokens(id: int):
    access_token = security.create_access_token(uid=str(id))
    refresh_token = security.create_refresh_token(uid=str(id))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "id": id
    }


@router.post("/registration/")
async def login(credentials: database.SUserLogin, request: Request):
    user = database.get_user_by_name(
        async_session=database.async_session,username=credentials.username)
    if user:
        return "username is already taken"

    password = credentials.password
    hashed_password = hashlib.new('sha256')
    hashed_password.update(password.encode())

    user_create = database.UserCreate(name=credentials.username, hashed_password=hashed_password)
    new_user_id = await database.create_user(
        async_session=database.async_session, user=user_create
    )

    tokens = await create_tokens(new_user_id)
    refr_t = tokens.get("refresh_token")
    await database.update_jwt_refresh_token(
        async_session=database.async_session, id=new_user_id, jwt_r_token=refr_t
    )
    return {
        "access_token": tokens.get("access_token"),
        "refresh_token": tokens.get("refresh_token"),
        "user_id": new_user_id
    }
    # return HTTPException(status_code=401, detail="Wrong username or password")


@router.post("/login/")
async def login():
    pass
