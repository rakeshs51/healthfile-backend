from typing import Optional
from pydantic import HttpUrl
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime
from .database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    reports = relationship("Report", back_populates="category")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    report_created_date = Column(Date)
    isVisible = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    file_url: Mapped[Optional[HttpUrl]] = Column(String, nullable=True)
    # Foreign key to reference the User model
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship to link back to the User model
    user = relationship("User", back_populates="reports")

    category = relationship("Category", back_populates="reports")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to the Report model
    reports = relationship("Report", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
