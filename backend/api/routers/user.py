# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List

# from database.models import User
# from database.database import get_db
# from api.schema import user


# router = APIRouter(
#     prefix="/api/user",
# )

# def get_user_by_name(name: str, db: Session):
#     return db.query(User).filter(User.name == name).first()

# @router.get("/", response_model=List[user.User])
# def get_list(db: Session = Depends(get_db)):
#     _user_list = db.query(User).all()
#     return _user_list

# @router.post("/", response_model=user.User)
# def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
#     try:
#         if get_user_by_name(user.name, db) is not None:
#             raise HTTPException(status_code=400, detail="This id is already existed") 
#         new_user = User(name=user.name, email=user.email)
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
#         return new_user
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
# @router.delete("/{user_name}", response_model=user.User)
# def delete_user(user_name: str, db: Session = Depends(get_db)):
#     try:
#         return user.delete_user_name(user_name, db)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.put("/{user_name}", response_model=user.User)
# def update_user(user: user.UserUpdate,user_name: str, db: Session = Depends(get_db)):
#     try:
#         return user.update_user(user, user_name, db)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))