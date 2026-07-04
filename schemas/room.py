from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RoomCreate(BaseModel):
    name:       str
    capacity:   int
    room_type:  Optional[str] = 'dars'


class RoomUpdate(BaseModel):
    name:       Optional[str]  = None
    capacity:   Optional[int]  = None
    room_type:  Optional[str]  = None
    is_active:  Optional[bool] = None


class RoomResponse(BaseModel):
    id:         int
    name:       str
    capacity:   int
    room_type:  str
    is_active:  bool               = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}