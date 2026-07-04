from sqlalchemy import Column, Integer, String, DateTime, Time, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Timetable(Base):

    __tablename__ = "timetable"

    id          = Column(Integer, primary_key=True, autoincrement=True)

    teacher_id  = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    room_id     = Column(Integer, ForeignKey("rooms.id"), nullable=False)

    group_id    = Column(Integer, ForeignKey("groups.id"), nullable=False)

    day_of_week = Column(Integer, nullable=False)

    start_time  = Column(Time, nullable=False)
    end_time    = Column(Time, nullable=False)

    subject     = Column(String(100), nullable=False)

    created_at  = Column(DateTime, server_default=func.now())


    teacher     = relationship("Teacher", back_populates="timetables")

    room        = relationship("Room", back_populates="timetables")

    group       = relationship("Group", back_populates="timetables")

    def __repr__(self):
        return f"<Timetable id={self.id} day={self.day_of_week} time={self.start_time}>"