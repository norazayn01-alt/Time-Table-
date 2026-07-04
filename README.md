# TimeTable — Dars Jadvali Boshqaruv Tizimi

## Arxitektura

```
app/
├── core/           # Config, database, DI dependencies
├── models/         # SQLAlchemy ORM modellari
├── schemas/        # Pydantic v2 schema (request/response)
├── repositories/   # Data access layer (generic CRUD + query)
├── services/       # Business logic (validation, conflict check)
└── api/v1/         # FastAPI routers (HTTP layer)
    └── endpoints/

alembic/            # DB migratsiyalari
├── versions/
│   └── 0001_initial.py
└── env.py

frontend/           # Single-page UI (vanilla JS)
main.py             # FastAPI app entry point
.env                # Environment variables
requirements.txt
```

## O'rnatish

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Migratsiya (Alembic)

```bash
# Jadvallarni yaratish (birinchi marta)
.venv/bin/python3 -m alembic upgrade head

# Yangi migratsiya yaratish (model o'zgarganda)
.venv/bin/python3 -m alembic revision --autogenerate -m "describe change"

# Migratsiya holatini ko'rish
.venv/bin/python3 -m alembic current
.venv/bin/python3 -m alembic history
```

## Serverni ishga tushirish

```bash
.venv/bin/python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API

- Swagger UI: http://localhost:8000/api/docs
- ReDoc:       http://localhost:8000/api/redoc
- Frontend:    http://localhost:8000/

## .env sozlamalari

```env
DATABASE_URL=postgresql://postgres:admin@localhost:5432/timetable
DEBUG=True
APP_TITLE=Timetable API
APP_VERSION=2.0.0
```

## Qatlamlar (Layers)

| Qatlam | Vazifa |
|--------|--------|
| `api/v1/endpoints/` | HTTP so'rovlarni qabul qilish, schema validatsiya |
| `services/` | Biznes logika (conflict tekshiruvi, unique validatsiya) |
| `repositories/` | Faqat DB bilan ishlash (CRUD operatsiyalari) |
| `models/` | DB jadval tartibi (SQLAlchemy) |
| `schemas/` | Request/Response formatlari (Pydantic v2) |
| `core/` | Config, DB ulanish, dependency injection |
