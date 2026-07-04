from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Group(Base):
    __tablename__ = "groups"
    id            = Column(Integer, primary_key=True, autoincrement=True)
    name          = Column(String(50), nullable=False, unique=True, index=True)
    student_count = Column(Integer, nullable=False)
    course_year   = Column(Integer, nullable=False)
    created_at    = Column(DateTime, server_default=func.now())
    timetables    = relationship("Timetable", back_populates="group", cascade="all, delete-orphan")