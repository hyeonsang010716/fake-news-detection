from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.models import User, Question, Answer
from api.schema import question, answer
from database.database import get_db

router = APIRouter(
    prefix="/api/question"
)

@router.post("/", response_model=question.Question)
def answer_question(question: question.QuestionCreate, db: Session = Depends(get_db)):
    # if db.query(Question).filter(question.content == question.content) is not None:
    #     return db.query(Question).filter(question.content == question.content).first()
    try:
        new_question = Question(content=question.content)

        answer = "답변입니당"
        new_answer = Answer(content=answer, question=new_question)
        
        db.add(new_question)
        db.add(new_answer)
        db.commit()
        db.refresh(new_question)
        return new_question
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
        
        