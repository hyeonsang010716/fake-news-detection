from pydantic import BaseModel
from typing import Optional, List

from api.schema.user import User

class QuestionBase(BaseModel):
    content: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    subject: Optional[str]
    user: Optional[User]

    class Config:
        orm_mode = True