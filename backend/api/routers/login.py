from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User
from api.schema import user

router = APIRouter(
    prefix="/api/login"
)

@router.get("/{username}", response_model=user.User)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user_data = db.query(User).filter(User.name == username).first()
    if user_data is not None:
        return user_data
    else:
        raise HTTPException(status_code=400, detail="존재하지 않는 유저입니다.")

@router.post("/", response_model=user.User)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.name == user.name).first() is not None:
        raise HTTPException(status_code=400, detail="이미 존재하는 이름입니다.")
    new_user = User(name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user