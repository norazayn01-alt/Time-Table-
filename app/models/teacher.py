from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id         = Column(Integer, primary_key=True, autoincrement=True, index=True)
    full_name  = Column(String(100), nullable=False, index=True)
    subject    = Column(String(100), nullable=False)
    email      = Column(String(150), unique=True, nullable=True, index=True)
    is_active  = Column(Boolean, nullable=False, default=True, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    timetables = relationship(
        "Timetable",
        back_populates="teacher",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Teacher id={self.id} name={self.full_name!r}>"
