from authx import AuthX, AuthXConfig
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
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

http_bearer = HTTPBearer()


async def create_tokens(id: int):
    access_token = security.create_access_token(uid=str(id))
    refresh_token = security.create_refresh_token(uid=str(id))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "id": id
    }


async def validate_access_token(token):
    pass


async def validate_refresh_token(token):
    pass


async def refresh_tokens(r_token, a_token, uid: int):
    ...
    await create_tokens(id=uid)


@router.post("/registration/")
async def login(credentials: database.SUserLogin, response: Response):
    user = await database.get_user_by_name(
        async_session=database.async_session, username=credentials.username)
    if user:
        return "username is already taken"

    hash_ = hashlib.new('sha256')
    hash_.update(credentials.password.encode())
    hashed_password = hash_.hexdigest()

    user_create = database.UserCreate(name=credentials.username, hashed_password=hashed_password)
    new_user_id = await database.create_user(
        async_session=database.async_session, user=user_create
    )

    tokens = await create_tokens(new_user_id)
    refr_t = tokens.get("refresh_token")
    await database.update_jwt_refresh_token(
        async_session=database.async_session, id=new_user_id, jwt_r_token=refr_t
    )

    # response.set_cookie(config.JWT_REFRESH_COOKIE_NAME, refr_t, httponly=True)
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, tokens.get('access_token'), httponly=True)
    return {
        "access_token": tokens.get("access_token"),
        "refresh_token": tokens.get("refresh_token"),
        "user_id": new_user_id
    }
    # return HTTPException(status_code=401, detail="Wrong username or password")


@router.post("/login/")
async def login(credentials: database.SUserLogin):
    user = await database.get_user_by_name(
        async_session=database.async_session,
        username=credentials.username
    )
    if not user:
        raise HTTPException(status_code=401)
    hash_ = hashlib.new('sha256')
    hash_.update(credentials.password.encode())
    hashed_password = hash_.hexdigest()
    if hashed_password != user.hashed_password:
        raise HTTPException(status_code=403)


@router.get("/users/me")
async def get_user_info(
        creds: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    token = creds.credentials
    payload = jwt.decode(
        token,
        os.getenv("JWT_SECRET_KEY"),
        algorithms=["HS256"]
    )
    uid: int = payload.get("sub")
    user = await database.get_user_by_uid(
        async_session=database.async_session,
        id=uid
    )
    return {
        "uid": uid,
        "username": user.name,
        "email": user.email,
        "is_superuser": user.is_superuser
    }
