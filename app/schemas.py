# schemas.py
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, HttpUrl
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

class Report(ReportBase):
    id: int
    created_at: datetime
    file_url: Optional[HttpUrl]  # URL to the uploaded file

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
    reports: List[Report] = []

    class Config:
        orm_mode: True
