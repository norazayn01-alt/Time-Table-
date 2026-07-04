from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class TeacherBase(BaseModel):
    full_name: str
    subject:   str
    email:     Optional[EmailStr] = None


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    full_name: Optional[str]       = None
    subject:   Optional[str]       = None
    email:     Optional[EmailStr]  = None
    is_active: Optional[bool]      = None


class TeacherResponse(TeacherBase):
    id:         int
    is_active:  bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
