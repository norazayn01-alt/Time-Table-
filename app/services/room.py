from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.room import Room
from app.repositories.room import room_repo
from app.schemas.room import RoomCreate, RoomUpdate


class RoomService:

    def get_all(self, db: Session) -> List[Room]:
        return room_repo.get_multi(db)

    def get_or_404(self, db: Session, room_id: int) -> Room:
        room = room_repo.get(db, id=room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Xona topilmadi",
            )
        return room

    def create(self, db: Session, data: RoomCreate) -> Room:
        if room_repo.get_by_name(db, name=data.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bu nomli xona allaqachon mavjud",
            )
        return room_repo.create(db, obj_in=data.model_dump())

    def update(self, db: Session, room_id: int, data: RoomUpdate) -> Room:
        room = self.get_or_404(db, room_id)
        update_data = data.model_dump(exclude_unset=True)
        if "name" in update_data:
            conflict = room_repo.get_by_name(db, name=update_data["name"])
            if conflict and conflict.id != room_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Bu nomli xona allaqachon mavjud",
                )
        return room_repo.update(db, db_obj=room, update_data=update_data)

    def delete(self, db: Session, room_id: int) -> dict:
        room = self.get_or_404(db, room_id)
        room_repo.delete(db, id=room_id)
        return {"message": f"'{room.name}' xonasi o'chirildi"}


room_service = RoomService()
