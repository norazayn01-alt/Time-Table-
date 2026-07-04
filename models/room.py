from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Room(Base):
    __tablename__ = "rooms"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(String(50), nullable=False, unique=True, index=True)
    capacity    = Column(Integer, nullable=False)
    room_type   = Column(String(50), nullable=False, default='dars')
    created_at  = Column(DateTime, server_default=func.now())
    timetables  = relationship("Timetable", back_populates="room", cascade="all, delete-orphan")