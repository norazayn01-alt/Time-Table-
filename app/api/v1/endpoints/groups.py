from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.schemas.group import GroupCreate, GroupUpdate, GroupResponse
from app.services.group import group_service

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("/", response_model=List[GroupResponse], summary="Barcha guruhlar")
def list_groups(db: Session = Depends(get_db)):
    return group_service.get_all(db)


@router.get("/{group_id}", response_model=GroupResponse, summary="Bitta guruh")
def get_group(group_id: int, db: Session = Depends(get_db)):
    return group_service.get_or_404(db, group_id)


@router.post(
    "/",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yangi guruh qo'shish",
)
def create_group(data: GroupCreate, db: Session = Depends(get_db)):
    return group_service.create(db, data)


@router.put("/{group_id}", response_model=GroupResponse, summary="Guruhni yangilash")
def update_group(group_id: int, data: GroupUpdate, db: Session = Depends(get_db)):
    return group_service.update(db, group_id, data)


@router.delete("/{group_id}", status_code=status.HTTP_200_OK, summary="Guruhni o'chirish")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    return group_service.delete(db, group_id)
