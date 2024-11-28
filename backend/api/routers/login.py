from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User
from api.schema import user

router = APIRouter(
    prefix="/api/login",
)

@router.post("/", response_model=user.User)
def create_user(user: user.UserCreate, db: Depends=Session(get_db)):
    if db.query(User).filter(User.name == user.name).first() is not None:
        raise HTTPException(status_code=400, detail="이미 존재하는 이름입니다.")
    new_user = User(name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user