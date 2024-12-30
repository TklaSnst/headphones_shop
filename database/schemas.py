from pydantic import BaseModel


class Base(BaseModel):
    pass


class ItemCreate(Base):
    fullname: str
    brand: str
    price: int
    img: str
    description: str


class UserCreate(Base):
    name: str
    hashed_password: str
    email: str | None = None
    is_superuser: bool = False


class SUserLogin(Base):
    username: str
    password: str


class GetUser(Base):
    user_id: int | None
    username: str
    email: str | None
    is_superuser: bool
