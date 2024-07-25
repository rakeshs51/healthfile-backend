# crud.py
from typing import Any, Dict
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

    # Fetch the category name
    category_name = db.query(models.Category.name).filter(models.Category.id == category_id).scalar()

    # Add category_name to the report object (not part of the model, but for the response)
    new_report_dict = new_report.__dict__
    new_report_dict['category_name'] = category_name

    return new_report_dict


def get_report_for_specific_id_for_current_user(db: Session, report_id: int, user_id: int) -> ReportResponse:
    report = (
        db.query(
            models.Report.id,
            models.Report.title,
            models.Report.report_created_date,
            models.Report.isVisible,
            models.Report.created_at,
            models.Report.file_url,
            models.Report.category_id,
            models.Category.name.label("category_name"),
            models.Report.user_id
        )
        .join(models.Category, models.Report.category_id == models.Category.id)
        .filter(models.Report.id == report_id, models.Report.user_id == user_id)
        .first()
    )

    if report:
        return ReportResponse(
            id=report.id,
            title=report.title,
            report_created_date=report.report_created_date,
            isVisible=report.isVisible,
            created_at=report.created_at,
            file_url=report.file_url,
            category_id=report.category_id,
            category_name=report.category_name,
            user_id=report.user_id
        )

    return None

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

def update_report_method(db: Session, report_id: int, user_id: int, report: ReportUpdate) -> Dict[str, Any]:
    db_report = db.query(models.Report).filter(models.Report.id == report_id, models.Report.user_id == user_id).first()
    if db_report:
        for key, value in report.dict(exclude_unset=True).items():
            setattr(db_report, key, value)
        db.commit()
        db.refresh(db_report)

        # Fetch the category name
        category_name = db.query(models.Category.name).filter(models.Category.id == db_report.category_id).scalar()

        # Prepare the response
        response = {
            "id": db_report.id,
            "title": db_report.title,
            "report_created_date": db_report.report_created_date,
            "isVisible": db_report.isVisible,
            "created_at": db_report.created_at,
            "category_id": db_report.category_id,
            "category_name": category_name,
            "file_url": db_report.file_url,
            "user_id": db_report.user_id
        }
        return response

def delete_report_method(db: Session, report_id: int, user_id: int) -> Dict[str, Any]:
    db_report = db.query(models.Report).filter(models.Report.id == report_id, models.Report.user_id == user_id).first()
    if db_report:
        # Fetch the category name before deletion
        category_name = db.query(models.Category.name).filter(models.Category.id == db_report.category_id).scalar()

        # Prepare the response
        response = {
            "id": db_report.id,
            "title": db_report.title,
            "report_created_date": db_report.report_created_date,
            "isVisible": db_report.isVisible,
            "created_at": db_report.created_at,
            "category_id": db_report.category_id,
            "category_name": category_name,
            "file_url": db_report.file_url,
            "user_id": db_report.user_id
        }

        db.delete(db_report)
        db.commit()
        return response