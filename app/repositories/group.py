from typing import Optional

from sqlalchemy.orm import Session

from app.models.group import Group
from app.repositories.base import BaseRepository


class GroupRepository(BaseRepository[Group]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Group]:
        return db.query(Group).filter(Group.name == name).first()


group_repo = GroupRepository(Group)
