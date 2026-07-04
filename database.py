from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/timetable"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,  # O'zgarishlar avtomatik saqlanmasin
    autoflush=False,   # Avtomatik yuborilmasin
    bind=engine        # Yuqoridagi engine ga bog'laymiz
)


class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()