from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from api.user import user_crud, user_schema

router = APIRouter(
    prefix="api/question"
)

@router.get("/", response_model=user_schema.User)
def get_list(db: Session = Depends(get_db)):
    # _quetion_list = user_crud.

# , user=user_schema.UserCreate