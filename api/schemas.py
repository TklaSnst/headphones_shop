from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel


class Base(BaseModel):
    pass


class UserRead(Base):
    id: int
    name: str
    is_superuser: bool
    email: str


class UserCreate(Base):
    id: int
    name: str
    hashed_password: str
    is_superuser: bool
    email: str


class UserUpdate(Base):
    name: Optional[str]
    is_superuser: Optional[str]
    email: Optional[str]


class ItemCreate(Base):
    fullname: str
    brand: str
    price: int
    img: str
    description: str
