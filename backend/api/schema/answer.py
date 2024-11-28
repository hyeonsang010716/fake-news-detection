from pydantic import BaseModel
from typing import List, Optional

from api.schema.question import Question

class AnswerBase(BaseModel):
    content: str

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    question: Question

    class Config:
        from_attributes = True

class AnswerDelete(BaseModel):
    id: Optional[int]
    content: Optional[str]