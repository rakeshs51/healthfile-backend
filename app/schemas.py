# schemas.py
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import List, Optional
from datetime import date, datetime

class ReportBase(BaseModel):
    title: str
    report_created_date: date
    isVisible: bool

class ReportCreate(BaseModel):
    title: str
    report_created_date: date
    isVisible: bool
    file: Optional[UploadFile] = None

    @classmethod
    def as_form(
        cls, 
        title: str = Form(...), 
        report_created_date: date = Form(...), 
        isVisible: bool = Form(...), 
        file: Optional[UploadFile] = File(None)
    ) -> "ReportCreate":
        return cls(title=title, report_created_date=report_created_date, isVisible=isVisible, file=file)



class ReportUpdate(BaseModel):
    title: str = None
    report_created_date: date = None
    isVisible: bool = None

class ReportResponse(ReportBase):
    id: int
    created_at: datetime
    file_url: HttpUrl  # URL to the uploaded file
    category_id: int
    category_name: str

    class Config:
        orm_mode: True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: str = None

class Category(CategoryBase):
    id: int
    reports: List[ReportResponse] = []

    class Config:
        orm_mode: True



#User 

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="The username of the user")
    email: EmailStr = Field(..., description="The email address of the user")
    password: str = Field(..., description="The password for the user")

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "securepassword123"
            }
        }

class Login(BaseModel):
    username_or_email: str = Field(..., description="The user's username or email address")
    password: str = Field(..., description="The user's password")

    class Config:
        schema_extra = {
            "example": {
                "username_or_email": "johndoe@example.com",
                "password": "securepassword123"
            }
        }

class UserDisplay(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True  # Enable ORM mode to facilitate returning ORM objects directly

        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com"
            }
        }


class UserInfoSchema(BaseModel):
    name: Optional[str] = Field(None, example="John Doe")
    date_of_birth: Optional[date] = Field(None, example="1990-01-01")
    gender: Optional[str] = Field(None, example="Male")
    phone_number: Optional[str] = Field(None, example="+1234567890")
    weight: Optional[float] = Field(None, example=70.5)
    height: Optional[float] = Field(None, example=175.0)
    age: Optional[int] = Field(None, example=30)
    bmi: Optional[float] = Field(None, example=23.5)
    emergency_contact_number: Optional[str] = Field(None, example="+0987654321")

    class Config:
        orm_mode = True