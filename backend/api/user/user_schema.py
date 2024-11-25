from database.models import User
from pydantic import BaseModel

class UserBase(BaseModel):
    name = str
    email = str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

class UserDelete(BaseModel):
    id: int | None = None
    name = str | None = None
    email = str | None = None