from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import User, UserInfo
from ..database import get_db
from ..utils.jwt_token import get_current_user
from ..schemas import *

router = APIRouter()

@router.get("/user/user-info/", response_model=UserInfoSchema)
async def read_user_info(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_info = db.query(UserInfo).filter(UserInfo.id == current_user.id).first()
    if not user_info:
        raise HTTPException(status_code=404, detail="User info not found")
    return user_info


@router.post("/user/user-info/", response_model=UserInfoSchema)
async def create_update_user_info(user_info: UserInfoSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user_info = db.query(UserInfo).filter(UserInfo.id == current_user.id).first()
    if db_user_info:
        for var, value in vars(user_info).items():
            setattr(db_user_info, var, value) if value else None
    else:
        db_user_info = UserInfo(id=current_user.id, **user_info.dict())
        db.add(db_user_info)
    db.commit()
    db.refresh(db_user_info)
    return db_user_info

@router.delete("/user/user-info/", status_code=204)
async def delete_user_info(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_info = db.query(UserInfo).filter(UserInfo.id == current_user.id).first()
    if not user_info:
        raise HTTPException(status_code=404, detail="User info not found")
    db.delete(user_info)
    db.commit()
    return {"message": "User info deleted"}

