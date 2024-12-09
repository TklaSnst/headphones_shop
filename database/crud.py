from sqlalchemy.ext.asyncio import AsyncSession
from .models import Item
from api import ItemCreate


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
