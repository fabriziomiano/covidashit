"""Postgres warehouse storage for COVIDash ETL outputs."""

from __future__ import annotations

import datetime as dt
import math
import os
from collections.abc import Iterable
from typing import Any

import pandas as pd
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Index, MetaData, Table, Text, UniqueConstraint, create_engine, delete, func, insert, select, text, update
from sqlalchemy.dialects.postgresql import JSONB, insert as pg_insert
from sqlalchemy.engine import Engine

from covidashflow.common.vars import DATE_KEY, PROVINCE_KEY, REGION_KEY, VAX_AGE_KEY, VAX_AREA_KEY, VAX_DATE_KEY, VAX_PROVIDER_KEY

DEFAULT_DATABASE_URL = "postgresql+psycopg://covidash:covidash@postgres:5432/covidash"

metadata = MetaData()

pandemic_daily = Table(
    "fact_pandemic_daily",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("scope", Text, nullable=False),
    Column("area", Text),
    Column("region", Text),
    Column("province", Text),
    Column("data", DateTime(timezone=True), nullable=False),
    Column("payload", JSONB, nullable=False),
    UniqueConstraint("scope", "area", "data", name="uq_fact_pandemic_daily_scope_area_data"),
    Index("ix_fact_pandemic_daily_scope_area_data", "scope", "area", "data"),
    Index("ix_fact_pandemic_daily_region", "region"),
    Index("ix_fact_pandemic_daily_province", "province"),
)

dashboard_artifacts = Table(
    "dashboard_artifacts",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("artifact_type", Text, nullable=False),
    Column("scope", Text),
    Column("area", Text),
    Column("sort_order", BigInteger, nullable=False, default=0),
    Column("payload", JSONB, nullable=False),
    Index("ix_dashboard_artifacts_lookup", "artifact_type", "scope", "area", "sort_order"),
)

population_age = Table(
    "fact_population_age",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("area_code", Text, nullable=False),
    Column("area", Text, nullable=False),
    Column("age_band", Text, nullable=False),
    Column("population", BigInteger, nullable=False),
    Column("payload", JSONB, nullable=False),
    UniqueConstraint("area_code", "age_band", name="uq_fact_population_age_area_age"),
    Index("ix_fact_population_age_area", "area"),
)

vaccine_admin_daily = Table(
    "fact_vaccine_admin_daily",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("data", DateTime(timezone=True), nullable=False),
    Column("area_code", Text, nullable=False),
    Column("area", Text, nullable=False),
    Column("age_band", Text),
    Column("provider", Text),
    Column("first_dose", BigInteger, nullable=False, default=0),
    Column("second_dose", BigInteger, nullable=False, default=0),
    Column("booster_dose", BigInteger, nullable=False, default=0),
    Column("total_admins", BigInteger, nullable=False, default=0),
    Column("payload", JSONB, nullable=False),
    UniqueConstraint("data", "area_code", "age_band", "provider", name="uq_fact_vaccine_admin_daily_natural"),
    Index("ix_fact_vaccine_admin_daily_area_data", "area_code", "data"),
    Index("ix_fact_vaccine_admin_daily_provider", "provider"),
    Index("ix_fact_vaccine_admin_daily_age", "age_band"),
)

vaccine_summary_daily = Table(
    "fact_vaccine_summary_daily",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("data", DateTime(timezone=True), nullable=False),
    Column("area_code", Text, nullable=False),
    Column("area", Text, nullable=False),
    Column("first_dose", BigInteger, nullable=False, default=0),
    Column("second_dose", BigInteger, nullable=False, default=0),
    Column("booster_dose", BigInteger, nullable=False, default=0),
    Column("delivered_doses", BigInteger, nullable=False, default=0),
    Column("total_admins", BigInteger, nullable=False, default=0),
    Column("population", BigInteger, nullable=False, default=0),
    Column("payload", JSONB, nullable=False),
    UniqueConstraint("area_code", "data", name="uq_fact_vaccine_summary_daily_area_data"),
    Index("ix_fact_vaccine_summary_daily_area_data", "area_code", "data"),
)

etl_run_log = Table(
    "etl_run_log",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("run_id", Text, nullable=False, unique=True),
    Column("pipeline", Text, nullable=False),
    Column("load_mode", Text, nullable=False),
    Column("status", Text, nullable=False),
    Column("started_at", DateTime(timezone=True), nullable=False),
    Column("finished_at", DateTime(timezone=True)),
    Column("rows_loaded", BigInteger, nullable=False, default=0),
    Column("skipped", Boolean, nullable=False, default=False),
    Column("message", Text),
    Index("ix_etl_run_log_pipeline_started", "pipeline", "started_at"),
)

# Kept only for fallback inspection during migration; production SQL mode does not read it.
documents = Table(
    "covidash_documents",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("collection_name", Text, nullable=False),
    Column("sort_order", BigInteger, nullable=False),
    Column("document", JSONB, nullable=False),
    Column("data", DateTime(timezone=True)),
    Column("area", Text),
    Column("region", Text),
    Column("province", Text),
    Index("ix_covidash_documents_collection_sort", "collection_name", "sort_order"),
)


def database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def get_engine(url: str | None = None) -> Engine:
    return create_engine(url or database_url(), future=True)


def ensure_schema(engine: Engine) -> None:
    metadata.create_all(engine)


def wait_for_database(engine: Engine) -> None:
    with engine.connect() as conn:
        conn.execute(text("select 1"))


def run_was_recorded(engine: Engine, run_id: str) -> bool:
    with engine.connect() as conn:
        return conn.execute(select(etl_run_log.c.id).where(etl_run_log.c.run_id == run_id)).first() is not None


def start_run(engine: Engine, run_id: str, pipeline: str, load_mode: str) -> bool:
    with engine.begin() as conn:
        metadata.create_all(conn)
        if conn.execute(select(etl_run_log.c.id).where(etl_run_log.c.run_id == run_id)).first() is not None:
            return False
        conn.execute(insert(etl_run_log).values(
            run_id=run_id,
            pipeline=pipeline,
            load_mode=load_mode,
            status="running",
            started_at=dt.datetime.now(dt.UTC),
            rows_loaded=0,
            skipped=False,
        ))
    return True


def finish_run(engine: Engine, run_id: str, status: str, rows_loaded: int = 0, message: str | None = None, skipped: bool = False) -> None:
    with engine.begin() as conn:
        conn.execute(
            update(etl_run_log)
            .where(etl_run_log.c.run_id == run_id)
            .values(
                status=status,
                finished_at=dt.datetime.now(dt.UTC),
                rows_loaded=rows_loaded,
                message=message,
                skipped=skipped,
            )
        )


def latest_pandemic_date(engine: Engine, scope: str) -> dt.datetime | None:
    with engine.connect() as conn:
        return conn.execute(select(func.max(pandemic_daily.c.data)).where(pandemic_daily.c.scope == scope)).scalar_one_or_none()


def latest_vaccine_admin_date(engine: Engine) -> dt.datetime | None:
    with engine.connect() as conn:
        return conn.execute(select(func.max(vaccine_admin_daily.c.data))).scalar_one_or_none()


def latest_vaccine_summary_date(engine: Engine) -> dt.datetime | None:
    with engine.connect() as conn:
        return conn.execute(select(func.max(vaccine_summary_daily.c.data))).scalar_one_or_none()


def replace_pandemic_daily(engine: Engine, scope: str, records: Iterable[dict[str, Any]]) -> int:
    rows = [_pandemic_row(scope, record) for record in records]
    with engine.begin() as conn:
        metadata.create_all(conn)
        conn.execute(delete(pandemic_daily).where(pandemic_daily.c.scope == scope))
        if rows:
            conn.execute(insert(pandemic_daily), rows)
    return len(rows)


def append_pandemic_daily(engine: Engine, scope: str, records: Iterable[dict[str, Any]]) -> int:
    rows = [_pandemic_row(scope, record) for record in records]
    if not rows:
        return 0
    stmt = pg_insert(pandemic_daily).values(rows).on_conflict_do_nothing(
        constraint="uq_fact_pandemic_daily_scope_area_data"
    )
    with engine.begin() as conn:
        metadata.create_all(conn)
        result = conn.execute(stmt)
    return int(result.rowcount or 0)


def replace_artifacts(engine: Engine, artifact_type: str, scope: str | None, records: Iterable[dict[str, Any]]) -> int:
    rows = [
        {
            "artifact_type": artifact_type,
            "scope": scope,
            "area": record.get("area"),
            "sort_order": index,
            "payload": _json_safe(record.get("payload", record)),
        }
        for index, record in enumerate(records)
    ]
    with engine.begin() as conn:
        metadata.create_all(conn)
        conn.execute(delete(dashboard_artifacts).where(dashboard_artifacts.c.artifact_type == artifact_type).where(dashboard_artifacts.c.scope == scope))
        if rows:
            conn.execute(insert(dashboard_artifacts), rows)
    return len(rows)


def replace_population(engine: Engine, records: Iterable[dict[str, Any]], area_names: dict[str, str]) -> int:
    rows = []
    for record in records:
        area_code = str(record.get(VAX_AREA_KEY))
        rows.append({
            "area_code": area_code,
            "area": area_names.get(area_code, area_code),
            "age_band": str(record.get(VAX_AGE_KEY)),
            "population": _int(record.get("totale_popolazione")),
            "payload": _json_safe(record),
        })
    with engine.begin() as conn:
        metadata.create_all(conn)
        conn.execute(delete(population_age))
        if rows:
            conn.execute(insert(population_age), rows)
    return len(rows)


def replace_vaccine_admins(engine: Engine, records: Iterable[dict[str, Any]], area_names: dict[str, str]) -> int:
    rows = []
    for record in records:
        area_code = str(record.get(VAX_AREA_KEY))
        rows.append({
            "data": _date_value(record, VAX_DATE_KEY),
            "area_code": area_code,
            "area": area_names.get(area_code, area_code),
            "age_band": record.get(VAX_AGE_KEY),
            "provider": record.get(VAX_PROVIDER_KEY),
            "first_dose": _int(record.get("d1")),
            "second_dose": _int(record.get("d2")),
            "booster_dose": _int(record.get("db1")),
            "total_admins": _int(record.get("totale")),
            "payload": _json_safe(record),
        })
    with engine.begin() as conn:
        metadata.create_all(conn)
        conn.execute(delete(vaccine_admin_daily))
        if rows:
            conn.execute(insert(vaccine_admin_daily), rows)
    return len(rows)


def append_vaccine_admins(engine: Engine, records: Iterable[dict[str, Any]], area_names: dict[str, str]) -> int:
    rows = []
    for record in records:
        area_code = str(record.get(VAX_AREA_KEY))
        rows.append({
            "data": _date_value(record, VAX_DATE_KEY),
            "area_code": area_code,
            "area": area_names.get(area_code, area_code),
            "age_band": record.get(VAX_AGE_KEY),
            "provider": record.get(VAX_PROVIDER_KEY),
            "first_dose": _int(record.get("d1")),
            "second_dose": _int(record.get("d2")),
            "booster_dose": _int(record.get("db1")),
            "total_admins": _int(record.get("totale")),
            "payload": _json_safe(record),
        })
    if not rows:
        return 0
    stmt = pg_insert(vaccine_admin_daily).values(rows).on_conflict_do_nothing(
        constraint="uq_fact_vaccine_admin_daily_natural"
    )
    with engine.begin() as conn:
        metadata.create_all(conn)
        result = conn.execute(stmt)
    return int(result.rowcount or 0)


def replace_vaccine_summary(engine: Engine, records: Iterable[dict[str, Any]], area_names: dict[str, str]) -> int:
    rows = []
    for record in records:
        area_code = str(record.get(VAX_AREA_KEY))
        rows.append({
            "data": _date_value(record, VAX_DATE_KEY),
            "area_code": area_code,
            "area": area_names.get(area_code, area_code),
            "first_dose": _int(record.get("d1")),
            "second_dose": _int(record.get("d2")),
            "booster_dose": _int(record.get("db1")),
            "delivered_doses": _int(record.get("dosi_consegnate")),
            "total_admins": _int(record.get("totale")),
            "population": _int(record.get("popolazione")),
            "payload": _json_safe(record),
        })
    with engine.begin() as conn:
        metadata.create_all(conn)
        conn.execute(delete(vaccine_summary_daily))
        if rows:
            conn.execute(insert(vaccine_summary_daily), rows)
    return len(rows)


def append_vaccine_summary(engine: Engine, records: Iterable[dict[str, Any]], area_names: dict[str, str]) -> int:
    rows = []
    for record in records:
        area_code = str(record.get(VAX_AREA_KEY))
        rows.append({
            "data": _date_value(record, VAX_DATE_KEY),
            "area_code": area_code,
            "area": area_names.get(area_code, area_code),
            "first_dose": _int(record.get("d1")),
            "second_dose": _int(record.get("d2")),
            "booster_dose": _int(record.get("db1")),
            "delivered_doses": _int(record.get("dosi_consegnate")),
            "total_admins": _int(record.get("totale")),
            "population": _int(record.get("popolazione")),
            "payload": _json_safe(record),
        })
    if not rows:
        return 0
    stmt = pg_insert(vaccine_summary_daily).values(rows).on_conflict_do_nothing(
        constraint="uq_fact_vaccine_summary_daily_area_data"
    )
    with engine.begin() as conn:
        metadata.create_all(conn)
        result = conn.execute(stmt)
    return int(result.rowcount or 0)


def replace_collection(engine: Engine, collection_name: str, records: Iterable[dict[str, Any]]) -> int:
    rows = [_document_row(collection_name, record, index) for index, record in enumerate(records)]
    with engine.begin() as conn:
        metadata.create_all(conn)
        conn.execute(delete(documents).where(documents.c.collection_name == collection_name))
        if rows:
            conn.execute(insert(documents), rows)
    return len(rows)


def replace_one(engine: Engine, collection_name: str, record: dict[str, Any]) -> int:
    return replace_collection(engine, collection_name, [record])


def _pandemic_row(scope: str, document: dict[str, Any]) -> dict[str, Any]:
    province = document.get(PROVINCE_KEY)
    region = document.get(REGION_KEY)
    area = f"{region}::{province}" if scope == "provincial" and province else region or "Italia"
    return {
        "scope": scope,
        "area": area,
        "region": region,
        "province": province,
        "data": _date_value(document, DATE_KEY),
        "payload": _json_safe(document),
    }


def _document_row(collection_name: str, document: dict[str, Any], sort_order: int) -> dict[str, Any]:
    return {
        "collection_name": collection_name,
        "sort_order": sort_order,
        "document": _json_safe(document),
        "data": _date_value(document, DATE_KEY) or _date_value(document, VAX_DATE_KEY),
        "area": document.get(REGION_KEY) or document.get(PROVINCE_KEY) or document.get(VAX_AREA_KEY),
        "region": document.get(REGION_KEY),
        "province": document.get(PROVINCE_KEY),
    }


def _date_value(document: dict[str, Any], key: str) -> dt.datetime | None:
    value = document.get(key)
    if isinstance(value, dt.datetime):
        return value
    if isinstance(value, dt.date):
        return dt.datetime.combine(value, dt.time.min)
    if isinstance(value, str):
        try:
            return dt.datetime.fromisoformat(value)
        except ValueError:
            return None
    return None


def _int(value: Any) -> int:
    try:
        return int(float(value or 0))
    except (TypeError, ValueError):
        return 0


def _json_safe(value: Any) -> Any:
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, (dt.datetime, dt.date)):
        return value.isoformat()
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if value is pd.NA:
        return None
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if hasattr(value, "item"):
        try:
            return _json_safe(value.item())
        except Exception:
            return value
    return value
