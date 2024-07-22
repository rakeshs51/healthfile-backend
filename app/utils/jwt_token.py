# utils/jwt_token.py
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from ..models import User
from sqlalchemy.orm import Session
from ..database import get_db

SECRET_KEY = "GOAT_123"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        email = payload.get("sub")
        if not user_id or not email:
            raise HTTPException(status_code=401, detail="Invalid JWT token")
        user = db.query(User).filter(User.id == user_id).first()
        if user.email!= email:
            raise HTTPException(status_code=401, detail="Invalid JWT Token, email and id mismatch")
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        print(user)
        return user
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials") from e


