from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Login, UserCreate, UserDisplay, Token
from ..models import User
from ..utils.hashing import Hash
from ..utils.jwt_token import create_access_token

router = APIRouter()

@router.post("/users/register", response_model=UserDisplay)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username already taken")
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    # If no existing user, proceed to create a new user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hash.bcrypt(user.password)
    )
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/users/login", response_model=Token)
async def login(request: Login, db: Session = Depends(get_db)):
    # Attempt to find the user by email or username
    user = db.query(User).filter((User.email == request.username) | (User.username == request.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")  # More generic message

    # Verify password
    if not Hash.verify(user.hashed_password, request.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Generate a JWT token
    access_token = await create_access_token(data={"sub": user.email,'id':user.id})  # Consider including user ID as well
    return {"access_token": access_token, "token_type": "bearer"}
