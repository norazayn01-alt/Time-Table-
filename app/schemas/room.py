from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class RoomBase(BaseModel):
    name:      str
    capacity:  int
    room_type: str = "dars"

    @field_validator("capacity")
    @classmethod
    def capacity_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Sig'im musbat son bo'lishi kerak")
        return v


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    name:      Optional[str]  = None
    capacity:  Optional[int]  = None
    room_type: Optional[str]  = None
    is_active: Optional[bool] = None


class RoomResponse(RoomBase):
    id:         int
    is_active:  bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
