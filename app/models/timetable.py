from sqlalchemy import (
    Column, Integer, String, DateTime, Time,
    ForeignKey, UniqueConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Timetable(Base):
    __tablename__ = "timetable"

    __table_args__ = (
        # Bir xona, bir kun, bir vaqtda faqat bitta dars
        UniqueConstraint("room_id", "day_of_week", "start_time", name="uq_room_day_time"),
        # Bir guruh, bir kun, bir vaqtda faqat bitta dars
        UniqueConstraint("group_id", "day_of_week", "start_time", name="uq_group_day_time"),
        # Bir o'qituvchi, bir kun, bir vaqtda faqat bitta dars
        UniqueConstraint("teacher_id", "day_of_week", "start_time", name="uq_teacher_day_time"),
    )

    id          = Column(Integer, primary_key=True, autoincrement=True, index=True)
    teacher_id  = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False, index=True)
    room_id     = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    group_id    = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False, index=True)
    day_of_week = Column(Integer, nullable=False)   # 1=Dushanba … 6=Shanba
    start_time  = Column(Time, nullable=False)
    end_time    = Column(Time, nullable=False)
    subject     = Column(String(100), nullable=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at  = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    teacher = relationship("Teacher", back_populates="timetables")
    room    = relationship("Room",    back_populates="timetables")
    group   = relationship("Group",   back_populates="timetables")

    def __repr__(self) -> str:
        return f"<Timetable id={self.id} day={self.day_of_week} time={self.start_time}>"
