from sqlalchemy.ext.asyncio import AsyncSession
from .models import Item
from api import ItemCreate
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


async def get_main_items(async_session: AsyncSession, item_id: Item.item_id):
    async with async_session() as session:
        try:
            stmt = select(Item).where(Item.item_id == item_id)
            result = await session.execute(stmt)
            item = result.scalar()
            return item
        except Exception as e:
            raise e
