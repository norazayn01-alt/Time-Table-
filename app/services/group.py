from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.group import Group
from app.repositories.group import group_repo
from app.schemas.group import GroupCreate, GroupUpdate


class GroupService:

    def get_all(self, db: Session) -> List[Group]:
        return group_repo.get_multi(db)

    def get_or_404(self, db: Session, group_id: int) -> Group:
        group = group_repo.get(db, id=group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Guruh topilmadi",
            )
        return group

    def create(self, db: Session, data: GroupCreate) -> Group:
        if group_repo.get_by_name(db, name=data.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bu nomli guruh allaqachon mavjud",
            )
        return group_repo.create(db, obj_in=data.model_dump())

    def update(self, db: Session, group_id: int, data: GroupUpdate) -> Group:
        group = self.get_or_404(db, group_id)
        update_data = data.model_dump(exclude_unset=True)
        if "name" in update_data:
            conflict = group_repo.get_by_name(db, name=update_data["name"])
            if conflict and conflict.id != group_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Bu nomli guruh allaqachon mavjud",
                )
        return group_repo.update(db, db_obj=group, update_data=update_data)

    def delete(self, db: Session, group_id: int) -> dict:
        group = self.get_or_404(db, group_id)
        group_repo.delete(db, id=group_id)
        return {"message": f"'{group.name}' guruhi o'chirildi"}


group_service = GroupService()
