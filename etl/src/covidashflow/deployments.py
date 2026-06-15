"""Register Prefect deployments for scheduled and on-demand ETL runs."""

from __future__ import annotations

from prefect.client.schemas.schedules import CronSchedule

from covidashflow.flows import dpc_flow, full_flow, vaccines_flow

WORK_POOL_NAME = "covidash-etl"
TIMEZONE = "Europe/Rome"


def register_deployments(work_pool_name: str = WORK_POOL_NAME) -> list[str]:
    """Create or update deployments shown in the Prefect UI."""

    deployments = [
        full_flow.to_deployment(
            name="manual-delta",
            parameters={"mode": "delta"},
            work_pool_name=work_pool_name,
            tags=["manual", "delta", "all"],
            description="Run all COVIDash ETL pipelines in delta mode on demand.",
        ),
        full_flow.to_deployment(
            name="manual-full",
            parameters={"mode": "full"},
            work_pool_name=work_pool_name,
            tags=["manual", "full", "all"],
            description="Run a full rebuild of all COVIDash ETL warehouse tables on demand.",
        ),
        dpc_flow.to_deployment(
            name="manual-dpc-delta",
            parameters={"mode": "delta"},
            work_pool_name=work_pool_name,
            tags=["manual", "delta", "dpc"],
            description="Run only the PCM-DPC pandemic ETL in delta mode on demand.",
        ),
        vaccines_flow.to_deployment(
            name="manual-vaccines-delta",
            parameters={"mode": "delta"},
            work_pool_name=work_pool_name,
            tags=["manual", "delta", "vaccines"],
            description="Run only the vaccination ETL in delta mode on demand.",
        ),
        full_flow.to_deployment(
            name="scheduled-daily-delta",
            parameters={"mode": "delta"},
            schedules=[CronSchedule(cron="0 5 * * *", timezone=TIMEZONE)],
            work_pool_name=work_pool_name,
            tags=["scheduled", "delta", "all"],
            description="Run all COVIDash ETL pipelines daily in delta mode.",
        ),
    ]

    registered = []
    for deployment in deployments:
        deployment.apply()
        registered.append(f"{deployment.flow_name}/{deployment.name}")
    return registered


def main() -> None:
    for name in register_deployments():
        print(f"Registered Prefect deployment: {name}")


if __name__ == "__main__":
    main()
