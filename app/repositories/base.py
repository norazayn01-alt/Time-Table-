from typing import TypeVar, Generic, Type, Optional, List, Any

from sqlalchemy.orm import Session

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic CRUD repository — barcha modellar uchun asosiy operatsiyalar."""

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    def get(self, db: Session, *, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()  # type: ignore[attr-defined]

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 200
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: dict[str, Any]) -> ModelType:
        obj = self.model(**obj_in)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(
        self, db: Session, *, db_obj: ModelType, update_data: dict[str, Any]
    ) -> ModelType:
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[ModelType]:
        obj = self.get(db, id=id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
