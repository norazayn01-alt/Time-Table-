from pydantic import BaseModel, model_validator, field_validator
from typing import Optional
from datetime import datetime, time


class TimetableBase(BaseModel):
    teacher_id:  int
    room_id:     int
    group_id:    int
    day_of_week: int      # 1=Dushanba … 6=Shanba
    start_time:  time
    end_time:    time
    subject:     str

    @field_validator("day_of_week")
    @classmethod
    def day_of_week_valid(cls, v: int) -> int:
        if not (1 <= v <= 6):
            raise ValueError("Hafta kuni 1 (Dushanba) dan 6 (Shanba) gacha bo'lishi kerak")
        return v

    @model_validator(mode="after")
    def end_after_start(self) -> "TimetableBase":
        if self.end_time <= self.start_time:
            raise ValueError("Tugash vaqti boshlanish vaqtidan keyin bo'lishi kerak")
        return self


class TimetableCreate(TimetableBase):
    pass


class TimetableUpdate(BaseModel):
    teacher_id:  Optional[int]  = None
    room_id:     Optional[int]  = None
    group_id:    Optional[int]  = None
    day_of_week: Optional[int]  = None
    start_time:  Optional[time] = None
    end_time:    Optional[time] = None
    subject:     Optional[str]  = None


class TimetableResponse(TimetableBase):
    id:         int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
