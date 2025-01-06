from .token_manager import (
    refresh_tokens, get_id_from_access_token, create_tokens,
    security, decode_token, update_tokens_cookie
)
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import ExpiredSignatureError
import hashlib
import database
import json


load_dotenv()
router = APIRouter(tags=["auth"],
                   prefix="/auth")
http_bearer = HTTPBearer()


async def check_user_authorize(request: Request, response: Response):
    a_token = request.cookies.get('jwt_access_token')
    r_token = request.cookies.get('jwt_refresh_token')
    if (
            (await decode_token(a_token) == 0) and (await decode_token(r_token) == 0) or
            (await decode_token(a_token) == 1) and (await decode_token(r_token) == 0)
    ):
        return 0
    elif (await decode_token(a_token) == 0) and (await decode_token(r_token) == 1):
        print('expired signature')
        tokens = await refresh_tokens(a_token, r_token, response)
        return tokens
    return 1


@router.post("/registration/")
async def registration(credentials: database.SUserLogin):
    user = await database.get_user_by_name(
        async_session=database.async_session, username=credentials.username)
    if user:
        raise HTTPException(status_code=401, detail="username is already taken")

    hash_ = hashlib.new('sha256')
    hash_.update(credentials.password.encode())
    hashed_password = hash_.hexdigest()

    user_create = database.UserCreate(name=credentials.username, hashed_password=hashed_password)
    new_user_id = await database.create_user(
        async_session=database.async_session, user=user_create
    )
    return {
        "username": user_create.name,
        "uid": new_user_id
    }


@router.post("/login/")
async def login(credentials: database.SUserLogin, response: Response):
    try:
        user = await database.get_user_by_name(
            async_session=database.async_session,
            username=credentials.username
        )
        hash_ = hashlib.new('sha256')
        hash_.update(credentials.password.encode())
        hashed_password = hash_.hexdigest()
        if (not user) or (hashed_password != user.hashed_password):
            raise HTTPException(status_code=403, detail="Wrong username or password")

        new_tokens = await update_tokens_cookie(
            uid=user.user_id,
            response=response
        )
        await database.update_jwt_refresh_token(
            async_session=database.async_session,
            id=user.user_id,
            jwt_r_token=new_tokens.get('jwt_refresh_token')
        )
        return new_tokens
    except Exception as ex:
        print(f"error: {ex}")
        raise ex


@router.get("/users/me/")
async def get_user_info(
        request: Request,
        response: Response,
        creds: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    print('get me')
    # a_token = creds.credentials
    a_token = (
        request.cookies.get('jwt_access_token'))
    r_token = request.cookies.get('jwt_refresh_token')

    if (
            (await decode_token(a_token) == 0) and (await decode_token(r_token) == 0) or
            (await decode_token(a_token) == 1) and (await decode_token(r_token) == 0)
    ):
        return HTTPException(status_code=401, detail='refresh or access token is hueviy, login again')

    elif (await decode_token(a_token) == 0) and (await decode_token(r_token) == 1):
        print('expired signature')
        tokens = await refresh_tokens(a_token, r_token, response)
        uid = await get_id_from_access_token(a_token=tokens.get('jwt_access_token'))
        user = await database.get_user_by_uid(
            async_session=database.async_session,
            id=uid
        )
        return {
            "username": user.name,
            "uid": user.user_id,
            "email": user.email
        }

    uid = await get_id_from_access_token(a_token=a_token)
    user = await database.get_user_by_uid(
        async_session=database.async_session,
        id=uid
    )
    return {
        "username": user.name,
        "uid": user.user_id,
        "email": user.email
    }


@router.post('/logout/')
async def logout(creds: HTTPAuthorizationCredentials = Depends(HTTPBearer)):
    token = creds.credentials
    uid = await get_id_from_access_token(token)
    status = await database.delete_refresh_token(
        async_session=database.async_session,
        uid=uid
    )
    return {
        "uid": uid,
        "delete-status": status
    }
