from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time


class TimetableCreate(BaseModel):
    teacher_id:     int
    room_id:        int
    group_id:       int
    day_of_week:    int         # 1=Dushanba ... 6=Shanba
    start_time:     time        # "08:00" formatida
    end_time:       time        # "09:30" formatida
    subject:        str


class TimetableUpdate(BaseModel):
    teacher_id:     Optional[int]   = None
    room_id:        Optional[int]   = None
    group_id:       Optional[int]   = None
    day_of_week:    Optional[int]   = None
    start_time:     Optional[time]  = None
    end_time:       Optional[time]  = None
    subject:        Optional[str]   = None


class TimetableResponse(BaseModel):
    id:             int
    teacher_id:     int
    room_id:        int
    group_id:       int
    day_of_week:    int
    start_time:     time
    end_time:       time
    subject:        str
    created_at:     Optional[datetime] = None
    updated_at:     Optional[datetime] = None

    model_config = {"from_attributes": True}