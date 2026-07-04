from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base   

class Teacher(Base):

    __tablename__ = "teachers"

    id          = Column(Integer, primary_key=True, autoincrement=True)

    full_name   = Column(String(100), nullable=False, index=True)

    subject     = Column(String(100), nullable=False)

    email       = Column(String(150), unique=True, nullable=True)

    created_at  = Column(DateTime, server_default=func.now())

   
    timetables  = relationship(
        "Timetable",
        back_populates="teacher",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Teacher id={self.id} name={self.full_name}>"
