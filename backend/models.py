from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"

    session_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.session_id"))
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user = relationship("User", backref="Questions")

class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("question.id"))
    content = Column(Text, nullable=False)
    question = relationship("Question", backref="answers")