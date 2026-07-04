from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ============================================================
# TeacherCreate — yangi o'qituvchi QO'SHISHDA tekshiradi
# Frontend POST /teachers ga shu formatda yuborishi kerak
# ============================================================
class TeacherCreate(BaseModel):
    full_name:  str             # majburiy
    subject:    str             # majburiy
    email:      Optional[EmailStr] = None  # ixtiyoriy, email formatida


# ============================================================
# TeacherUpdate — o'qituvchini TAHRIRLASHDA tekshiradi
# Optional — har bir maydon ixtiyoriy (faqat o'zgarganini yuborsa bo'ladi)
# ============================================================
class TeacherUpdate(BaseModel):
    full_name:  Optional[str]       = None
    subject:    Optional[str]       = None
    email:      Optional[EmailStr]  = None
    is_active:  Optional[bool]      = None


# ============================================================
# TeacherResponse — o'qituvchi ma'lumotini QAYTARISHDA ishlatiladi
# DB dan kelgan ma'lumot shu formatda frontendga boradi
# ============================================================
class TeacherResponse(BaseModel):
    id:         int
    full_name:  str
    subject:    str
    email:      Optional[str]      = None
    is_active:  bool               = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}