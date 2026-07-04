from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class GroupBase(BaseModel):
    name:           str
    student_count:  int
    course_year:    int
    specialization: Optional[str] = None

    @field_validator("student_count")
    @classmethod
    def student_count_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Talabalar soni musbat bo'lishi kerak")
        return v

    @field_validator("course_year")
    @classmethod
    def course_year_valid(cls, v: int) -> int:
        if not (1 <= v <= 6):
            raise ValueError("Kurs yili 1 dan 6 gacha bo'lishi kerak")
        return v


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name:           Optional[str]  = None
    student_count:  Optional[int]  = None
    course_year:    Optional[int]  = None
    specialization: Optional[str]  = None
    is_active:      Optional[bool] = None


class GroupResponse(GroupBase):
    id:         int
    is_active:  bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
