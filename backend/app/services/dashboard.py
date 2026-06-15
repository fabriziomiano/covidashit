"""Dashboard data service backed by COVIDash warehouse collections."""

from __future__ import annotations

import datetime as dt
from typing import Any, Literal

from fastapi import HTTPException, status
from backend.app.core.constants import (
    DATE_KEY,
    ITALY_MAP,
    NEW_POSITIVE_KEY,
    NOTE_KEY,
    OD_POP_KEY,
    OD_TO_PC_MAP,
    PAGE_BASE_TITLE,
    PC_TO_OD_MAP,
    POSITIVITY_INDEX,
    PROVINCE_KEY,
    PROVINCES,
    REGION_KEY,
    REGIONS,
    TOTAL_CASES_KEY,
    VARS,
    VAX_AGE_KEY,
    VAX_AREA_KEY,
    VAX_BOOSTER_DOSE_KEY,
    VAX_DATE_KEY,
    VAX_DOSES,
    VAX_FIRST_DOSE_KEY,
    VAX_POP_KEY,
    VAX_PROVIDER_KEY,
    VAX_SECOND_DOSE_KEY,
    VAX_TOT_ADMINS_KEY,
    VERSION,
)
from backend.app.core.sql_db import SqlCollections
from backend.app.services.serializers import chart_date, clean_document, display_date, number

Scope = Literal["national", "regional", "provincial"]

DAILY_SERIES_KEYS = [
    ("tamponi_g_ma", "tamponi_g", "tamponi"),
    ("nuovi_positivi_ma", "nuovi_positivi", None),
    ("deceduti_g_ma", "deceduti_g", "deceduti"),
    ("ingressi_terapia_intensiva_ma", "ingressi_terapia_intensiva", None),
]
CURRENT_SERIES_KEYS = ["totale_positivi", "isolamento_domiciliare", "totale_ospedalizzati", "terapia_intensiva"]
CUMULATIVE_SERIES_KEYS = [TOTAL_CASES_KEY, "deceduti", "tamponi", "dimessi_guariti"]


class DashboardService:
    """Read and shape analytics documents without changing their meaning."""

    def __init__(self, collections: SqlCollections) -> None:
        self.collections = collections

    def config(self) -> dict[str, Any]:
        """Return labels, area lists, and variable metadata for the frontend."""

        return {
            "version": VERSION,
            "pageTitle": PAGE_BASE_TITLE,
            "regions": REGIONS,
            "provinces": PROVINCES,
            "italyMap": ITALY_MAP,
            "varsConfig": clean_document(VARS),
        }

    def pandemic_snapshot(self, scope: Scope, area: str | None = None) -> dict[str, Any]:
        """Return one complete pandemic dashboard snapshot for a scope/area."""

        self._validate_pandemic_area(scope, area)
        trends = self._pandemic_trends(scope, area)
        collection, query = self._data_query(scope, area)
        latest_doc = collection.find_one(query, sort=[(DATE_KEY, -1)]) or {}
        return {
            "scope": scope,
            "area": area,
            "dashboardTitle": self._dashboard_title(scope, area),
            "pageTitle": self._page_title(scope, area),
            "trendCards": trends,
            "series": self._pandemic_series(scope, area),
            "breakdown": self._pandemic_breakdown(scope, area),
            "notes": self._notes(latest_doc),
            "latestUpdate": display_date(latest_doc.get(DATE_KEY)),
            "positivityIdx": self._percentage_label(latest_doc.get(POSITIVITY_INDEX)),
            "population": None if scope == "provincial" else number(self._area_population(area or "Italia")),
            "region": self._province_region(area) if scope == "provincial" else area,
            "regionProvinces": ITALY_MAP.get(self._province_region(area), []) if scope == "provincial" else ITALY_MAP.get(area or "", []),
        }

    def vaccines_snapshot(self, area: str | None = None) -> dict[str, Any]:
        """Return one complete vaccine dashboard snapshot."""

        if area is not None and area not in REGIONS:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Area {area} not found")
        od_area = PC_TO_OD_MAP.get(area or "Italia")
        population = self._area_population(area or "Italia")
        return {
            "scope": "vaccines",
            "area": area,
            "dashboardTitle": area or "Italy",
            "pageTitle": f"{PAGE_BASE_TITLE} | Vaccines" + (f" | {area}" if area else ""),
            "latestUpdate": self._latest_vaccine_update(),
            "adminsPerc": self._admins_percentage(od_area),
            "percPopVax": self._perc_pop_vax(population, od_area),
            "trends": self._vax_trends(od_area if area else None),
            "population": number(population),
        }

    def vaccine_chart(self, chart_id: str, area: str | None = None) -> dict[str, Any]:
        """Return one vaccine chart payload."""

        menu = {
            "trend": self.vaccine_trend_chart,
            "region": self.vaccine_region_chart,
            "age": self.vaccine_age_chart,
            "provider": self.vaccine_provider_chart,
        }
        try:
            return menu[chart_id](area=area)
        except KeyError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown chart") from exc

    def vaccine_region_chart(self, area: str | None = None) -> dict[str, Any]:
        """Return administrations by region, preserving the original bar chart shape."""

        pipe = [
            {"$match": {VAX_AREA_KEY: {"$ne": "ITA"}}},
            {"$group": {"_id": f"${VAX_AREA_KEY}", "first": {"$sum": f"${VAX_FIRST_DOSE_KEY}"}, "second": {"$sum": f"${VAX_SECOND_DOSE_KEY}"}, "booster": {"$sum": f"${VAX_BOOSTER_DOSE_KEY}"}}},
        ]
        rows = list(self.collections.vax_admins_summary.aggregate(pipe))
        pop = self._region_pop_dict()
        shaped = []
        for row in rows:
            region = OD_TO_PC_MAP.get(row.get("_id"), row.get("_id"))
            shaped.append({**row, "region": region, "population": pop.get(region, 0)})
        shaped.sort(key=lambda item: item["population"], reverse=True)
        return {
            "title": "Admins per region",
            "categories": [row["region"] for row in shaped],
            "pop_dict": pop,
            "first": {"name": "First Dose", "data": [row.get("first", 0) for row in shaped]},
            "second": {"name": "Second Dose", "data": [row.get("second", 0) for row in shaped]},
            "booster": {"name": "Booster Dose", "data": [row.get("booster", 0) for row in shaped]},
            "population": {"name": "Population", "data": [row.get("population", 0) for row in shaped]},
        }

    def vaccine_trend_chart(self, area: str | None = None) -> dict[str, Any]:
        """Return cumulative second-dose percentage time series by region."""

        rows = list(self.collections.vax_admins_summary.find({}).sort(VAX_DATE_KEY, 1))
        by_region: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            by_region.setdefault(row.get(VAX_AREA_KEY), []).append(row)
        data = []
        for region_code, region_rows in sorted(by_region.items()):
            if region_code == "ITA":
                continue
            cumulative = 0
            points = []
            for row in region_rows:
                cumulative += row.get(VAX_SECOND_DOSE_KEY, 0) or 0
                population = self._summary_population(row) or 1
                points.append(round(cumulative / population * 100, 2))
            data.append({"name": OD_TO_PC_MAP.get(region_code, region_code), "data": points})
        dates = [chart_date(row.get(VAX_DATE_KEY)) for row in by_region.get("SIC", rows)]
        common_length = min([len(dates), *(len(item["data"]) for item in data)]) if data else len(dates)
        dates = dates[:common_length]
        data = [{**item, "data": item["data"][:common_length]} for item in data]
        return {"title": "Vaccination trend", "yAxisTitle": "Pop. vaccinated (2nd dose) [%]", "dates": dates, "data": data}

    def vaccine_age_chart(self, area: str | None = None) -> dict[str, Any]:
        """Return age-band administrations and population."""

        od_area = PC_TO_OD_MAP.get(area) if area in REGIONS else None
        match = [{"$match": {VAX_AREA_KEY: od_area}}] if od_area else []
        pipe = match + [{"$group": {"_id": f"${VAX_AGE_KEY}", "first": {"$sum": f"${VAX_FIRST_DOSE_KEY}"}, "second": {"$sum": f"${VAX_SECOND_DOSE_KEY}"}, "booster": {"$sum": f"${VAX_BOOSTER_DOSE_KEY}"}}}, {"$sort": {"_id": 1}}]
        rows = list(self.collections.vax_admins.aggregate(pipe))
        pop = self._age_pop_dict(od_area)
        categories = [row.get("_id") for row in rows]
        return {
            "title": "Admins per age",
            "yAxisTitle": "Counts",
            "categories": categories,
            "age_dict": pop,
            "first": {"name": "First Dose", "data": [row.get("first", 0) for row in rows]},
            "second": {"name": "Second Dose", "data": [row.get("second", 0) for row in rows]},
            "booster": {"name": "Booster Dose", "data": [row.get("booster", 0) for row in rows]},
            "population": {"name": "Population", "data": [pop.get(row.get("_id"), 0) for row in rows]},
        }

    def vaccine_provider_chart(self, area: str | None = None) -> dict[str, Any]:
        """Return administered doses by vaccine provider."""

        od_area = PC_TO_OD_MAP.get(area) if area in REGIONS else None
        match = [{"$match": {VAX_AREA_KEY: od_area}}] if od_area else []
        pipe = match + [{"$group": {"_id": f"${VAX_PROVIDER_KEY}", "tot": {"$sum": f"${VAX_TOT_ADMINS_KEY}"}}}, {"$sort": {"tot": -1}}]
        data = [[row.get("_id"), row.get("tot", 0)] for row in self.collections.vax_admins.aggregate(pipe)]
        return {"title": "Admins per provider", "name": "Doses administered", "data": data}

    def _validate_pandemic_area(self, scope: Scope, area: str | None) -> None:
        if scope == "regional" and area not in REGIONS:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Area {area} not found")
        if scope == "provincial" and area not in PROVINCES:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Area {area} not found")

    def _data_query(self, scope: Scope, area: str | None) -> tuple[Any, dict[str, Any]]:
        if scope == "regional":
            return self.collections.regional_data, {REGION_KEY: area}
        if scope == "provincial":
            return self.collections.provincial_data, {PROVINCE_KEY: area}
        return self.collections.national_data, {}

    def _pandemic_trends(self, scope: Scope, area: str | None) -> list[dict[str, Any]]:
        if scope == "national":
            trends = list(self.collections.national_trends.find({}))
        elif scope == "regional":
            trends = (self.collections.regional_trends.find_one({REGION_KEY: area}) or {}).get("trends", [])
        else:
            trends = (self.collections.provincial_trends.find_one({PROVINCE_KEY: area}) or {}).get("trends", [])
        return [self._normalize_trend_card(card) for card in trends]

    def _pandemic_series(self, scope: Scope, area: str | None) -> dict[str, Any]:
        """Return chart series rebuilt from canonical rows.

        Source cumulative corrections can briefly move backwards. Rebuilding
        here keeps the chart output stable and prevents visual artifacts such
        as multi-million daily swab spikes.
        """

        rows = self._pandemic_rows(scope, area)
        dates = [self._iso_date(row.get(DATE_KEY)) for row in rows]
        return {
            "dates": dates,
            "daily": self._daily_series(scope, rows),
            "current": self._current_series(scope, rows),
            "cum": self._cumulative_series_from_rows(scope, rows),
        }

    def _cumulative_series(self, scope: Scope, area: str | None) -> list[dict[str, Any]]:
        """Build cumulative chart series from chronological fact rows."""

        collection, query = self._data_query(scope, area)
        keys = [TOTAL_CASES_KEY, "deceduti", "tamponi", "dimessi_guariti"]
        if scope == "provincial":
            keys = [TOTAL_CASES_KEY]
        rows = collection.find(query, {DATE_KEY: True, **{key: True for key in keys}}).sort(DATE_KEY, 1)
        values = {key: [] for key in keys}
        for row in rows:
            for key in keys:
                values[key].append(row.get(key, 0) or 0)
        return [
            {
                "id": key,
                "name": VARS.get(key, {}).get("title", key),
                "data": data,
            }
            for key, data in values.items()
            if data
        ]

    def _pandemic_rows(self, scope: Scope, area: str | None) -> list[dict[str, Any]]:
        """Return one chronological row per date for the selected dashboard."""

        collection, query = self._data_query(scope, area)
        rows_by_date: dict[Any, dict[str, Any]] = {}
        for row in collection.find(query).sort(DATE_KEY, 1):
            date = row.get(DATE_KEY)
            if date is not None:
                rows_by_date[date] = row
        return [rows_by_date[date] for date in sorted(rows_by_date)]

    def _daily_series(self, scope: Scope, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Build seven-day moving-average daily series from sanitized source rows."""

        if scope == "provincial":
            source = self._moving_average([self._number(row.get(NEW_POSITIVE_KEY)) for row in rows])
            return self._sort_series([self._series_item("nuovi_positivi_ma", source)])

        series = []
        for ma_key, daily_key, cumulative_key in DAILY_SERIES_KEYS:
            if cumulative_key:
                values = self._sanitized_delta(rows, cumulative_key)
            else:
                values = [self._number(row.get(daily_key)) for row in rows]
            series.append(self._series_item(ma_key, self._moving_average(values)))
        return self._sort_series(series)

    def _current_series(self, scope: Scope, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Build current-state chart series for national and regional dashboards."""

        if scope == "provincial":
            return []
        return self._sort_series(
            [self._series_item(key, [self._number(row.get(key)) for row in rows]) for key in CURRENT_SERIES_KEYS]
        )

    def _cumulative_series_from_rows(self, scope: Scope, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Build monotonic cumulative chart series from canonical rows."""

        keys = [TOTAL_CASES_KEY] if scope == "provincial" else CUMULATIVE_SERIES_KEYS
        return self._sort_series(
            [self._series_item(key, self._monotonic_values(rows, key)) for key in keys]
        )

    def _series_item(self, key: str, data: list[float]) -> dict[str, Any]:
        """Return one typed chart-series item with the configured display label."""

        return {"id": key, "name": VARS.get(key, {}).get("title", key), "data": data}

    def _sort_series(self, series: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Sort series by their visible maximum."""

        return sorted(series, key=lambda item: max(item["data"]) if item["data"] else 0, reverse=True)

    def _sanitized_delta(self, rows: list[dict[str, Any]], key: str) -> list[float]:
        """Compute daily deltas while ignoring temporary cumulative backtracks."""

        deltas: list[float] = []
        last_valid: float | None = None
        for row in rows:
            current = self._number(row.get(key))
            if last_valid is None:
                deltas.append(0)
                last_valid = current
                continue
            if current < last_valid:
                deltas.append(0)
                continue
            deltas.append(current - last_valid)
            last_valid = current
        return deltas

    def _monotonic_values(self, rows: list[dict[str, Any]], key: str) -> list[float]:
        """Return cumulative values without brief source backtracks."""

        values = []
        last_valid = 0.0
        for row in rows:
            current = self._number(row.get(key))
            if current >= last_valid:
                last_valid = current
            values.append(last_valid)
        return values

    def _moving_average(self, values: list[float], window: int = 7) -> list[float]:
        """Return a trailing moving average with a stable output length."""

        averages = []
        for index in range(len(values)):
            start = max(0, index - window + 1)
            window_values = values[start : index + 1]
            averages.append(round(sum(window_values) / len(window_values)))
        return averages

    def _number(self, value: Any) -> float:
        """Coerce numeric values to finite floats for chart math."""

        try:
            numeric = float(value or 0)
        except (TypeError, ValueError):
            return 0.0
        return numeric if numeric == numeric else 0.0

    def _percentage_label(self, value: Any) -> str:
        """Return a percentage label for already-computed ratio values."""

        if value in (None, "n/a", ""):
            return "n/a"
        try:
            return f"{float(value):.2f}%"
        except (TypeError, ValueError):
            return str(value) if str(value).endswith("%") else f"{value}%"

    def _iso_date(self, value: Any) -> str:
        """Return an ISO date string consumable by the D3 time axis."""

        if isinstance(value, (dt.datetime, dt.date)):
            return value.isoformat()
        return str(value)

    def _coerce_datetime(self, value: Any) -> dt.datetime | None:
        """Normalize date-like values for cross-table comparisons."""

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

    def _pandemic_breakdown(self, scope: Scope, area: str | None) -> dict[str, Any]:
        if scope == "provincial":
            return {}
        if scope == "national":
            doc = self.collections.regional_breakdown.find_one({}, {"_id": False}) or {}
            return clean_document(doc)
        doc = self.collections.provincial_breakdown.find_one({REGION_KEY: area}, {"_id": False}) or {}
        return clean_document(doc.get("breakdowns", {}))

    def _normalize_trend_card(self, card: dict[str, Any]) -> dict[str, Any]:
        normalized = clean_document(card)
        card_id = normalized.get("id")
        config = VARS.get(card_id, {})
        normalized.setdefault("title", config.get("title", card_id))
        normalized.setdefault("type", config.get("type", "daily"))
        normalized.setdefault("icon", config.get("icon", "fas fa-chart-line"))
        normalized["countLabel"] = number(normalized.get("count"))
        normalized["lastWeekCountLabel"] = number(normalized.get("last_week_count"))
        if normalized.get("last_week_dt"):
            normalized["lastWeekDateLabel"] = display_date(normalized.get("last_week_dt"))
        return normalized

    def _notes(self, doc: dict[str, Any]) -> str:
        note = doc.get(NOTE_KEY)
        return "" if note in (None, 0, "0") else str(note)

    def _dashboard_title(self, scope: Scope, area: str | None) -> str:
        if scope == "national":
            return "Italy"
        return area or "Italy"

    def _page_title(self, scope: Scope, area: str | None) -> str:
        return PAGE_BASE_TITLE if scope == "national" else f"{PAGE_BASE_TITLE} | {area}"

    def _province_region(self, province: str | None) -> str | None:
        for region, provinces in ITALY_MAP.items():
            if province in provinces:
                return region
        return None

    def _region_pop_dict(self) -> dict[str, int]:
        pipe = [{"$group": {"_id": {VAX_AREA_KEY: f"${VAX_AREA_KEY}"}, OD_POP_KEY: {"$sum": f"${OD_POP_KEY}"}}}]
        population = {
            OD_TO_PC_MAP.get(row["_id"][VAX_AREA_KEY], row["_id"][VAX_AREA_KEY]): row.get(OD_POP_KEY, 0)
            for row in self.collections.population.aggregate(pipe)
        }
        if population:
            return population

        # Fall back to the latest summary population by area when the
        # dedicated population table has not been loaded yet.
        fallback_pipe = [
            {"$match": {VAX_AREA_KEY: {"$ne": "ITA"}}},
            {"$group": {"_id": f"${VAX_AREA_KEY}", VAX_POP_KEY: {"$max": f"${VAX_POP_KEY}"}}},
        ]
        return {
            OD_TO_PC_MAP.get(row["_id"], row["_id"]): self._summary_population(row)
            for row in self.collections.vax_admins_summary.aggregate(fallback_pipe)
        }

    def _summary_population(self, row: dict[str, Any]) -> int:
        """Return population from vaccine summary rows normalized to people.

        Some source summaries store ``popolazione`` as a doubled value. When
        the dedicated population table is absent, this fallback halves the
        summary value to keep population-based KPIs in the expected range.
        """

        return int((row.get(VAX_POP_KEY, 0) or 0) / 2)

    def _area_population(self, area: str) -> int:
        pop = self._region_pop_dict()
        return int(pop.get(area, sum(pop.values())))

    def _age_pop_dict(self, od_area: str | None = None) -> dict[str, int]:
        match = [{"$match": {VAX_AREA_KEY: od_area}}] if od_area else []
        pipe = match + [{"$group": {"_id": {VAX_AGE_KEY: f"${VAX_AGE_KEY}"}, OD_POP_KEY: {"$sum": f"${OD_POP_KEY}"}}}]
        return {row["_id"][VAX_AGE_KEY]: row.get(OD_POP_KEY, 0) for row in self.collections.population.aggregate(pipe)}

    def _admins_percentage(self, od_area: str | None) -> float | str:
        query = {VAX_AREA_KEY: od_area} if od_area and od_area != "ITA" else {}
        rows = list(self.collections.vax_admins_summary.find(query))
        administered = sum(row.get(VAX_TOT_ADMINS_KEY, 0) or 0 for row in rows)
        delivered = sum(row.get("dosi_consegnate", 0) or 0 for row in rows)
        return round(administered / delivered * 100, 1) if delivered else "n/a"

    def _perc_pop_vax(self, population: int, od_area: str | None) -> dict[str, float | None]:
        def total(dtype: str) -> int:
            match = [{"$match": {VAX_AREA_KEY: od_area}}] if od_area and od_area != "ITA" else []
            pipe = match + [{"$group": {"_id": None, "tot": {"$sum": f"${dtype}"}}}]
            row = next(self.collections.vax_admins_summary.aggregate(pipe), {})
            return int(row.get("tot", 0))

        if population == 0:
            return {"first": None, "second": None, "booster": None}
        return {
            "first": round(total(VAX_FIRST_DOSE_KEY) / population * 100, 1),
            "second": round(total(VAX_SECOND_DOSE_KEY) / population * 100, 1),
            "booster": round(total(VAX_BOOSTER_DOSE_KEY) / population * 100, 1),
        }

    def _vax_trends(self, od_area: str | None = None) -> list[dict[str, Any]]:
        match = [{"$match": {VAX_AREA_KEY: od_area}}] if od_area else []
        pipe = match + [{"$group": {"_id": f"${VAX_DATE_KEY}", VAX_FIRST_DOSE_KEY: {"$sum": f"${VAX_FIRST_DOSE_KEY}"}, VAX_SECOND_DOSE_KEY: {"$sum": f"${VAX_SECOND_DOSE_KEY}"}, VAX_BOOSTER_DOSE_KEY: {"$sum": f"${VAX_BOOSTER_DOSE_KEY}"}}}, {"$sort": {"_id": -1}}, {"$limit": 7}]
        data = list(self.collections.vax_admins.aggregate(pipe))
        trends = []
        for dose in VAX_DOSES:
            if len(data) < 2:
                continue
            count = data[0].get(dose, 0)
            baseline = data[-1].get(dose, 0)
            diff = count - baseline
            status_name = "increase" if diff > 0 else "decrease" if diff < 0 else "stable"
            status_config = VARS[dose][status_name]
            trends.append({
                "id": dose,
                "title": VARS[dose]["title"],
                "icon": VARS[dose]["icon"],
                "count": count,
                "countLabel": number(count),
                "last_week_count": baseline,
                "lastWeekCountLabel": number(baseline),
                "last_week_dt": display_date(data[-1].get("_id")),
                "comparisonLabel": "vs previous sample",
                "percentage": f"{round(diff / baseline * 100)}%" if baseline else "n/a",
                "colour": status_config["colour"],
                "status_icon": status_config["icon"],
            })
        return trends

    def _latest_vaccine_update(self) -> str:
        summary_doc = self.collections.vax_admins_summary.find_one({}, sort=[(VAX_DATE_KEY, -1)]) or {}
        admins_doc = self.collections.vax_admins.find_one({}, sort=[(VAX_DATE_KEY, -1)]) or {}
        candidates = [
            self._coerce_datetime(summary_doc.get(VAX_DATE_KEY)),
            self._coerce_datetime(admins_doc.get(VAX_DATE_KEY)),
        ]
        latest = max((candidate for candidate in candidates if candidate is not None), default=None)
        return display_date(latest)
