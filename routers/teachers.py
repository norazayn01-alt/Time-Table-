from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.teacher import Teacher
from schemas.teacher import TeacherCreate, TeacherUpdate, TeacherResponse

# ============================================================
# APIRouter — bu fayl o'z route larini shu orqali belgilaydi
# prefix = barcha endpoint lar /teachers dan boshlanadi
# tags = Swagger docs da guruhlab ko'rsatadi
# ============================================================
router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)


# ============================================================
# GET /teachers — barcha o'qituvchilarni olish
# response_model = qaytariladigan ma'lumot formati
# ============================================================
@router.get("/", response_model=List[TeacherResponse])
def get_all_teachers(db: Session = Depends(get_db)):
    # db.query(Teacher) = SELECT * FROM teachers
    teachers = db.query(Teacher).all()
    return teachers


# ============================================================
# GET /teachers/1 — bitta o'qituvchini ID si bilan olish
# {teacher_id} = URL dan olinadi, masalan: /teachers/1
# ============================================================
@router.get("/{teacher_id}", response_model=TeacherResponse)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    # .filter() = WHERE teacher.id = teacher_id
    # .first() = birinchi natijani qaytaradi
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()

    # Topilmasa 404 xato qaytaramiz
    if not teacher:
        raise HTTPException(status_code=404, detail="O'qituvchi topilmadi")

    return teacher


# ============================================================
# POST /teachers — yangi o'qituvchi qo'shish
# data: TeacherCreate = Schema tekshirgan ma'lumot
# ============================================================
@router.post("/", response_model=TeacherResponse)
def create_teacher(data: TeacherCreate, db: Session = Depends(get_db)):
    # Email takrorlanmasligini tekshiramiz
    if data.email:
        existing = db.query(Teacher).filter(Teacher.email == data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Bu email allaqachon mavjud")

    # Yangi Teacher obyekti yaratamiz
    # **data.model_dump() = schemadagi barcha maydonlarni Teacher ga uzatadi
    teacher = Teacher(**data.model_dump())

    # DB ga qo'shamiz
    db.add(teacher)

    # O'zgarishlarni saqlaymiz
    db.commit()

    # DB dagi yangi holatni olamiz (id va created_at ni olish uchun)
    db.refresh(teacher)

    return teacher


# ============================================================
# PUT /teachers/1 — o'qituvchini yangilash
# ============================================================
@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher(teacher_id: int, data: TeacherUpdate, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()

    if not teacher:
        raise HTTPException(status_code=404, detail="O'qituvchi topilmadi")

    # Faqat yuborilgan maydonlarni yangilaymiz
    # exclude_unset=True = faqat o'zgartirilgan maydonlar
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(teacher, key, value)

    db.commit()
    db.refresh(teacher)
    return teacher


# ============================================================
# DELETE /teachers/1 — o'qituvchini o'chirish
# CASCADE — uning timetable lari ham o'chadi (DB da belgilangan)
# ============================================================
@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()

    if not teacher:
        raise HTTPException(status_code=404, detail="O'qituvchi topilmadi")

    db.delete(teacher)
    db.commit()

    return {"message": f"O'qituvchi '{teacher.full_name}' o'chirildi"}