from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.teacher import Teacher
from app.repositories.teacher import teacher_repo
from app.schemas.teacher import TeacherCreate, TeacherUpdate


class TeacherService:

    def get_all(self, db: Session) -> List[Teacher]:
        return teacher_repo.get_multi(db)

    def get_or_404(self, db: Session, teacher_id: int) -> Teacher:
        teacher = teacher_repo.get(db, id=teacher_id)
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="O'qituvchi topilmadi",
            )
        return teacher

    def create(self, db: Session, data: TeacherCreate) -> Teacher:
        if data.email:
            existing = teacher_repo.get_by_email(db, email=data.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Bu email allaqachon mavjud",
                )
        return teacher_repo.create(db, obj_in=data.model_dump())

    def update(self, db: Session, teacher_id: int, data: TeacherUpdate) -> Teacher:
        teacher = self.get_or_404(db, teacher_id)
        update_data = data.model_dump(exclude_unset=True)
        if "email" in update_data and update_data["email"]:
            conflict = teacher_repo.get_by_email(db, email=update_data["email"])
            if conflict and conflict.id != teacher_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Bu email allaqachon mavjud",
                )
        return teacher_repo.update(db, db_obj=teacher, update_data=update_data)

    def delete(self, db: Session, teacher_id: int) -> dict:
        teacher = self.get_or_404(db, teacher_id)
        teacher_repo.delete(db, id=teacher_id)
        return {"message": f"'{teacher.full_name}' o'qituvchisi o'chirildi"}


teacher_service = TeacherService()
