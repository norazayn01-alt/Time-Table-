from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.timetable import Timetable
from models.teacher import Teacher
from models.room import Room
from models.group import Group
from schemas.timetable import TimetableCreate, TimetableUpdate, TimetableResponse

router = APIRouter(
    prefix="/timetable",
    tags=["Timetable"]
)


@router.get("/", response_model=List[TimetableResponse])
def get_timetable(db: Session = Depends(get_db)):
    return db.query(Timetable).all()


# Guruh bo'yicha jadval — masalan: CS-101 ning jadvali
@router.get("/group/{group_id}", response_model=List[TimetableResponse])
def get_group_timetable(group_id: int, db: Session = Depends(get_db)):
    entries = db.query(Timetable).filter(Timetable.group_id == group_id).all()
    if not entries:
        raise HTTPException(status_code=404, detail="Bu guruh uchun jadval topilmadi")
    return entries


# O'qituvchi bo'yicha jadval
@router.get("/teacher/{teacher_id}", response_model=List[TimetableResponse])
def get_teacher_timetable(teacher_id: int, db: Session = Depends(get_db)):
    entries = db.query(Timetable).filter(Timetable.teacher_id == teacher_id).all()
    if not entries:
        raise HTTPException(status_code=404, detail="Bu o'qituvchi uchun jadval topilmadi")
    return entries


@router.post("/", response_model=TimetableResponse)
def create_timetable(data: TimetableCreate, db: Session = Depends(get_db)):
    # Teacher, Room, Group mavjudligini tekshiramiz
    if not db.query(Teacher).filter(Teacher.id == data.teacher_id).first():
        raise HTTPException(status_code=404, detail="O'qituvchi topilmadi")
    if not db.query(Room).filter(Room.id == data.room_id).first():
        raise HTTPException(status_code=404, detail="Xona topilmadi")
    if not db.query(Group).filter(Group.id == data.group_id).first():
        raise HTTPException(status_code=404, detail="Guruh topilmadi")

    # Conflict tekshiruvi — xona bir vaqtda band bo'lmasligi kerak
    room_conflict = db.query(Timetable).filter(
        Timetable.room_id     == data.room_id,
        Timetable.day_of_week == data.day_of_week,
        Timetable.start_time  == data.start_time
    ).first()
    if room_conflict:
        raise HTTPException(status_code=400, detail="Bu xona bu vaqtda band!")

    # Guruh conflict
    group_conflict = db.query(Timetable).filter(
        Timetable.group_id    == data.group_id,
        Timetable.day_of_week == data.day_of_week,
        Timetable.start_time  == data.start_time
    ).first()
    if group_conflict:
        raise HTTPException(status_code=400, detail="Bu guruh bu vaqtda boshqa darsda!")

    # O'qituvchi conflict
    teacher_conflict = db.query(Timetable).filter(
        Timetable.teacher_id  == data.teacher_id,
        Timetable.day_of_week == data.day_of_week,
        Timetable.start_time  == data.start_time
    ).first()
    if teacher_conflict:
        raise HTTPException(status_code=400, detail="Bu o'qituvchi bu vaqtda boshqa darsda!")

    entry = Timetable(**data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.put("/{entry_id}", response_model=TimetableResponse)
def update_timetable(entry_id: int, data: TimetableUpdate, db: Session = Depends(get_db)):
    entry = db.query(Timetable).filter(Timetable.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Jadval yozuvi topilmadi")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(entry, key, value)

    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}")
def delete_timetable(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(Timetable).filter(Timetable.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Jadval yozuvi topilmadi")

    db.delete(entry)
    db.commit()
    return {"message": "Jadval yozuvi o'chirildi"}