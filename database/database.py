from .models import Base
from os import getenv
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (AsyncSession, create_async_engine,
                                    async_sessionmaker)

load_dotenv()
engine = create_async_engine(getenv('DB'))
async_session = async_sessionmaker(engine)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

