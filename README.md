# COVIDash.it

Modern COVID analytics dashboard for Italy. This rewrite preserves the original COVIDash.it product meaning while moving the application toward a maintainable FastAPI + React architecture.

The data contract is intentionally unchanged: MongoDB is populated by [`covidashflow`](https://github.com/fabriziomiano/covidashflow), and this app reads those existing collections.

## Architecture

- `backend/`: FastAPI API layer over the existing MongoDB collections.
- `frontend/`: React + TypeScript + Vite single-page app with D3 charts.

## Preserved dashboard semantics

The modern app keeps the original dashboard structure:

- Pandemic national dashboard at `/`.
- Regional pandemic dashboards at `/regions/:area`.
- Provincial pandemic dashboards at `/provinces/:area`.
- Vaccination dashboard at `/vaccines` and `/vaccines/:area`.
- Same major KPI groups: daily, current, cumulative, and vaccine dose trends.
- Same area hierarchy: Italy, regions, provinces.
- Same vaccine charts: administrations by region, vaccination trend, administrations by age, and provider pie chart.
- Same historical reference periods on pandemic time-series charts, including lockdown and vaccine-day markers.
- Same Mongo collection contract produced by `covidashflow`.

D3 is used for the modern charts. The goal is not a pixel-for-pixel copy of the legacy Highcharts setup: the charts preserve the original analytical meaning while adding richer tooltips, responsive axes, key-period legends, compact value formatting, and time drill controls where useful.

## Configuration

Create a local environment file:

```shell
cp .env.example .env
```

Important variables:

| Variable | Purpose |
| --- | --- |
| `MONGO_URI` | Mongo database populated by `covidashflow`. |
| `PORT` | FastAPI/production HTTP port. Defaults to `5050` because macOS Control Center may reserve `5000`. |
| `CORS_ORIGINS` | Allowed local frontend/API origins. |
| `FRONTEND_DIST` | Built frontend directory served by FastAPI in production. |
| `*_COLLECTION` | Existing covidashflow output collection names. |

The defaults match the historical collection names: `National`, `NationalTrends`, `NationalSeries`, `Regional`, `RegionalTrends`, `RegionalSeries`, `RegionalBreakdown`, `Provincial`, `ProvincialTrends`, `ProvincialSeries`, `ProvincialBreakdown`, `VaxAdmins`, `VaxAdminsSummary`, and `Population`.

## Run locally

Backend:

```shell
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 5050
```

Frontend:

```shell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` to `http://localhost:5050`; production Docker serves the built app on `PORT`, normally `5050`.

## Build

Frontend only:

```shell
cd frontend
npm run build
```

Docker production image:

```shell
docker compose --env-file .env build
docker compose --env-file .env up -d
```

The container builds the React app, installs the FastAPI backend, and serves the SPA through FastAPI on `PORT`.

## Frontend behaviour

- Pandemic tabs preserve the legacy daily, current, and cumulative views.
- KPI cards show the current value, the previous comparison value, the comparison date, and percentage change where the baseline allows it.
- Large values use compact formatting in the UI while preserving full labels in API payloads.
- Pandemic time-series charts include D3 tooltips, dynamic x-axis ticks, time drill controls, and key-period markers.
- Vaccine coverage is shown as summary cards for first dose, second dose, and booster coverage.
- Vaccine charts use D3-native views for regional coverage, age-band doses, vaccination trend by selected regions, and provider share.
- Region/province navigation uses compact autocomplete instead of a large native dropdown.

## API

Modern endpoints:

- `GET /api/health`
- `GET /api/config`
- `GET /api/pandemic/national`
- `GET /api/pandemic/regional?area=Sicilia`
- `GET /api/pandemic/provincial?area=Catania`
- `GET /api/vaccines`
- `GET /api/vaccines?area=Sicilia`

Backward-compatible vaccine chart endpoints:

- `GET /api/vax_charts/region`
- `GET /api/vax_charts/trend`
- `GET /api/vax_charts/age?area=Sicilia`
- `GET /api/vax_charts/provider?area=Sicilia`

The legacy Flask app and its `/api/plot` matplotlib endpoint were removed in v7.0.0. The supported runtime surface is the FastAPI API plus the React dashboard.

## Deploy on a private server

A pragmatic private-server deployment is:

1. Build the Docker image on the server or in CI.
2. Provide `.env` with the production `MONGO_URI`, `PORT`, CORS origins, and collection names.
3. Run `docker compose --env-file .env up -d`.
4. Put Nginx/Caddy in front of the container for TLS, gzip/brotli, and canonical host redirects.
5. Keep `covidashflow` scheduled separately so MongoDB stays populated before dashboards are read.

Example reverse proxy flow:

```text
https://www.covidash.it -> Nginx/Caddy -> covidashit app container -> MongoDB populated by covidashflow
```

## Tests and checks

Backend tests:

```shell
pytest
```

Frontend checks:

```shell
cd frontend
npm run build
npm run lint
```

Docker smoke check:

```shell
docker compose --env-file .env build
docker compose --env-file .env up -d
curl --fail http://localhost:${PORT:-5050}/api/health
docker compose --env-file .env down
```

## Assumptions

- MongoDB contains the same collection names and document shapes generated by `covidashflow`.
- The FastAPI layer reads the existing covidashflow collections directly and rebuilds some chart series from canonical raw rows where this prevents known legacy artifacts from duplicated/corrected cumulative data.
- Vaccine summary and administration collections can have different latest dates; the dashboard uses the latest available vaccine date and labels trend-card comparison samples explicitly.

## Remaining manual checks

- Compare each KPI card count, trend direction, and percentage against the current production dashboard.
- Compare D3 series visibility, time drill behaviour, key-period markers, and date labels for national, regional, and provincial pages.
- Validate vaccine percentage calculations and regional chart selections against the live dashboard after connecting to production Mongo.
