# schemas.py
from pydantic import BaseModel
from typing import List
from datetime import date, datetime

class ReportBase(BaseModel):
    title: str
    report_created_date: date
    isVisible: bool

class ReportCreate(ReportBase):
    pass

class ReportUpdate(BaseModel):
    title: str = None
    report_created_date: date = None
    isVisible: bool = None

class Report(ReportBase):
    id: int
    created_at: datetime

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
