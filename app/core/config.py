from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:admin@localhost:5432/timetable"

    # App
    APP_TITLE: str = "Timetable API"
    APP_DESCRIPTION: str = "Dars jadvali boshqaruv tizimi"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
