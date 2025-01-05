from sqlalchemy.ext.asyncio import AsyncSession

import database
from .models import Item, User, Basket
from .schemas import ItemCreate, UserCreate, BasketAddItem
from sqlalchemy import select


async def create_item(async_session: AsyncSession,
                      name: str, price: int, img_src: str, description: str):
    async with async_session() as session:
        try:
            data = ItemCreate(
                name=name,
                price=price,
                img_src=img_src,
                description=description
            )
            item_create = Item(**data.model_dump())
            session.add(item_create)
            await session.commit()
            return "item created"
        except Exception as e:
            raise e


async def get_item_by_id(async_session: AsyncSession, item_id: Item.item_id):
    async with async_session() as session:
        try:
            stmt = select(Item).where(Item.item_id == item_id)
            result = await session.execute(stmt)
            item = result.scalar()
            return item
        except Exception as e:
            raise e


async def get_start_items(async_session: AsyncSession, c: int):
    async with async_session() as session:
        try:
            stmt = session.querry(Item).filter(Item.item_id <= c).all()
            result = await session.execute(stmt)
            items = result.scalars()
            return items
        except Exception as e:
            raise e


async def get_main_items(async_session: AsyncSession, item_id: Item.item_id):
    async with async_session() as session:
        try:
            stmt = select(Item).where(Item.item_id == item_id)
            result = await session.execute(stmt)
            item = result.scalar()
            return item
        except Exception as e:
            raise e


async def get_user_by_name(async_session: AsyncSession, username):
    async with async_session() as session:
        try:
            stmt = select(User).where(User.name == username)
            result = await session.execute(stmt)
            user = result.scalar()
            return user
        except Exception as e:
            print(f"error: {e}")
            raise e


async def get_user_by_uid(async_session: AsyncSession, id: int) -> User:
    async with async_session() as session:
        try:
            stmt = select(User).where(User.user_id == id)
            result = await session.execute(stmt)
            user = result.scalar()
            return user
        except Exception as e:
            print(f"error: {e}")
            raise e


async def create_user(async_session: AsyncSession, user: UserCreate):
    async with async_session() as session:
        try:
            user_create = User(**user.model_dump())
            session.add(user_create)
            await session.commit()
            await session.refresh(user_create)
            return user_create.user_id
        except Exception as e:
            print(f"error: {e}")
            raise e


async def update_jwt_refresh_token(
        async_session: AsyncSession, id: User.user_id, jwt_r_token: str
):
    async with async_session() as session:
        try:
            stmt = select(User).where(User.user_id == id)
            result = await session.execute(stmt)
            user = result.scalar()
            user.jwt_refresh_token = jwt_r_token
            await session.commit()
        except Exception as e:
            print(f"error: {e}")
            raise e


async def delete_refresh_token(async_session: AsyncSession, uid: int):
    async with async_session() as session:
        try:
            stmt = select(User).where(User.user_id == uid)
            result = await session.execute(stmt)
            user = result.scalar()
            user.jwt_refresh_token = None
            await session.commit()
            return 1
        except Exception as e:
            return 0


async def add_item_to_basket(async_session: AsyncSession, item: BasketAddItem):
    async with async_session() as session:
        try:
            item_add = Basket(**item.model_dump())
            session.add(item_add)
            await session.commit()
            await session.refresh(item_add)
            return item_add.string_id
        except Exception as e:
            print(f"error: {e}")
            raise e
