"""HTTP routes for the modern COVIDash API."""

from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pymongo.errors import PyMongoError

from backend.app.core.db import MongoStore
from backend.app.services.dashboard import DashboardService

router = APIRouter(prefix="/api")


def get_service(request: Request) -> DashboardService:
    """Return a request-scoped dashboard service backed by the app Mongo store."""

    store: MongoStore = request.app.state.mongo_store
    return DashboardService(store.collections)


@router.get("/health")
def health(request: Request) -> dict[str, str]:
    """Return application and database health."""

    store: MongoStore = request.app.state.mongo_store
    try:
        store.ping()
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="MongoDB unavailable") from exc
    return {"status": "ok"}


@router.get("/config")
def config(service: Annotated[DashboardService, Depends(get_service)]) -> dict:
    """Return shared dashboard configuration for the frontend."""

    return service.config()


@router.get("/pandemic/{scope}")
def pandemic_snapshot(
    scope: Literal["national", "regional", "provincial"],
    service: Annotated[DashboardService, Depends(get_service)],
    area: Annotated[str | None, Query(description="Region or province name")] = None,
) -> dict:
    """Return a complete pandemic dashboard snapshot."""

    return service.pandemic_snapshot(scope=scope, area=area)


@router.get("/vaccines")
def vaccines_snapshot(
    service: Annotated[DashboardService, Depends(get_service)],
    area: Annotated[str | None, Query(description="Region name")] = None,
) -> dict:
    """Return a complete vaccine dashboard snapshot."""

    return service.vaccines_snapshot(area=area)


@router.get("/vax_charts/{chart_id}")
def vaccine_chart(
    chart_id: str,
    service: Annotated[DashboardService, Depends(get_service)],
    area: Annotated[str | None, Query(description="Optional region name")] = None,
) -> dict:
    """Return a legacy-compatible vaccine chart payload."""

    return service.vaccine_chart(chart_id=chart_id, area=area)
