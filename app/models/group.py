from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Group(Base):
    __tablename__ = "groups"

    id             = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name           = Column(String(50), nullable=False, unique=True, index=True)
    student_count  = Column(Integer, nullable=False)
    course_year    = Column(Integer, nullable=False)
    specialization = Column(String(100), nullable=True)
    is_active      = Column(Boolean, nullable=False, default=True, server_default="true")
    created_at     = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at     = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    timetables = relationship(
        "Timetable",
        back_populates="group",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Group id={self.id} name={self.name!r}>"
