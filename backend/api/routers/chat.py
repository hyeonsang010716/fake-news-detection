from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from database.models import Question, Answer, User
from api.schema import question, user
from database.database import get_db
from model.agent import Agent


router = APIRouter(
    prefix="/api/chat"
)

@router.get("/", response_model=List[question.Question])
def get_all_question(db: Session = Depends(get_db)):
    _questions_lists = db.query(Question).all()
    return [question for question in _questions_lists]

@router.post("/", response_model=question.Question)
def answer_question(question: question.QuestionCreate, user: user.UserCreate, db: Session = Depends(get_db)):
    # existing_question = db.query(Question).filter(question.content == question.content).first()
    # if existing_question is not None:
    #     return existing_question
    try:
        curr_user = db.query(User).filter(User.name == user.name).first()
        new_question = Question(content=question.content, user = curr_user)
        
        # agent 답변 코드
        agent = Agent()

        graph = agent.graph # model

        try:
            response = graph.invoke({"youtube_link" : question.content})

            print("유튜브 내용 :")
            print(response["youtube_summary_content"])

            print("유튜브 주장들 : ")
            print(response["keywords"])

            print("주장들 결과 : ")
            print(response["response"])
        
            model_answer = response["response"][0]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="죄송합니다. 질문에 대한 답변이 어렵습니다.")
            
        new_answer = Answer(content=model_answer, question=new_question)

        db.add(new_question)
        db.add(new_answer)
        db.commit()
        db.refresh(new_question)
        db.refresh(new_answer)
        return new_question
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
        