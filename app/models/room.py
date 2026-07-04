from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id         = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name       = Column(String(50), nullable=False, unique=True, index=True)
    capacity   = Column(Integer, nullable=False)
    room_type  = Column(String(50), nullable=False, default="dars")
    is_active  = Column(Boolean, nullable=False, default=True, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    timetables = relationship(
        "Timetable",
        back_populates="room",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Room id={self.id} name={self.name!r}>"
