from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.schemas.teacher import TeacherCreate, TeacherUpdate, TeacherResponse
from app.services.teacher import teacher_service

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.get("/", response_model=List[TeacherResponse], summary="Barcha o'qituvchilar")
def list_teachers(db: Session = Depends(get_db)):
    return teacher_service.get_all(db)


@router.get("/{teacher_id}", response_model=TeacherResponse, summary="Bitta o'qituvchi")
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    return teacher_service.get_or_404(db, teacher_id)


@router.post(
    "/",
    response_model=TeacherResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yangi o'qituvchi qo'shish",
)
def create_teacher(data: TeacherCreate, db: Session = Depends(get_db)):
    return teacher_service.create(db, data)


@router.put("/{teacher_id}", response_model=TeacherResponse, summary="O'qituvchini yangilash")
def update_teacher(teacher_id: int, data: TeacherUpdate, db: Session = Depends(get_db)):
    return teacher_service.update(db, teacher_id, data)


@router.delete("/{teacher_id}", status_code=status.HTTP_200_OK, summary="O'qituvchini o'chirish")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    return teacher_service.delete(db, teacher_id)
