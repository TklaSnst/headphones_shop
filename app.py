from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.staticfiles import StaticFiles
from database import create_tables, drop_tables
from pages import router as pages_router
from auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await drop_tables()
    # print('tables dropped')
    await create_tables()
    # print('tables created and clean')
    yield
    print('shutdown...')


app = FastAPI(lifespan=lifespan)

app.mount("/static",
          StaticFiles(directory="static"), name="static"
          )
app.include_router(pages_router)
app.include_router(auth_router)
