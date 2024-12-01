from pydantic import BaseModel
from typing import Optional, List

class QuestionBase(BaseModel):
    id: int
    content: str

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    questions: List[QuestionBase]

class UserDelete(BaseModel):
    id: Optional[int]
    name: Optional[str]