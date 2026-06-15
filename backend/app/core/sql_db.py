"""SQL-first dashboard data access over the COVIDash Postgres warehouse."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Any, Iterable

from sqlalchemy import BigInteger, Column, DateTime, Index, MetaData, Table, Text, and_, create_engine, func, select, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine

from backend.app.core.constants import (
    OD_POP_KEY,
    PROVINCE_KEY,
    REGION_KEY,
    VAX_AGE_KEY,
    VAX_AREA_KEY,
    VAX_BOOSTER_DOSE_KEY,
    VAX_DATE_KEY,
    VAX_FIRST_DOSE_KEY,
    VAX_POP_KEY,
    VAX_PROVIDER_KEY,
    VAX_SECOND_DOSE_KEY,
    VAX_TOT_ADMINS_KEY,
)
from backend.app.core.settings import Settings, get_settings

metadata = MetaData()

pandemic_daily = Table(
    "fact_pandemic_daily",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("scope", Text, nullable=False),
    Column("area", Text),
    Column("region", Text),
    Column("province", Text),
    Column("data", DateTime(timezone=True), nullable=False),
    Column("payload", JSONB, nullable=False),
)

dashboard_artifacts = Table(
    "dashboard_artifacts",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("artifact_type", Text, nullable=False),
    Column("scope", Text),
    Column("area", Text),
    Column("sort_order", BigInteger, nullable=False),
    Column("payload", JSONB, nullable=False),
)

population_age = Table(
    "fact_population_age",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("area_code", Text, nullable=False),
    Column("area", Text, nullable=False),
    Column("age_band", Text, nullable=False),
    Column("population", BigInteger, nullable=False),
    Column("payload", JSONB, nullable=False),
)

vaccine_admin_daily = Table(
    "fact_vaccine_admin_daily",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("data", DateTime(timezone=True), nullable=False),
    Column("area_code", Text, nullable=False),
    Column("area", Text, nullable=False),
    Column("age_band", Text),
    Column("provider", Text),
    Column("first_dose", BigInteger, nullable=False),
    Column("second_dose", BigInteger, nullable=False),
    Column("booster_dose", BigInteger, nullable=False),
    Column("total_admins", BigInteger, nullable=False),
    Column("payload", JSONB, nullable=False),
)

vaccine_summary_daily = Table(
    "fact_vaccine_summary_daily",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("data", DateTime(timezone=True), nullable=False),
    Column("area_code", Text, nullable=False),
    Column("area", Text, nullable=False),
    Column("first_dose", BigInteger, nullable=False),
    Column("second_dose", BigInteger, nullable=False),
    Column("booster_dose", BigInteger, nullable=False),
    Column("delivered_doses", BigInteger, nullable=False),
    Column("total_admins", BigInteger, nullable=False),
    Column("population", BigInteger, nullable=False),
    Column("payload", JSONB, nullable=False),
)


@dataclass
class SqlCollections:
    national_data: "SqlCollection"
    national_trends: "SqlCollection"
    national_series: "SqlCollection"
    regional_data: "SqlCollection"
    regional_trends: "SqlCollection"
    regional_series: "SqlCollection"
    regional_breakdown: "SqlCollection"
    provincial_data: "SqlCollection"
    provincial_trends: "SqlCollection"
    provincial_series: "SqlCollection"
    provincial_breakdown: "SqlCollection"
    vax_admins: "SqlCollection"
    vax_admins_summary: "SqlCollection"
    population: "SqlCollection"


class SqlDashboardStore:
    """Postgres warehouse store exposing the dashboard collection contract."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.engine = create_engine(self.settings.database_url, future=True)
        self.collections = SqlCollections(
            national_data=SqlCollection(self.engine, "pandemic", scope="national"),
            national_trends=SqlCollection(self.engine, "artifact", artifact_type="pandemic_trends", scope="national", flatten_trends=True),
            national_series=SqlCollection(self.engine, "artifact", artifact_type="unused", scope="national"),
            regional_data=SqlCollection(self.engine, "pandemic", scope="regional"),
            regional_trends=SqlCollection(self.engine, "artifact", artifact_type="pandemic_trends", scope="regional", wrap_trends=True),
            regional_series=SqlCollection(self.engine, "artifact", artifact_type="unused", scope="regional"),
            regional_breakdown=SqlCollection(self.engine, "artifact", artifact_type="pandemic_breakdown", scope="national"),
            provincial_data=SqlCollection(self.engine, "pandemic", scope="provincial"),
            provincial_trends=SqlCollection(self.engine, "artifact", artifact_type="pandemic_trends", scope="provincial", wrap_trends=True),
            provincial_series=SqlCollection(self.engine, "artifact", artifact_type="unused", scope="provincial"),
            provincial_breakdown=SqlCollection(self.engine, "artifact", artifact_type="pandemic_breakdown", scope="regional", wrap_breakdown=True),
            vax_admins=SqlCollection(self.engine, "vaccine_admins"),
            vax_admins_summary=SqlCollection(self.engine, "vaccine_summary"),
            population=SqlCollection(self.engine, "population"),
        )

    def ping(self) -> bool:
        with self.engine.connect() as conn:
            conn.execute(text("select 1"))
        return True

    def close(self) -> None:
        self.engine.dispose()


class SqlCursor:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows
        self._index = 0

    def sort(self, key: str, direction: int) -> "SqlCursor":
        self.rows.sort(key=lambda row: _sort_value(row.get(key)), reverse=direction < 0)
        self._index = 0
        return self

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self.rows):
            raise StopIteration
        row = self.rows[self._index]
        self._index += 1
        return row


class SqlCollection:
    def __init__(
        self,
        engine: Engine,
        kind: str,
        scope: str | None = None,
        artifact_type: str | None = None,
        flatten_trends: bool = False,
        wrap_trends: bool = False,
        wrap_breakdown: bool = False,
    ) -> None:
        self.engine = engine
        self.kind = kind
        self.scope = scope
        self.artifact_type = artifact_type
        self.flatten_trends = flatten_trends
        self.wrap_trends = wrap_trends
        self.wrap_breakdown = wrap_breakdown

    def find(self, query: dict[str, Any] | None = None, projection: dict[str, Any] | None = None) -> SqlCursor:
        return SqlCursor(self._load(query or {}, projection))

    def find_one(
        self,
        query: dict[str, Any] | None = None,
        projection: dict[str, Any] | None = None,
        sort: list[tuple[str, int]] | None = None,
    ) -> dict[str, Any] | None:
        row = self._find_one_sql(query or {}, sort)
        if row is not None:
            return _project(row, projection) if projection else row
        rows = self._load(query or {}, projection)
        if sort:
            key, direction = sort[0]
            rows.sort(key=lambda row: _sort_value(row.get(key)), reverse=direction < 0)
        return rows[0] if rows else None

    def aggregate(self, pipeline: list[dict[str, Any]]) -> Iterable[dict[str, Any]]:
        sql_rows = self._aggregate_sql(pipeline)
        if sql_rows is not None:
            return iter(sql_rows)

        rows = self._load(_match_from_pipeline(pipeline), None)
        group_stage = next((stage["$group"] for stage in pipeline if "$group" in stage), None)
        if group_stage is None:
            return iter(rows)
        grouped = _group_rows(rows, group_stage)
        sort_stage = next((stage["$sort"] for stage in pipeline if "$sort" in stage), None)
        if sort_stage:
            key, direction = next(iter(sort_stage.items()))
            grouped.sort(key=lambda row: _sort_value(row.get(key)), reverse=direction < 0)
        limit_stage = next((stage["$limit"] for stage in pipeline if "$limit" in stage), None)
        if limit_stage:
            grouped = grouped[: int(limit_stage)]
        return iter(grouped)



    def _find_one_sql(self, query: dict[str, Any], sort: list[tuple[str, int]] | None) -> dict[str, Any] | None:
        if not sort or self.kind not in {"vaccine_admins", "vaccine_summary", "population"}:
            return None
        key, direction = sort[0]
        table = _aggregate_table(self.kind)
        if table is None:
            return None
        sort_column = _sql_field_column(table, f"${key}")
        if sort_column is None:
            return None
        stmt = select(table.c.payload)
        filters = _sql_filters(table, query)
        if filters:
            stmt = stmt.where(and_(*filters))
        stmt = stmt.order_by(sort_column.desc() if direction < 0 else sort_column.asc()).limit(1)
        with self.engine.connect() as conn:
            row = conn.execute(stmt).first()
        return dict(row[0]) if row else None

    def _aggregate_sql(self, pipeline: list[dict[str, Any]]) -> list[dict[str, Any]] | None:
        group_stage = next((stage["$group"] for stage in pipeline if "$group" in stage), None)
        if group_stage is None:
            return None

        table = _aggregate_table(self.kind)
        if table is None:
            return None

        match = _match_from_pipeline(pipeline)
        group_expr = group_stage.get("_id")
        group_columns = _sql_group_columns(table, group_expr)
        if group_columns is None:
            return None

        id_columns, id_builder = group_columns
        select_columns = [column.label(label) for label, column in id_columns]
        sum_columns: list[tuple[str, Any]] = []
        for field, expr in group_stage.items():
            if field == "_id" or not isinstance(expr, dict) or "$sum" not in expr:
                if field != "_id":
                    return None
                continue
            column = _sql_metric_column(table, expr["$sum"])
            if column is None:
                return None
            sum_columns.append((field, column))
            select_columns.append(func.coalesce(func.sum(column), 0).label(field))

        stmt = select(*select_columns)
        filters = _sql_filters(table, match)
        if filters:
            stmt = stmt.where(and_(*filters))
        if id_columns:
            stmt = stmt.group_by(*[column for _, column in id_columns])

        sort_stage = next((stage["$sort"] for stage in pipeline if "$sort" in stage), None)
        if sort_stage:
            sort_key, direction = next(iter(sort_stage.items()))
            sort_column = next((column for label, column in id_columns if label == sort_key), None)
            if sort_key == "_id" and len(id_columns) == 1:
                sort_column = id_columns[0][1]
            if sort_column is None:
                sort_column = next((expr for expr in select_columns if getattr(expr, "name", None) == sort_key), None)
            if sort_column is not None:
                stmt = stmt.order_by(sort_column.desc() if direction < 0 else sort_column.asc())
        if limit_stage := next((stage["$limit"] for stage in pipeline if "$limit" in stage), None):
            stmt = stmt.limit(int(limit_stage))

        with self.engine.connect() as conn:
            rows = conn.execute(stmt).mappings().all()

        result = []
        for row in rows:
            item = {"_id": id_builder(row)}
            for field, _ in sum_columns:
                item[field] = _clean_number(row[field])
            result.append(item)
        return result

    def _load(self, query: dict[str, Any], projection: dict[str, Any] | None) -> list[dict[str, Any]]:
        if self.kind == "pandemic":
            rows = self._load_pandemic(query)
        elif self.kind == "artifact":
            rows = self._load_artifacts(query)
        elif self.kind == "population":
            rows = self._load_payload_table(population_age, query, order_by=[population_age.c.area.asc(), population_age.c.age_band.asc()])
        elif self.kind == "vaccine_admins":
            rows = self._load_payload_table(vaccine_admin_daily, query, order_by=[vaccine_admin_daily.c.data.asc()])
        elif self.kind == "vaccine_summary":
            rows = self._load_payload_table(vaccine_summary_daily, query, order_by=[vaccine_summary_daily.c.data.asc()])
        else:
            rows = []
        rows = [row for row in rows if _matches(row, query)]
        if projection:
            rows = [_project(row, projection) for row in rows]
        return rows

    def _load_pandemic(self, query: dict[str, Any]) -> list[dict[str, Any]]:
        stmt = select(pandemic_daily.c.payload).where(pandemic_daily.c.scope == self.scope)
        filters = []
        area = query.get(REGION_KEY) or query.get(PROVINCE_KEY)
        if area is not None and not isinstance(area, dict):
            column = pandemic_daily.c.province if self.scope == "provincial" else pandemic_daily.c.area
            filters.append(column == area)
        if filters:
            stmt = stmt.where(and_(*filters))
        stmt = stmt.order_by(pandemic_daily.c.data.asc())
        with self.engine.connect() as conn:
            return [dict(row[0]) for row in conn.execute(stmt)]

    def _load_artifacts(self, query: dict[str, Any]) -> list[dict[str, Any]]:
        stmt = select(dashboard_artifacts.c.area, dashboard_artifacts.c.payload).where(
            dashboard_artifacts.c.artifact_type == self.artifact_type,
            dashboard_artifacts.c.scope == self.scope,
        )
        area = query.get(REGION_KEY) or query.get(PROVINCE_KEY)
        if area is not None and not isinstance(area, dict):
            stmt = stmt.where(dashboard_artifacts.c.area == area)
        stmt = stmt.order_by(dashboard_artifacts.c.sort_order.asc())
        with self.engine.connect() as conn:
            rows = [(row[0], dict(row[1])) for row in conn.execute(stmt)]
        if self.flatten_trends:
            return list(rows[0][1].get("trends", [])) if rows else []
        if self.wrap_trends:
            return [{REGION_KEY: area, PROVINCE_KEY: area, "trends": payload.get("trends", [])} for area, payload in rows]
        if self.wrap_breakdown:
            return [{REGION_KEY: area, "breakdowns": payload} for area, payload in rows]
        return [payload for _, payload in rows]

    def _load_payload_table(self, table: Table, query: dict[str, Any], order_by: list[Any]) -> list[dict[str, Any]]:
        stmt = select(table.c.payload)
        filters = []
        area_code = query.get(VAX_AREA_KEY)
        if area_code is not None and not isinstance(area_code, dict) and "area_code" in table.c:
            filters.append(table.c.area_code == area_code)
        if filters:
            stmt = stmt.where(and_(*filters))
        stmt = stmt.order_by(*order_by)
        with self.engine.connect() as conn:
            return [dict(row[0]) for row in conn.execute(stmt)]



def _aggregate_table(kind: str) -> Table | None:
    return {
        "population": population_age,
        "vaccine_admins": vaccine_admin_daily,
        "vaccine_summary": vaccine_summary_daily,
    }.get(kind)


def _sql_group_columns(table: Table, expr: Any):
    if expr is None:
        return [], lambda row: None
    if isinstance(expr, str):
        column = _sql_field_column(table, expr)
        if column is None:
            return None
        return [("_id", column)], lambda row: row["_id"]
    if isinstance(expr, dict):
        columns = []
        for label, value in expr.items():
            column = _sql_field_column(table, value)
            if column is None:
                return None
            columns.append((label, column))
        return columns, lambda row: {label: row[label] for label, _ in columns}
    return None


def _sql_filters(table: Table, query: dict[str, Any]) -> list[Any]:
    filters = []
    for field, expected in query.items():
        column = _sql_field_column(table, f"${field}")
        if column is None:
            return []
        if isinstance(expected, dict):
            if "$ne" in expected:
                filters.append(column != expected["$ne"])
            continue
        filters.append(column == expected)
    return filters


def _sql_field_column(table: Table, expr: Any):
    if not isinstance(expr, str) or not expr.startswith("$"):
        return None
    key = expr[1:]
    if table is population_age:
        return {
            VAX_AREA_KEY: population_age.c.area_code,
            VAX_AGE_KEY: population_age.c.age_band,
            OD_POP_KEY: population_age.c.population,
        }.get(key)
    if table is vaccine_admin_daily:
        return {
            VAX_DATE_KEY: vaccine_admin_daily.c.data,
            VAX_AREA_KEY: vaccine_admin_daily.c.area_code,
            VAX_AGE_KEY: vaccine_admin_daily.c.age_band,
            VAX_PROVIDER_KEY: vaccine_admin_daily.c.provider,
            VAX_FIRST_DOSE_KEY: vaccine_admin_daily.c.first_dose,
            VAX_SECOND_DOSE_KEY: vaccine_admin_daily.c.second_dose,
            VAX_BOOSTER_DOSE_KEY: vaccine_admin_daily.c.booster_dose,
            VAX_TOT_ADMINS_KEY: vaccine_admin_daily.c.total_admins,
        }.get(key)
    if table is vaccine_summary_daily:
        return {
            VAX_DATE_KEY: vaccine_summary_daily.c.data,
            VAX_AREA_KEY: vaccine_summary_daily.c.area_code,
            VAX_FIRST_DOSE_KEY: vaccine_summary_daily.c.first_dose,
            VAX_SECOND_DOSE_KEY: vaccine_summary_daily.c.second_dose,
            VAX_BOOSTER_DOSE_KEY: vaccine_summary_daily.c.booster_dose,
            VAX_TOT_ADMINS_KEY: vaccine_summary_daily.c.total_admins,
            VAX_POP_KEY: vaccine_summary_daily.c.population,
            "dosi_consegnate": vaccine_summary_daily.c.delivered_doses,
        }.get(key)
    return None


def _sql_metric_column(table: Table, expr: Any):
    return _sql_field_column(table, expr)


def _match_from_pipeline(pipeline: list[dict[str, Any]]) -> dict[str, Any]:
    for stage in pipeline:
        if "$match" in stage:
            return stage["$match"]
    return {}


def _matches(row: dict[str, Any], query: dict[str, Any]) -> bool:
    for key, expected in query.items():
        actual = row.get(key)
        if isinstance(expected, dict):
            if "$ne" in expected and actual == expected["$ne"]:
                return False
            continue
        if actual != expected:
            return False
    return True


def _project(row: dict[str, Any], projection: dict[str, Any]) -> dict[str, Any]:
    if projection.get("_id") is False and len(projection) == 1:
        return dict(row)
    include = {key for key, enabled in projection.items() if enabled is True}
    projected = {key: row.get(key) for key in include if key in row} if include else dict(row)
    if projection.get("_id") is False:
        projected.pop("_id", None)
    return projected


def _group_rows(rows: list[dict[str, Any]], group_stage: dict[str, Any]) -> list[dict[str, Any]]:
    groups: dict[Any, dict[str, Any]] = {}
    for row in rows:
        key = _group_key(row, group_stage.get("_id"))
        hash_key = _hashable_key(key)
        out = groups.setdefault(hash_key, {"_id": key})
        for field, expr in group_stage.items():
            if field == "_id" or not isinstance(expr, dict):
                continue
            if "$sum" in expr:
                out[field] = _clean_number(out.get(field, 0) + _number(_field(row, expr["$sum"])))
            elif "$max" in expr:
                out[field] = _clean_number(max(out.get(field, 0), _number(_field(row, expr["$max"]))))
    return list(groups.values())


def _group_key(row: dict[str, Any], expr: Any) -> Any:
    if isinstance(expr, str):
        return _field(row, expr)
    if isinstance(expr, dict):
        return {key: _field(row, value) for key, value in expr.items()}
    return expr


def _hashable_key(value: Any) -> Any:
    if isinstance(value, dict):
        return tuple(sorted((key, _hashable_key(item)) for key, item in value.items()))
    if isinstance(value, list):
        return tuple(_hashable_key(item) for item in value)
    return value


def _field(row: dict[str, Any], expr: Any) -> Any:
    if isinstance(expr, str) and expr.startswith("$"):
        return row.get(expr[1:])
    return expr


def _number(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _clean_number(value: float) -> int | float:
    return int(value) if float(value).is_integer() else value


def _sort_value(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return dt.datetime.fromisoformat(value)
        except ValueError:
            return value
    return value if value is not None else ""
