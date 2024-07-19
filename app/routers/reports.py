# report.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..database import get_db
from ..models import Report, Category
from ..schemas import *
from ..utils.crud import *
from ..utils.s3_client_operations import *

router = APIRouter()

@router.post("/categories/{category_id}/reports/", response_model=Report)
async def create_report_for_category(category_id: int, report: ReportCreate = Depends(ReportCreate.as_form), db: Session = Depends(get_db)):
    db_category = get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    
     # Upload file to S3 if present
    file_url = ""
    if report.file:
        try:
            file_url = await upload_file_to_s3(report.file)
            print(file_url)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")
    
    try:
        return create_report(db=db, report=report, file_url=file_url, category_id=category_id)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database transaction failed: {str(e)}")
    

@router.get("/reports/", response_model=List[Report])
def read_reports(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reports = get_reports(db, skip=skip, limit=limit)
    return reports

@router.get("/reports/{report_id}", response_model=Report)
def read_report(report_id: int, db: Session = Depends(get_db)):
    db_report = get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

@router.put("/reports/{report_id}", response_model=Report)
def update_report(report_id: int, report: ReportUpdate, db: Session = Depends(get_db)):
    db_report = get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    updated_report = update_report_method(db, report_id=report_id, report=report)
    return updated_report

@router.delete("/reports/{report_id}", response_model=Report)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    db_report = get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    deleted_report = delete_report_method(db, report_id=report_id)
    return deleted_report

@router.get("/reports_by_category/", response_model=Dict[str, Any])
def read_all_reports(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    result = {
        "status": "success",
        "data": [
            {
                "category": category.name,
                "reports": [
                    {
                        "id": report.id,
                        "title": report.title,
                        "report_created_date": report.report_created_date,
                        "isVisible": report.isVisible
                    } for report in category.reports
                ]
            } for category in categories
        ]
    }
    return result
