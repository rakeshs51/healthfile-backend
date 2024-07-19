from fastapi import FastAPI

from app import models
from app.database import engine
from .routers.reports import router as report_router
from .routers.category import router as category_router
from .utils.s3_client import init_s3_client

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_s3_client()
    print("S3 Client Initialized")


app.include_router(report_router, prefix="/api", tags=["reports"])
app.include_router(category_router, prefix="/api", tags=["categories"])

@app.get("/healthcheck")
async def ping():
    return {"message": "Health OK"}