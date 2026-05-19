from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Resume Analyzer AI Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"

    BACKEND_DIR: Path = Path(__file__).resolve().parent
    UPLOAD_DIR: Path = BACKEND_DIR / "uploads"

    MAX_UPLOAD_SIZE_MB: int = 5
    ALLOWED_EXTENSIONS: list[str] = [".pdf", ".docx", ".txt"]

    CORS_ORIGINS: list[str] = [
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug_value(cls, value: object) -> bool:
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            normalized_value = value.strip().lower()

            if normalized_value in {"1", "true", "yes", "on", "debug"}:
                return True

            if normalized_value in {"0", "false", "no", "off", "release", "prod", "production"}:
                return False

        return bool(value)

    @property
    def max_upload_size_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    app_settings = Settings()
    app_settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return app_settings


settings = get_settings()
