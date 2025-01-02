from authx import AuthX, AuthXConfig
from jwt.exceptions import ExpiredSignatureError
import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException
import database


load_dotenv()

config = AuthXConfig()
config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = "jwt_access_token"
config.JWT_REFRESH_COOKIE_NAME = "jwt_refresh_cookie"

security = AuthX(config=config)


async def create_tokens(id: int):
    access_token = security.create_access_token(uid=str(id))
    refresh_token = security.create_refresh_token(uid=str(id))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "id": id
    }


async def get_id_from_access_token(a_token):
    payload = jwt.decode(
        a_token,
        os.getenv("JWT_SECRET_KEY"),
        algorithms=["HS256"]
    )
    uid: int = payload.get("sub")
    return uid


async def decode_token(token):
    try:
        jwt.decode(
            token,
            os.getenv("JWT_SECRET_KEY"),
            algorithms=["HS256"]
        )
        return 1
    except ExpiredSignatureError:
        return 0


async def update_tokens_cookie(uid, response):
    tokens = await create_tokens(uid)
    r_token = tokens.get("refresh_token")
    a_token = tokens.get("access_token")
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, tokens.get('access_token'), httponly=True)
    response.set_cookie(config.JWT_REFRESH_COOKIE_NAME, tokens.get('refresh_token'), httponly=True)
    return {
        "access_token": a_token,
        "refresh_token": r_token
    }


async def refresh_tokens(r_token, a_token, response):
    uid = await get_id_from_access_token(a_token=a_token)
    user = await database.get_user_by_uid(
        async_session=database.async_session,
        id=uid
    )
    if user.jwt_refresh_token != r_token:
        raise HTTPException(status_code=401)
    new_tokens = await update_tokens_cookie(uid, response)
    return new_tokens
