"""Runtime settings for the FastAPI application."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache


def _cors_origins() -> tuple[str, ...]:
    """Read comma-separated CORS origins from the current environment."""

    return tuple(origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if origin.strip())


@dataclass(frozen=True)
class Settings:
    """Environment-driven application settings for the SQL-backed dashboard."""

    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "postgresql+psycopg://covidash:covidash@localhost:5433/covidash"))
    cors_origins: tuple[str, ...] = field(default_factory=_cors_origins)
    app_host: str = field(default_factory=lambda: os.getenv("HOST", "0.0.0.0"))
    app_port: int = field(default_factory=lambda: int(os.getenv("PORT", os.getenv("COVIDASHIT_PORT", "5050"))))
    frontend_dist: str = field(default_factory=lambda: os.getenv("FRONTEND_DIST", "frontend/dist"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings read from the current process environment."""

    return Settings()
