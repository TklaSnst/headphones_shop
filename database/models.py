from sqlalchemy import ForeignKey
from sqlalchemy.orm import (DeclarativeBase, mapped_column, Mapped,)


class Base(DeclarativeBase):
    pass


class Color(Base):
    __tablename__ = "colors"
    color_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    color_name: Mapped[str] = mapped_column(nullable=False)


class Item(Base):
    __tablename__ = "items"
    item_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    color: Mapped[int] = mapped_column(ForeignKey(Color.color_id), default=1)
    brand: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    img_url: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    jwt_refresh_token: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
