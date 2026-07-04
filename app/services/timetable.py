from __future__ import annotations
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.timetable import Timetable
from app.repositories.timetable import timetable_repo
from app.repositories.teacher import teacher_repo
from app.repositories.room import room_repo
from app.repositories.group import group_repo
from app.schemas.timetable import TimetableCreate, TimetableUpdate


class TimetableService:

    def get_all(self, db: Session) -> List[Timetable]:
        return timetable_repo.get_multi_sorted(db)

    def get_or_404(self, db: Session, entry_id: int) -> Timetable:
        entry = timetable_repo.get(db, id=entry_id)
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Jadval yozuvi topilmadi",
            )
        return entry

    def get_by_group(self, db: Session, group_id: int) -> List[Timetable]:
        if not group_repo.get(db, id=group_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guruh topilmadi")
        return timetable_repo.get_by_group(db, group_id=group_id)

    def get_by_teacher(self, db: Session, teacher_id: int) -> List[Timetable]:
        if not teacher_repo.get(db, id=teacher_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="O'qituvchi topilmadi")
        return timetable_repo.get_by_teacher(db, teacher_id=teacher_id)

    def _check_conflicts(
        self, db: Session, data: TimetableCreate | TimetableUpdate, exclude_id: int | None = None
    ) -> None:
        teacher_id  = getattr(data, "teacher_id", None)
        room_id     = getattr(data, "room_id", None)
        group_id    = getattr(data, "group_id", None)
        day_of_week = getattr(data, "day_of_week", None)
        start_time  = getattr(data, "start_time", None)

        if day_of_week is None or start_time is None:
            return  # Partial update — skip conflict check

        if room_id and timetable_repo.get_conflict(
            db, room_id=room_id, day_of_week=day_of_week, start_time=start_time, exclude_id=exclude_id
        ):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bu xona bu vaqtda band!")

        if group_id and timetable_repo.get_conflict(
            db, group_id=group_id, day_of_week=day_of_week, start_time=start_time, exclude_id=exclude_id
        ):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bu guruh bu vaqtda boshqa darsda!")

        if teacher_id and timetable_repo.get_conflict(
            db, teacher_id=teacher_id, day_of_week=day_of_week, start_time=start_time, exclude_id=exclude_id
        ):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bu o'qituvchi bu vaqtda boshqa darsda!")

    def create(self, db: Session, data: TimetableCreate) -> Timetable:
        if not teacher_repo.get(db, id=data.teacher_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="O'qituvchi topilmadi")
        if not room_repo.get(db, id=data.room_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Xona topilmadi")
        if not group_repo.get(db, id=data.group_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guruh topilmadi")
        self._check_conflicts(db, data)
        return timetable_repo.create(db, obj_in=data.model_dump())

    def update(self, db: Session, entry_id: int, data: TimetableUpdate) -> Timetable:
        entry = self.get_or_404(db, entry_id)
        self._check_conflicts(db, data, exclude_id=entry_id)
        update_data = data.model_dump(exclude_unset=True)
        return timetable_repo.update(db, db_obj=entry, update_data=update_data)

    def delete(self, db: Session, entry_id: int) -> dict:
        self.get_or_404(db, entry_id)
        timetable_repo.delete(db, id=entry_id)
        return {"message": "Dars o'chirildi"}


timetable_service = TimetableService()
