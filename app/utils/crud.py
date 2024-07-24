# crud.py
from sqlalchemy.orm import Session
from ..models import Category, Report
from ..schemas import *
from .. import models

# Category CRUD methods

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category_method(db: Session, category: CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category_method(db: Session, category_id: int, category: CategoryUpdate):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db_category.name = category.name
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category_method(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category



# Report CRUD methods

def create_report(db: Session, report: ReportCreate, file_url: str, category_id: int, user_id: int):
    new_report = models.Report(
        title=report.title,
        report_created_date=report.report_created_date,
        isVisible=report.isVisible,
        file_url=file_url,
        category_id=category_id,
        user_id=user_id
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

def get_report_for_specific_id_for_current_user(db: Session, report_id: int, user_id: int) -> Report:
    return db.query(models.Report).filter(models.Report.id == report_id, models.Report.user_id == user_id).first()

def get_reports_for_current_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    reports = (
        db.query(
            models.Report.id,
            models.Report.title,
            models.Report.report_created_date,
            models.Report.isVisible,
            models.Report.created_at,
            models.Report.file_url,
            models.Report.category_id,
            models.Category.name.label("category_name")
        )
        .join(models.Category, models.Report.category_id == models.Category.id)
        .filter(models.Report.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return reports
def update_report_method(db: Session, report_id: int, user_id: int, report: ReportUpdate) -> Report:
    db_report = db.query(models.Report).filter(models.Report.id == report_id, models.Report.user_id == user_id).first()
    if db_report:
        for key, value in report.dict(exclude_unset=True).items():
            setattr(db_report, key, value)
        db.commit()
        db.refresh(db_report)
    return db_report

def delete_report_method(db: Session, report_id: int, user_id: int) -> Report:
    db_report = db.query(models.Report).filter(models.Report.id == report_id, models.Report.user_id == user_id).first()
    if db_report:
        db.delete(db_report)
        db.commit()
    return db_report
