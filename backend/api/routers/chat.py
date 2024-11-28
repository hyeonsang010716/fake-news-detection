from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.models import Question, Answer, User
from api.schema import question, answer
from database.database import get_db
from model.agent import Agent


router = APIRouter(
    prefix="/api/chat"
)

@router.post("/", response_model=question.Question)
def answer_questio(question: question.QuestionCreate, db: Session = Depends(get_db)):
    existing_question = db.query(Question).filter(question.content == question.content).first()
    if existing_question is not None:
        return existing_question
    try:
        new_question = Question(content=question.content)
        
        # agent 답변 코드
        # agent = Agent()
        # graph = agent.graph 

        # model_answer = graph.invoke({"youtube_content" : question.content})
        # if not model_answer:
        #     model_answer="죄송합니다. 질문에 대한 답변이 어렵습니다."
        model_answer = "몰러유"
        new_answer = Answer(content=model_answer, question=new_question)

        db.add(new_question)
        db.add(new_answer)
        db.commit()
        db.refresh(new_answer)
        return new_answer
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
        
        