"""MongoDB connection helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from backend.app.core.settings import Settings, get_settings


@dataclass
class MongoCollections:
    """Named Mongo collections produced by covidashflow."""

    national_data: Collection[Any]
    national_trends: Collection[Any]
    national_series: Collection[Any]
    regional_data: Collection[Any]
    regional_trends: Collection[Any]
    regional_series: Collection[Any]
    regional_breakdown: Collection[Any]
    provincial_data: Collection[Any]
    provincial_trends: Collection[Any]
    provincial_series: Collection[Any]
    provincial_breakdown: Collection[Any]
    vax_admins: Collection[Any]
    vax_admins_summary: Collection[Any]
    population: Collection[Any]


class MongoStore:
    """Small wrapper around PyMongo with explicit collection names."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.client: MongoClient[Any] = MongoClient(
            self.settings.mongo_uri,
            serverSelectionTimeoutMS=self.settings.mongo_timeout_ms,
            connectTimeoutMS=self.settings.mongo_timeout_ms,
            socketTimeoutMS=self.settings.mongo_timeout_ms,
        )
        self.db: Database[Any] = self.client.get_default_database()
        self.collections = MongoCollections(
            national_data=self.db[self.settings.national_data_collection],
            national_trends=self.db[self.settings.national_trends_collection],
            national_series=self.db[self.settings.national_series_collection],
            regional_data=self.db[self.settings.regional_data_collection],
            regional_trends=self.db[self.settings.regional_trends_collection],
            regional_series=self.db[self.settings.regional_series_collection],
            regional_breakdown=self.db[self.settings.regional_breakdown_collection],
            provincial_data=self.db[self.settings.provincial_data_collection],
            provincial_trends=self.db[self.settings.provincial_trends_collection],
            provincial_series=self.db[self.settings.provincial_series_collection],
            provincial_breakdown=self.db[self.settings.provincial_breakdown_collection],
            vax_admins=self.db[self.settings.vax_admins_collection],
            vax_admins_summary=self.db[self.settings.vax_admins_summary_collection],
            population=self.db[self.settings.population_collection],
        )

    def ping(self) -> bool:
        """Return True when MongoDB responds to a ping command."""

        self.client.admin.command("ping")
        return True

    def close(self) -> None:
        """Close the underlying PyMongo client."""

        self.client.close()
