from typing import Optional

from sqlalchemy.orm import Session

from app.models.room import Room
from app.repositories.base import BaseRepository


class RoomRepository(BaseRepository[Room]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Room]:
        return db.query(Room).filter(Room.name == name).first()


room_repo = RoomRepository(Room)
