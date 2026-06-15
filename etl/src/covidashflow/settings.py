"""Environment-driven ETL settings."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class EtlSettings:
    """Runtime settings for Prefect/PostgreSQL ETL runs."""

    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "postgresql+psycopg://covidash:covidash@postgres:5432/covidash"))
    prefect_api_url: str = field(default_factory=lambda: os.getenv("PREFECT_API_URL", "http://prefect-server:4200/api"))
