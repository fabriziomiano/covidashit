# Showcase Notes

COVIDash.it is best evaluated as an archived full-stack analytics project rather than a live COVID tracker.

## What To Look At

- The dashboard exposes national, regional, provincial, and vaccination views.
- Charts are rebuilt from warehouse-backed API payloads.
- Area search and routed dashboards make the historical data inspectable.
- The ETL remains runnable and demonstrates full and delta loading semantics.
- Prefect deployments document how live operations would have worked.

## Suggested Demo Path

1. Start Postgres and Prefect:

   ```shell
   docker compose up -d postgres prefect-server prefect-worker
   ```

2. Load the historical data:

   ```shell
   docker compose --profile etl run --rm etl python -m covidashflow all --mode full --run-id showcase-full-001
   ```

3. Start the dashboard:

   ```shell
   docker compose up -d app
   ```

4. Open `http://localhost:5050`.

## Screenshot Checklist

When refreshing portfolio material, capture:

- national pandemic dashboard,
- one regional dashboard,
- vaccination dashboard,
- Prefect deployments page,
- API docs at `/docs`.

Keep screenshots framed as historical data inspection.
