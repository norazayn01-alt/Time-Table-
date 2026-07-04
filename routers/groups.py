from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.group import Group
from schemas.group import GroupCreate, GroupUpdate, GroupResponse

router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)


@router.get("/", response_model=List[GroupResponse])
def get_all_groups(db: Session = Depends(get_db)):
    groups = db.query(Group).all()
    return groups


@router.get("/{group_id}", response_model=GroupResponse)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Guruh topilmadi")
    return group


@router.post("/", response_model=GroupResponse)
def create_group(data: GroupCreate, db: Session = Depends(get_db)):
    existing = db.query(Group).filter(Group.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu nomli guruh allaqachon mavjud")

    group = Group(**data.model_dump())
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


@router.put("/{group_id}", response_model=GroupResponse)
def update_group(group_id: int, data: GroupUpdate, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Guruh topilmadi")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(group, key, value)

    db.commit()
    db.refresh(group)
    return group


@router.delete("/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Guruh topilmadi")

    db.delete(group)
    db.commit()
    return {"message": f"'{group.name}' guruhi o'chirildi"}