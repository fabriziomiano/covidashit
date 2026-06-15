"""Runtime settings for the FastAPI application."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    """Environment-driven application settings.

    Collection names intentionally match the historical dashboard and the
    covidashflow output collections, preserving the existing data contract.
    """

    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/covid")
    cors_origins: tuple[str, ...] = tuple(
        origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if origin.strip()
    )
    app_host: str = os.getenv("HOST", "0.0.0.0")
    app_port: int = int(os.getenv("PORT", "5050"))
    frontend_dist: str = os.getenv("FRONTEND_DIST", "frontend/dist")
    national_data_collection: str = os.getenv("NATIONAL_DATA_COLLECTION", "National")
    national_trends_collection: str = os.getenv("NATIONAL_TRENDS_COLLECTION", "NationalTrends")
    national_series_collection: str = os.getenv("NATIONAL_SERIES_COLLECTION", "NationalSeries")
    regional_data_collection: str = os.getenv("REGIONAL_DATA_COLLECTION", "Regional")
    regional_trends_collection: str = os.getenv("REGIONAL_TRENDS_COLLECTION", "RegionalTrends")
    regional_series_collection: str = os.getenv("REGIONAL_SERIES_COLLECTION", "RegionalSeries")
    regional_breakdown_collection: str = os.getenv("REGIONAL_BREAKDOWN_COLLECTION", "RegionalBreakdown")
    provincial_data_collection: str = os.getenv("PROVINCIAL_DATA_COLLECTION", "Provincial")
    provincial_trends_collection: str = os.getenv("PROVINCIAL_TRENDS_COLLECTION", "ProvincialTrends")
    provincial_series_collection: str = os.getenv("PROVINCIAL_SERIES_COLLECTION", "ProvincialSeries")
    provincial_breakdown_collection: str = os.getenv("PROVINCIAL_BREAKDOWN_COLLECTION", "ProvincialBreakdown")
    vax_admins_collection: str = os.getenv("VAX_ADMINS_COLLECTION", "VaxAdmins")
    vax_admins_summary_collection: str = os.getenv("VAX_ADMINS_SUMMARY_COLLECTION", "VaxAdminsSummary")
    population_collection: str = os.getenv("POP_COLLECTION", "Population")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings read from the current process environment."""

    return Settings()
