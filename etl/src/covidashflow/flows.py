"""Prefect flows for COVIDash ETL."""

from __future__ import annotations

from prefect import flow, task

from covidashflow.common.postgres import ensure_schema, get_engine, wait_for_database
from covidashflow.sql_pipeline import LoadMode, run_dpc_sql_pipeline, run_opendata_sql_pipeline


@task(retries=3, retry_delay_seconds=10)
def prepare_database() -> None:
    """Wait for Postgres and ensure the COVIDash schema exists."""

    engine = get_engine()
    wait_for_database(engine)
    ensure_schema(engine)


@task
def load_dpc_data(mode: LoadMode = "full", run_id: str | None = None) -> int:
    """Load pandemic datasets into Postgres."""

    return run_dpc_sql_pipeline(get_engine(), mode=mode, run_id=run_id)


@task
def load_vaccine_data(mode: LoadMode = "full", run_id: str | None = None) -> int:
    """Load vaccination datasets into Postgres."""

    return run_opendata_sql_pipeline(get_engine(), mode=mode, run_id=run_id)


@flow(name="covidash-dpc-etl")
def dpc_flow(mode: LoadMode = "full", run_id: str | None = None) -> int:
    """Run the PCM-DPC pandemic ETL."""

    prepare_database()
    return load_dpc_data(mode, run_id)


@flow(name="covidash-vaccines-etl")
def vaccines_flow(mode: LoadMode = "full", run_id: str | None = None) -> int:
    """Run the Italia Open Data vaccination ETL."""

    prepare_database()
    return load_vaccine_data(mode, run_id)


@flow(name="covidash-full-etl")
def full_flow(mode: LoadMode = "full", run_id: str | None = None) -> int:
    """Run every COVIDash ETL pipeline."""

    prepare_database()
    dpc_run_id = f"{run_id}-dpc" if run_id else None
    vaccines_run_id = f"{run_id}-vaccines" if run_id else None
    return load_dpc_data(mode, dpc_run_id) + load_vaccine_data(mode, vaccines_run_id)
