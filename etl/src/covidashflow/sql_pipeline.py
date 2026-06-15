"""Postgres warehouse loading pipelines for COVIDash data."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from typing import Literal

import pandas as pd
from sqlalchemy.engine import Engine

from covidashflow.common.geo import OD_TO_PC_MAP
from covidashflow.common.postgres import (
    append_pandemic_daily,
    append_vaccine_admins,
    append_vaccine_summary,
    finish_run,
    latest_pandemic_date,
    latest_vaccine_admin_date,
    latest_vaccine_summary_date,
    replace_artifacts,
    replace_pandemic_daily,
    replace_population,
    replace_vaccine_admins,
    replace_vaccine_summary,
    start_run,
)
from covidashflow.common.vars import DATE_KEY, REGION_KEY, PROVINCE_KEY, VAX_DATE_KEY
from covidashflow.dpc.pipeline import DpcSources, extract_dpc_frame
from covidashflow.dpc.transform import (
    build_national_trends,
    build_provincial_breakdowns,
    build_provincial_trends,
    build_regional_breakdown,
    build_regional_trends,
    preprocess_national_df,
    preprocess_provincial_df,
    preprocess_regional_df,
)
from covidashflow.opendata.pipeline import OpenDataSources, extract_opendata_frame
from covidashflow.opendata.transform import preprocess_vax_admins_df, preprocess_vax_admins_summary_df

LoadMode = Literal["full", "delta"]


def run_dpc_sql_pipeline(engine: Engine, sources: DpcSources = DpcSources(), mode: LoadMode = "full", run_id: str | None = None) -> int:
    """Load PCM-DPC pandemic data into typed Postgres warehouse tables."""

    return _logged_run(engine, run_id or _run_id("dpc", mode), "dpc", mode, lambda: _load_dpc(engine, sources, mode))


def run_opendata_sql_pipeline(engine: Engine, sources: OpenDataSources = OpenDataSources(), mode: LoadMode = "full", run_id: str | None = None) -> int:
    """Load Italia Open Data vaccination data into typed Postgres warehouse tables."""

    return _logged_run(engine, run_id or _run_id("vaccines", mode), "vaccines", mode, lambda: _load_vaccines(engine, sources, mode))


def _load_dpc(engine: Engine, sources: DpcSources, mode: LoadMode) -> int:
    national_df = preprocess_national_df(extract_dpc_frame(sources.national_url))
    regional_df = preprocess_regional_df(extract_dpc_frame(sources.regional_url))
    provincial_df = preprocess_provincial_df(extract_dpc_frame(sources.provincial_url))

    loaded = 0
    if mode == "full":
        loaded += replace_pandemic_daily(engine, "national", national_df.to_dict(orient="records"))
        loaded += replace_pandemic_daily(engine, "regional", regional_df.to_dict(orient="records"))
        loaded += replace_pandemic_daily(engine, "provincial", provincial_df.to_dict(orient="records"))
    else:
        loaded += append_pandemic_daily(engine, "national", _new_rows(national_df, DATE_KEY, latest_pandemic_date(engine, "national")))
        loaded += append_pandemic_daily(engine, "regional", _new_rows(regional_df, DATE_KEY, latest_pandemic_date(engine, "regional")))
        loaded += append_pandemic_daily(engine, "provincial", _new_rows(provincial_df, DATE_KEY, latest_pandemic_date(engine, "provincial")))

    if mode == "full" or loaded:
        _replace_dpc_artifacts(engine, national_df, regional_df, provincial_df)
    return loaded


def _replace_dpc_artifacts(engine: Engine, national_df: pd.DataFrame, regional_df: pd.DataFrame, provincial_df: pd.DataFrame) -> None:
    replace_artifacts(engine, "pandemic_trends", "national", [{"area": "Italia", "payload": {"trends": build_national_trends(national_df)}}])
    replace_artifacts(
        engine,
        "pandemic_trends",
        "regional",
        [
            {"area": record.get(REGION_KEY), "payload": {"trends": record.get("trends", [])}}
            for record in build_regional_trends(regional_df)
        ],
    )
    replace_artifacts(
        engine,
        "pandemic_trends",
        "provincial",
        [
            {"area": record.get(PROVINCE_KEY), "payload": {"trends": record.get("trends", [])}}
            for record in build_provincial_trends(provincial_df)
        ],
    )
    replace_artifacts(engine, "pandemic_breakdown", "national", [{"area": "Italia", "payload": build_regional_breakdown(regional_df)}])
    replace_artifacts(
        engine,
        "pandemic_breakdown",
        "regional",
        [
            {"area": record.get(REGION_KEY), "payload": record.get("breakdowns", {})}
            for record in build_provincial_breakdowns(provincial_df)
        ],
    )


def _load_vaccines(engine: Engine, sources: OpenDataSources, mode: LoadMode) -> int:
    area_names = dict(OD_TO_PC_MAP)
    area_names.setdefault("ITA", "Italia")

    population_df = extract_opendata_frame(sources.population_url)
    population_records = population_df.to_dict(orient="records")
    replace_population(engine, population_records, area_names)

    population = _region_pop_dict(population_records)
    vax_df = extract_opendata_frame(sources.vax_admins_url, parse_dates=True, low_memory=False)
    preprocessed_vax_df = preprocess_vax_admins_df(vax_df)

    summary_df = extract_opendata_frame(sources.vax_admins_summary_url, parse_dates=True)
    preprocessed_summary_df = preprocess_vax_admins_summary_df(summary_df, population)

    if mode == "full":
        loaded = replace_vaccine_admins(engine, preprocessed_vax_df.to_dict(orient="records"), area_names)
        loaded += replace_vaccine_summary(engine, preprocessed_summary_df.to_dict(orient="records"), area_names)
        return loaded + len(population_records)

    loaded = append_vaccine_admins(engine, _new_rows(preprocessed_vax_df, VAX_DATE_KEY, latest_vaccine_admin_date(engine)), area_names)
    loaded += append_vaccine_summary(engine, _new_rows(preprocessed_summary_df, VAX_DATE_KEY, latest_vaccine_summary_date(engine)), area_names)
    return loaded


def _region_pop_dict(records: list[dict]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for record in records:
        area = record.get("area")
        totals[area] = totals.get(area, 0) + int(record.get("totale_popolazione") or 0)
    return {OD_TO_PC_MAP[area]: population for area, population in totals.items()}


def _new_rows(df: pd.DataFrame, date_key: str, latest: object | None) -> list[dict]:
    if latest is None or df.empty:
        return df.to_dict(orient="records")
    cutoff = pd.Timestamp(latest).tz_localize(None)
    dates = pd.to_datetime(df[date_key]).dt.tz_localize(None)
    return df.loc[dates > cutoff].to_dict(orient="records")


def _logged_run(engine: Engine, run_id: str, pipeline: str, mode: LoadMode, loader: Callable[[], int]) -> int:
    if not start_run(engine, run_id, pipeline, mode):
        return 0
    try:
        rows_loaded = loader()
    except Exception as exc:
        finish_run(engine, run_id, "failed", message=str(exc))
        raise
    finish_run(engine, run_id, "completed", rows_loaded=rows_loaded, skipped=rows_loaded == 0)
    return rows_loaded


def _run_id(pipeline: str, mode: LoadMode) -> str:
    return f"{pipeline}-{mode}-{uuid.uuid4()}"
