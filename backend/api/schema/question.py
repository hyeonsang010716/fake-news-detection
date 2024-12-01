from pydantic import BaseModel
from typing import Optional, List

from api.schema.user import User

class AnswerBase(BaseModel):
    id: int
    content: str

class QuestionBase(BaseModel):
    content: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    user: Optional[User]
    answers: List[AnswerBase]
