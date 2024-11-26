from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.models import Question, Answer
from api.schema import question, answer
from database.database import get_db

router = APIRouter(
    prefix="/api/question"
)

@router.post("/", response_model=question.Question)
def answer_question(q: str, db: Session = Depends(get_db)):
    if db.query(Question).filter(question.content == q) is not None:
        return db.query(Question).filter(question.content == q).answer
    try:
        answer = "답변입니당"
        new_answer = Answer(content=answer)
        new_question = Question(content=q, answer=new_answer)
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        return new_question
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
        
        