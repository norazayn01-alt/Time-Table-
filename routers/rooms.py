from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.room import Room
from schemas.room import RoomCreate, RoomUpdate, RoomResponse

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.get("/", response_model=List[RoomResponse])
def get_all_rooms(db: Session = Depends(get_db)):
    rooms = db.query(Room).all()
    return rooms


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Xona topilmadi")
    return room


@router.post("/", response_model=RoomResponse)
def create_room(data: RoomCreate, db: Session = Depends(get_db)):
    # Bir xil nomli xona borligini tekshiramiz
    existing = db.query(Room).filter(Room.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu nomli xona allaqachon mavjud")

    room = Room(**data.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(room_id: int, data: RoomUpdate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Xona topilmadi")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(room, key, value)

    db.commit()
    db.refresh(room)
    return room


@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Xona topilmadi")

    db.delete(room)
    db.commit()
    return {"message": f"'{room.name}' xonasi o'chirildi"}