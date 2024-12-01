from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

class UserDelete(BaseModel):
    id: Optional[int]
    name: Optional[str]