from datetime import time
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.timetable import Timetable
from app.repositories.base import BaseRepository


class TimetableRepository(BaseRepository[Timetable]):

    def get_by_group(self, db: Session, *, group_id: int) -> List[Timetable]:
        return (
            db.query(Timetable)
            .filter(Timetable.group_id == group_id)
            .order_by(Timetable.day_of_week, Timetable.start_time)
            .all()
        )

    def get_by_teacher(self, db: Session, *, teacher_id: int) -> List[Timetable]:
        return (
            db.query(Timetable)
            .filter(Timetable.teacher_id == teacher_id)
            .order_by(Timetable.day_of_week, Timetable.start_time)
            .all()
        )

    def get_conflict(
        self,
        db: Session,
        *,
        room_id: Optional[int] = None,
        group_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
        day_of_week: int,
        start_time: time,
        exclude_id: Optional[int] = None,
    ) -> Optional[Timetable]:
        """Conflict tekshiruvi — bir vaqtda xona/guruh/o'qituvchi band emasligini tekshiradi."""
        q = db.query(Timetable).filter(
            Timetable.day_of_week == day_of_week,
            Timetable.start_time  == start_time,
        )
        if room_id:
            q = q.filter(Timetable.room_id == room_id)
        if group_id:
            q = q.filter(Timetable.group_id == group_id)
        if teacher_id:
            q = q.filter(Timetable.teacher_id == teacher_id)
        if exclude_id:
            q = q.filter(Timetable.id != exclude_id)
        return q.first()

    def get_multi_sorted(self, db: Session) -> List[Timetable]:
        return (
            db.query(Timetable)
            .order_by(Timetable.day_of_week, Timetable.start_time)
            .all()
        )


timetable_repo = TimetableRepository(Timetable)
