from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_users import FastAPIUsers
from starlette.staticfiles import StaticFiles
from database import create_tables, drop_tables, User
from pages import router as pages_router
from api import (get_user_manager, auth_backend,
                 UserUpdate, UserRead, UserCreate)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    print('tables dropped')
    await create_tables()
    print('tables created and clean')
    yield
    print('shutdown...')


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(pages_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
