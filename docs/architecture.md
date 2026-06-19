# Architecture

COVIDash.it is kept as an archival analytics system. The original public-health data sources are historical, but the repository preserves a complete modern data-product shape: extraction, transformation, warehouse loading, API serving, and interactive dashboard rendering.

## Runtime Shape

- React + TypeScript + D3 renders the browser dashboard.
- FastAPI serves API routes and the built SPA.
- PostgreSQL stores typed warehouse tables and JSON payloads used by the API.
- Prefect 3 runs the ETL flows and records operational state.
- Docker Compose provides a single-machine local and deployment stack.

## Data Flow

1. ETL reads Italian Civil Protection pandemic CSVs and Italian vaccination open-data CSVs.
2. Pandas transformations normalize dates, area names, daily deltas, moving averages, and chart payloads.
3. SQLAlchemy writes fact tables and run-log records into PostgreSQL.
4. FastAPI reads PostgreSQL through a dashboard service layer.
5. React fetches snapshots and chart payloads from `/api/*`.

## Archived-Data Assumption

The project should not imply active public-health monitoring. Its current value is as a reproducible showcase of:

- migrating a legacy dashboard into a typed monorepo,
- preserving data lineage from public CSVs to chart-ready responses,
- keeping operational ETL concepts visible through Prefect,
- serving a polished dashboard from a containerized API app.

For deterministic replay, pin source URLs in `etl/src/covidashflow/common/urls.py` to immutable upstream commits or restore a saved PostgreSQL dump before launching the app.

## Validation

The intended quality gates are:

- backend unit tests with `pytest`,
- frontend lint and production build,
- Docker Compose configuration validation,
- optional Docker image build for end-to-end packaging.
