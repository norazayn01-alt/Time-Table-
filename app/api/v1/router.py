from fastapi import APIRouter

from app.api.v1.endpoints import teachers, rooms, groups, timetable

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(teachers.router)
api_router.include_router(rooms.router)
api_router.include_router(groups.router)
api_router.include_router(timetable.router)
