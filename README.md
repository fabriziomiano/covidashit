# COVIDash.it

COVIDash.it is an archival showcase of an Italian COVID-19 analytics dashboard. The public data sources are no longer meaningfully updated, so the project is kept as a reproducible full-stack data product: React/D3 frontend, FastAPI API, PostgreSQL warehouse, and Prefect 3 ETL.

The live-style ETL remains in the repo because it demonstrates how the original dashboard data path was modernized. For portfolio review, the important story is deterministic historical replay and dashboard inspection, not ongoing epidemiological freshness.

## Showcase

- Product: `https://covidash.it`
- Documentation: `docs/`
- Architecture: React + TypeScript + D3, FastAPI, PostgreSQL, Prefect 3, Docker Compose
- Demonstrates: dashboard modernization, open-data ETL, typed warehouse tables, API facade design, containerized local deployment, SEO/error handling, and CI-ready validation
- Historical scope: pandemic and vaccination datasets are treated as archived public data

## Architecture

- `etl/`: Prefect flows and loaders that extract DPC and Italian vaccine open data, normalize it, and write typed PostgreSQL warehouse tables plus dashboard artifacts.
- `backend/`: FastAPI API layer. In the default Compose stack it reads PostgreSQL through the SQL dashboard store.
- `frontend/`: React + TypeScript + Vite dashboard with D3 charts.
- `docker-compose.yaml`: unified local stack for PostgreSQL, Prefect, ETL, and the dashboard app.

## Data Loading

The ETL supports both initial full loads and incremental delta loads. Full loads replace warehouse tables and refresh dashboard artifacts. Delta loads compare source dates with the latest loaded PostgreSQL dates and append only new rows. Each pipeline writes an `etl_run_log` entry with status, row count, skipped state, and failure message when applicable. Reusing the exact same run id is treated as already handled and does not replay the load.

For showcase and review use, prefer a full load with an explicit run id. If long-term reproducibility is required, pin the source URLs in `etl/src/covidashflow/common/urls.py` to immutable GitHub commit URLs or import a saved PostgreSQL dump before starting the app.

Run a full initial load:

```shell
docker compose --profile etl run --rm etl python -m covidashflow all --mode full --run-id initial-full-001
```

Run a delta load:

```shell
docker compose --profile etl run --rm etl python -m covidashflow all --mode delta --run-id delta-$(date +%Y%m%d%H%M%S)
```

Load individual pipelines by replacing `all` with `dpc` or `vaccines`.

## Run Locally

Start the database, Prefect UI, and worker:

```shell
docker compose up -d postgres prefect-server prefect-worker
```

Load data, then start the dashboard:

```shell
docker compose --profile etl run --rm etl python -m covidashflow all --mode full --run-id local-full-001
docker compose up -d app
```

Open:

- Dashboard: `http://localhost:5050`
- Dashboard health: `http://localhost:5050/api/health`
- Prefect UI: `http://localhost:8080`
- Prefect API health: `http://localhost:8080/api/health` locally, or `https://prefect.covidash.it/api/health` through NGINX

Default local ports can be overridden with `COVIDASHIT_PORT`, `COVIDASH_SQL_PORT`, and `PREFECT_UI_PORT`. Set `PREFECT_UI_API_URL` to the browser-reachable Prefect API URL. The default is `https://prefect.covidash.it/api`; for direct localhost access override it with `http://localhost:8080/api`.

## Prefect Runs

`prefect-worker` registers these deployments when it starts. The manual deployments are the useful ones for this archived showcase; the scheduled/event-triggered paths are retained to document the production-style design:

- `covidash-full-etl/manual-delta` for an on-demand all-pipeline delta run.
- `covidash-full-etl/manual-full` for an on-demand full warehouse rebuild.
- `covidash-dpc-etl/manual-dpc-delta` for an on-demand pandemic-only delta run.
- `covidash-vaccines-etl/manual-vaccines-delta` for an on-demand vaccines-only delta run.
- `covidash-full-etl/scheduled-daily-delta` for the daily scheduled delta run at 05:00 Europe/Rome. This is demo infrastructure now that upstream data is historical.

In the Prefect UI, open a deployment and click **Run** to trigger it immediately. The same run can be triggered from the CLI:

```shell
docker compose exec prefect-worker prefect deployment run covidash-full-etl/manual-delta
```

The worker also creates the automation `Run COVIDash delta ETL on source data commit`. It runs `covidash-full-etl/manual-delta` when Prefect receives this event for either upstream data repository:

- event name: `covidash.source.commit`
- resource id: `github.repository.pcm-dpc/COVID-19`
- resource id: `github.repository.italia/covid19-opendata-vaccini`

A GitHub webhook bridge, Cloudflare Worker, or other event sender can emit the event to Prefect when the source repositories publish commits. A local smoke event can be emitted with:

```shell
docker compose exec prefect-worker prefect events emit covidash.source.commit   --resource-id github.repository.pcm-dpc/COVID-19   --payload '{"repository":"pcm-dpc/COVID-19","reason":"manual-smoke"}'
```

## Configuration

Important variables:

| Variable | Purpose | Default |
| --- | --- | --- |
| `DATABASE_URL` | PostgreSQL URL for ETL and SQL dashboard reads. | Compose service URL |
| `COVIDASHIT_PORT` | Dashboard HTTP port. | `5050` |
| `COVIDASH_SQL_PORT` | Host PostgreSQL port. | `5433` |
| `PREFECT_UI_PORT` | Host Prefect UI/API port. | `8080` |
| `PREFECT_UI_API_URL` | API URL used by the Prefect browser UI. Use the browser-reachable hostname. | `https://prefect.covidash.it/api` |
| `PREFECT_API_DATABASE_CONNECTION_URL` | Prefect Server metadata database. Uses Postgres in Compose to avoid SQLite lock contention. | Compose service URL |
| `CORS_ORIGINS` | Allowed frontend/API origins. | local dashboard/dev origins plus `http://covidash.it` |
| `FRONTEND_DIST` | Built frontend directory served by FastAPI. | `/app/frontend/dist` in Docker |

## Dashboard Routes

- `/` for the national pandemic dashboard.
- `/regions/:area` for regional pandemic dashboards.
- `/provinces/:area` for provincial pandemic dashboards.
- `/vaccines` and `/vaccines/:area` for vaccination dashboards.

API endpoints:

- `GET /api/health`
- `GET /api/config`
- `GET /api/pandemic/national`
- `GET /api/pandemic/regional?area=Sicilia`
- `GET /api/pandemic/provincial?area=Catania`
- `GET /api/vaccines`
- `GET /api/vaccines?area=Sicilia`
- `GET /api/vax_charts/region`
- `GET /api/vax_charts/trend`
- `GET /api/vax_charts/age?area=Sicilia`
- `GET /api/vax_charts/provider?area=Sicilia`

## Build And Test

Backend tests inside the app container:

```shell
docker compose exec app sh -c 'PYTHONPATH=/app pytest backend/tests'
```

Docker build and frontend production build are covered by:

```shell
docker compose build app
```

Validate Compose files:

```shell
docker compose -f docker-compose.yaml config --quiet
docker compose -f docker-compose.sql.yaml config --quiet
```

Frontend validation:

```shell
cd frontend
npm ci
npm run lint
npm run build
```

## Deployment

A single-host deployment can run the unified stack directly:

```shell
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d postgres prefect-server app
docker compose --profile etl run --rm etl python -m covidashflow all --mode delta --run-id production-delta-$(date +%Y%m%d%H%M%S)
```

Put nginx in front of the dashboard and Prefect UI. The intended hosts are:

```text
https://covidash.it -> app on localhost:5050
https://prefect.covidash.it -> prefect-server on localhost:8080
```

The app image enables Uvicorn proxy headers so nginx can pass `X-Forwarded-*` headers for TLS-aware redirects and links.
