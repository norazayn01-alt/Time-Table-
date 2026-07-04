from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.schemas.timetable import TimetableCreate, TimetableUpdate, TimetableResponse
from app.services.timetable import timetable_service

router = APIRouter(prefix="/timetable", tags=["Timetable"])


@router.get("/", response_model=List[TimetableResponse], summary="Barcha jadval")
def list_timetable(db: Session = Depends(get_db)):
    return timetable_service.get_all(db)


@router.get("/{entry_id}", response_model=TimetableResponse, summary="Bitta jadval yozuvi")
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    return timetable_service.get_or_404(db, entry_id)


@router.get("/group/{group_id}", response_model=List[TimetableResponse], summary="Guruh jadvali")
def group_timetable(group_id: int, db: Session = Depends(get_db)):
    return timetable_service.get_by_group(db, group_id)


@router.get("/teacher/{teacher_id}", response_model=List[TimetableResponse], summary="O'qituvchi jadvali")
def teacher_timetable(teacher_id: int, db: Session = Depends(get_db)):
    return timetable_service.get_by_teacher(db, teacher_id)


@router.post(
    "/",
    response_model=TimetableResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Jadvalga dars qo'shish",
)
def create_entry(data: TimetableCreate, db: Session = Depends(get_db)):
    return timetable_service.create(db, data)


@router.put("/{entry_id}", response_model=TimetableResponse, summary="Jadval yozuvini yangilash")
def update_entry(entry_id: int, data: TimetableUpdate, db: Session = Depends(get_db)):
    return timetable_service.update(db, entry_id, data)


@router.delete("/{entry_id}", status_code=status.HTTP_200_OK, summary="Darsni o'chirish")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    return timetable_service.delete(db, entry_id)
