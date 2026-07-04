from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GroupCreate(BaseModel):
    name:           str
    student_count:  int
    course_year:    int
    specialization: Optional[str] = None


class GroupUpdate(BaseModel):
    name:           Optional[str]   = None
    student_count:  Optional[int]   = None
    course_year:    Optional[int]   = None
    specialization: Optional[str]   = None
    is_active:      Optional[bool]  = None


class GroupResponse(BaseModel):
    id:             int
    name:           str
    student_count:  int
    course_year:    int
    specialization: Optional[str]      = None
    is_active:      bool               = True
    created_at:     Optional[datetime] = None
    updated_at:     Optional[datetime] = None

    model_config = {"from_attributes": True}