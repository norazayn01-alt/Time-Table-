from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown lifecycle.
    
    Migratsiyalarni ishlatish:
        .venv/bin/alembic upgrade head
    """
    yield


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── API v1 ────────────────────────────────────────────────────────────────────
app.include_router(api_router)

# ── Frontend (static) — eng oxirida mount qilinadi ───────────────────────────
import os
_frontend_dir = "frontend/dist" if os.path.isdir("frontend/dist") else "frontend"
app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")