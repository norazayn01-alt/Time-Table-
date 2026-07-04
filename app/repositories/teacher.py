from typing import Optional

from sqlalchemy.orm import Session

from app.models.teacher import Teacher
from app.repositories.base import BaseRepository


class TeacherRepository(BaseRepository[Teacher]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Teacher]:
        return db.query(Teacher).filter(Teacher.email == email).first()


teacher_repo = TeacherRepository(Teacher)
