"""Transform PCM-DPC COVID-19 dataframes into warehouse-ready records."""

from __future__ import annotations

import pandas as pd
from covidashflow.common.geo import PROVINCES, REGIONS
from covidashflow.common.vars import (
    DAILY_QUANTITIES,
    DAILY_SWABS_KEY,
    DATE_KEY,
    NEW_POSITIVE_KEY,
    NEW_POSITIVE_MA_KEY,
    NON_CUM_QUANTITIES,
    POSITIVITY_INDEX,
    PROV_TREND_CARDS,
    PROVINCE_CODE,
    PROVINCE_KEY,
    REGION_CODE,
    REGION_KEY,
    STATE_KEY,
    TOTAL_CASES_KEY,
    TOTAL_DEATHS_KEY,
    TOTAL_HEALED_KEY,
    TOTAL_SWABS_KEY,
    TREND_CARDS,
    VARS,
)
from covidashflow.common.logging import get_logger

COLUMNS_TO_DROP = [STATE_KEY]
DELTA_SOURCE_COLUMNS = [col for col, meta in VARS.items() if meta["type"] != "daily"]
MOVING_AVERAGE_SOURCE_COLUMNS = [
    col for col, meta in VARS.items() if meta["type"] == "daily" and not col.endswith("_ma")
]
REGION_SET = set(REGIONS)
PROVINCE_SET = set(PROVINCES)
CUMULATIVE_DELTA_COLUMNS = {
    TOTAL_CASES_KEY,
    TOTAL_DEATHS_KEY,
    TOTAL_HEALED_KEY,
    TOTAL_SWABS_KEY,
}


logger = get_logger(__name__)


def add_delta(df: pd.DataFrame) -> pd.DataFrame:
    """Add daily delta columns for cumulative and current DPC quantities."""
    for col in _available_columns(df, DELTA_SOURCE_COLUMNS):
        if col in CUMULATIVE_DELTA_COLUMNS:
            df[f"{col}_g"] = _safe_cumulative_diff(df[col])
        else:
            df[f"{col}_g"] = df[col].diff()
    return df


def add_percentages(df: pd.DataFrame) -> pd.DataFrame:
    """Add seven-day percentage-difference columns for available DPC variables."""
    for col in _available_columns(df, VARS.keys()):
        diff_df = df[col].diff(periods=7)
        df[f"{col}_perc"] = diff_df.div(df[col].shift(7).abs()) * 100
    return df


def add_positivity_idx(df: pd.DataFrame) -> pd.DataFrame:
    """Add positivity index as new positives divided by daily swabs."""
    df[POSITIVITY_INDEX] = (df[NEW_POSITIVE_KEY].div(df[DAILY_SWABS_KEY]) * 100).round(
        decimals=2
    )
    return df


def add_moving_avg(df: pd.DataFrame) -> pd.DataFrame:
    """Add integer seven-day moving averages for available daily quantities."""
    for col in _available_columns(df, MOVING_AVERAGE_SOURCE_COLUMNS):
        moving_average_col = f"{col}_ma"
        df[moving_average_col] = clean_df(df[col].rolling(7).mean()).astype(int)
    return df


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Replace null-like values with zero while preserving dataframe shape."""
    return df.where(pd.notnull(df), None).fillna(value=0)


def preprocess_national_df(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess national DPC records with deltas, averages, percentages, and positivity."""
    df = _sort_and_dedupe(df.copy(), [DATE_KEY])
    df = add_delta(df)
    df = add_moving_avg(df)
    df = add_percentages(df)
    df = add_positivity_idx(df)
    return clean_df(df)


def preprocess_regional_df(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess regional DPC records independently per region code."""
    df = _sort_and_dedupe(df, [REGION_CODE, DATE_KEY])
    regional_frames = []
    for _, df_region in df.groupby(REGION_CODE, sort=False):
        df_region = df_region.copy()
        df_region = add_delta(df_region)
        df_region = add_moving_avg(df_region)
        df_region = add_percentages(df_region)
        df_region = add_positivity_idx(df_region)
        regional_frames.append(df_region)
    return clean_df(pd.concat(regional_frames))


def preprocess_provincial_df(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess provincial DPC records independently per province code."""
    df = df.rename(columns=lambda x: x.strip())
    df = _sort_and_dedupe(df, [PROVINCE_CODE, DATE_KEY])
    provincial_frames = []
    for _, province_df in df.groupby(PROVINCE_CODE, sort=False):
        province_df = province_df.copy()
        province_df[NEW_POSITIVE_KEY] = province_df[TOTAL_CASES_KEY].diff()
        new_positive_diff = province_df[NEW_POSITIVE_KEY].diff(periods=7)
        province_df["nuovi_positivi_perc"] = (
            new_positive_diff.div(province_df[NEW_POSITIVE_KEY].shift(7).abs()) * 100
        )
        province_df["totale_casi_perc"] = (
            province_df[NEW_POSITIVE_KEY].div(province_df[TOTAL_CASES_KEY].shift(7).abs())
            * 100
        )
        province_df = add_moving_avg(province_df)
        provincial_frames.append(province_df)
    return clean_df(pd.concat(provincial_frames))


def build_trend(df: pd.DataFrame, col: str) -> dict:
    """Build one trend-card document for a DPC metric column."""
    values = df[col].astype(int).to_numpy()
    count = values[-1].item()
    last_week_count = values[-8].item()
    percentage_values = df[f"{col}_perc"].dropna().to_numpy()
    try:
        percentage = f"{round(percentage_values[-1])}%"
    except (IndexError, OverflowError, TypeError):
        percentage = "n/a"

    status = _trend_status(count, last_week_count)
    return {
        "id": col,
        "type": VARS[col]["type"],
        "title": VARS[col]["title"],
        "desc": VARS[col]["desc"],
        "longdesc": VARS[col]["longdesc"],
        "count": count,
        "colour": VARS[col][status]["colour"],
        "icon": VARS[col]["icon"],
        "status_icon": VARS[col][status]["icon"],
        "tooltip": VARS[col][status]["tooltip"],
        "percentage_difference": percentage,
        "last_week_count": last_week_count,
        "last_week_dt": df[DATE_KEY].iloc[-8],
    }


def build_national_trends(df: pd.DataFrame) -> list:
    """Build all national trend-card documents available in the dataframe."""
    trends = []
    for col in TREND_CARDS:
        try:
            trends.append(build_trend(df, col))
        except Exception as e:
            logger.error(f"{e}")
            continue
    return trends


def build_regional_trends(df: pd.DataFrame) -> list:
    """Build trend-card documents for every region in a regional DPC dataframe."""
    trends = []
    for _, region_df in df.groupby(REGION_CODE, sort=False):
        trends.append(
            {
                REGION_KEY: region_df[REGION_KEY].to_numpy()[-1],
                "trends": build_national_trends(region_df),
            }
        )
    return trends


def build_provincial_trends(df: pd.DataFrame) -> list:
    """Build trend-card documents for every province in a provincial dataframe."""
    trends = []
    for _, province_df in df.groupby(PROVINCE_CODE, sort=False):
        province_trends = []
        for col in PROV_TREND_CARDS:
            try:
                province_trends.append(build_trend(province_df, col))
            except KeyError as e:
                logger.error(f"Error in build_provincial_trends: {e}")
                continue
        trends.append(
            {
                PROVINCE_KEY: province_df[PROVINCE_KEY].to_numpy()[-1],
                "trends": province_trends,
            }
        )
    return trends


def build_regional_breakdown(df: pd.DataFrame) -> dict:
    """Build metric-to-region breakdown documents for the latest regional rows."""
    breakdown = {}
    latest_regions = _latest_by_group(df, REGION_CODE)
    for col in TREND_CARDS:
        breakdown[col] = []
        for _, row in latest_regions.iterrows():
            area = row[REGION_KEY]
            if area not in REGION_SET:
                continue
            breakdown[col].append(
                {"area": area, "count": int(row[col]), "url": f"/regions/{area}"}
            )
    return breakdown


def build_provincial_breakdowns(df: pd.DataFrame) -> list:
    """Build per-region provincial metric breakdown documents."""
    breakdowns = []
    latest_provinces = _latest_by_group(df, PROVINCE_CODE)
    for _, region_df in latest_provinces.groupby(REGION_CODE, sort=False):
        region = region_df[REGION_KEY].to_numpy()[-1]
        if region not in REGION_SET:
            continue
        breakdown = {REGION_KEY: region, "breakdowns": {}}
        for col in PROV_TREND_CARDS:
            breakdown["breakdowns"][col] = []
            for _, row in region_df.iterrows():
                province = row[PROVINCE_KEY]
                if province not in PROVINCE_SET:
                    continue
                breakdown["breakdowns"][col].append(
                    {"area": province, "count": int(row[col]), "url": f"/provinces/{province}"}
                )
        breakdowns.append(breakdown)
    return breakdowns


def build_series(df: pd.DataFrame) -> tuple:
    """Build shared date, daily-series, and current-series chart payloads."""
    dates = df[DATE_KEY].to_list()
    series_daily = sorted(
        [
            {"id": col, "name": VARS[col]["title"], "data": df[col].tolist()}
            for col in _available_columns(df, DAILY_QUANTITIES)
        ],
        key=lambda x: max(x["data"]),
        reverse=True,
    )
    series_current = sorted(
        [
            {"id": col, "name": VARS[col]["title"], "data": df[col].tolist()}
            for col in _available_columns(df, NON_CUM_QUANTITIES)
        ],
        key=lambda x: max(x["data"]),
        reverse=True,
    )
    series = (dates, series_daily, series_current)
    return series


def build_national_series(df: pd.DataFrame) -> dict:
    """Build the national chart-series document."""
    data_series = build_series(df)
    return {
        "dates": data_series[0],
        "daily": data_series[1],
        "current": data_series[2],
    }


def build_regional_series(df: pd.DataFrame) -> list:
    """Build chart-series documents for every region."""
    regional_series = []
    for _, area_df in df.groupby(REGION_CODE, sort=False):
        series = build_series(area_df)
        regional_series.append(
            {
                REGION_KEY: area_df[REGION_KEY].to_numpy()[-1],
                "dates": series[0],
                "daily": series[1],
                "current": series[2],
            }
        )
    return regional_series


def build_provincial_series(df: pd.DataFrame) -> list:
    """Build chart-series documents for every province."""
    provincial_series = []
    for _, area_df in df.groupby(PROVINCE_CODE, sort=False):
        dates = area_df[DATE_KEY].to_list()
        series_daily = [
            {
                "id": NEW_POSITIVE_MA_KEY,
                "name": VARS[NEW_POSITIVE_MA_KEY]["title"],
                "data": area_df[NEW_POSITIVE_MA_KEY].to_numpy().tolist(),
            }
        ]
        series_cum = [
            {
                "id": TOTAL_CASES_KEY,
                "name": VARS[TOTAL_CASES_KEY]["title"],
                "data": area_df[TOTAL_CASES_KEY].to_numpy().tolist(),
            }
        ]
        provincial_series.append(
            {
                PROVINCE_KEY: area_df[PROVINCE_KEY].to_numpy()[-1],
                "dates": dates,
                "daily": series_daily,
                "cum": series_cum,
            }
        )
    return provincial_series


def _available_columns(df: pd.DataFrame, columns) -> list:
    """Return configured columns that are present in a dataframe."""
    return [col for col in columns if col in df.columns]


def _latest_by_group(df: pd.DataFrame, group_column: str) -> pd.DataFrame:
    """Return the last observed row for each group, preserving source order."""
    return df.groupby(group_column, sort=False).tail(1)


def _safe_cumulative_diff(series: pd.Series) -> pd.Series:
    """Diff cumulative data while ignoring temporary backwards corrections."""

    deltas = []
    last_valid = None
    for value in series:
        if pd.isna(value):
            deltas.append(0)
            continue
        if last_valid is None:
            deltas.append(0)
            last_valid = value
            continue
        if value < last_valid:
            deltas.append(0)
            continue
        deltas.append(value - last_valid)
        last_valid = value
    return pd.Series(deltas, index=series.index)


def _sort_and_dedupe(df: pd.DataFrame, subset: list[str]) -> pd.DataFrame:
    """Sort rows chronologically and keep one source record per date/group."""

    sort_columns = [col for col in subset if col in df.columns]
    if DATE_KEY in df.columns and DATE_KEY not in sort_columns:
        sort_columns.append(DATE_KEY)
    return df.sort_values(sort_columns).drop_duplicates(subset=subset, keep="last").reset_index(drop=True)


def _trend_status(count: int, last_week_count: int) -> str:
    """Classify a metric as increase, decrease, or stable against last week."""
    if count < last_week_count:
        return "decrease"
    if count > last_week_count:
        return "increase"
    return "stable"
