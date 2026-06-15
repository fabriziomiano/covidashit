"""Register Prefect deployments for scheduled and on-demand ETL runs."""

from __future__ import annotations

import asyncio

from prefect.client.orchestration import get_client
from prefect.client.schemas.schedules import CronSchedule
from prefect.events.actions import RunDeployment
from prefect.events.schemas.automations import AutomationCore, EventTrigger

from covidashflow.flows import dpc_flow, full_flow, vaccines_flow

WORK_POOL_NAME = "covidash-etl"
TIMEZONE = "Europe/Rome"
SOURCE_COMMIT_AUTOMATION_NAME = "Run COVIDash delta ETL on source data commit"
SOURCE_COMMIT_EVENT = "covidash.source.commit"
SOURCE_REPOSITORIES = [
    "pcm-dpc/COVID-19",
    "italia/covid19-opendata-vaccini",
]


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


async def register_source_commit_automation() -> str:
    """Create or update the event automation for upstream data commits.

    The automation is triggered by events emitted with:
    - event: covidash.source.commit
    - resource.prefect.resource.id: github.repository.<owner>/<repo>

    GitHub webhooks or a small bridge service can emit these events to Prefect
    when the upstream data repositories publish new commits.
    """

    async with get_client() as client:
        deployment = await client.read_deployment_by_name("covidash-full-etl/manual-delta")
        automation = AutomationCore(
            name=SOURCE_COMMIT_AUTOMATION_NAME,
            description=(
                "Run the all-pipeline delta ETL when PCM-DPC or Italia Open Data "
                "source repositories emit a new data commit event."
            ),
            enabled=True,
            tags=["source-trigger", "delta", "github"],
            trigger=EventTrigger(
                expect={SOURCE_COMMIT_EVENT},
                match={
                    "prefect.resource.id": [f"github.repository.{repo}" for repo in SOURCE_REPOSITORIES],
                },
                posture="Reactive",
                threshold=1,
                within=0,
            ),
            actions=[
                RunDeployment(
                    deployment_id=deployment.id,
                    parameters={"mode": "delta"},
                )
            ],
        )
        existing = await client.read_automations_by_name(SOURCE_COMMIT_AUTOMATION_NAME)
        if existing:
            await client.update_automation(existing[0].id, automation)
            return f"Updated Prefect automation: {SOURCE_COMMIT_AUTOMATION_NAME}"
        await client.create_automation(automation)
        return f"Registered Prefect automation: {SOURCE_COMMIT_AUTOMATION_NAME}"


def main() -> None:
    for name in register_deployments():
        print(f"Registered Prefect deployment: {name}")
    print(asyncio.run(register_source_commit_automation()))


if __name__ == "__main__":
    main()
