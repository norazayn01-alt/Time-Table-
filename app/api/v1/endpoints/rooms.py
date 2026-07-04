from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse
from app.services.room import room_service

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=List[RoomResponse], summary="Barcha xonalar")
def list_rooms(db: Session = Depends(get_db)):
    return room_service.get_all(db)


@router.get("/{room_id}", response_model=RoomResponse, summary="Bitta xona")
def get_room(room_id: int, db: Session = Depends(get_db)):
    return room_service.get_or_404(db, room_id)


@router.post(
    "/",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yangi xona qo'shish",
)
def create_room(data: RoomCreate, db: Session = Depends(get_db)):
    return room_service.create(db, data)


@router.put("/{room_id}", response_model=RoomResponse, summary="Xonani yangilash")
def update_room(room_id: int, data: RoomUpdate, db: Session = Depends(get_db)):
    return room_service.update(db, room_id, data)


@router.delete("/{room_id}", status_code=status.HTTP_200_OK, summary="Xonani o'chirish")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    return room_service.delete(db, room_id)
