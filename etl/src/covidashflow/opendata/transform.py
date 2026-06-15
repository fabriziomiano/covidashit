"""Transform Italia Open Data vaccination data into warehouse-ready records."""

import pandas as pd

from covidashflow.common.geo import OD_TO_PC_MAP
from covidashflow.common.vars import (
    F_SEX_KEY,
    M_SEX_KEY,
    OD_NUTS1_KEY,
    OD_NUTS2_KEY,
    OD_POP_KEY,
    OD_REGION_CODE,
    POP_KEY,
    VAX_AGE_KEY,
    VAX_AREA_KEY,
    VAX_DATE_FMT,
    VAX_DATE_KEY,
    VAX_PROVIDER_KEY,
)
from covidashflow.common.logging import get_logger

logger = get_logger(__name__)

VAX_GROUP_COLUMNS = [
    VAX_DATE_KEY,
    VAX_PROVIDER_KEY,
    VAX_AREA_KEY,
    VAX_AGE_KEY,
    OD_NUTS1_KEY,
    OD_NUTS2_KEY,
    OD_REGION_CODE,
]
AGE_BUCKET_REPLACEMENTS = {"80-89": "80+", "90+": "80+"}


def get_region_pop_dict(pop_collection) -> dict:
    """Return a PCM-DPC region-name to population mapping from records."""
    it_pop_dict = {}
    try:
        pop_pipe = [
            {
                "$group": {
                    "_id": {VAX_AREA_KEY: f"${VAX_AREA_KEY}"},
                    f"{OD_POP_KEY}": {"$sum": f"${OD_POP_KEY}"},
                },
            }
        ]
        records = list(pop_collection.aggregate(pipeline=pop_pipe))
        it_pop_dict = {
            OD_TO_PC_MAP[r["_id"][VAX_AREA_KEY]]: r[OD_POP_KEY] for r in records
        }
    except Exception as e:
        logger.error(f"While getting region pop dict: {e}")
    return it_pop_dict


def preprocess_vax_admins_df(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize, group, and identify vaccination administration records."""
    df = df.copy()
    df[VAX_AGE_KEY] = df[VAX_AGE_KEY].str.strip().replace(AGE_BUCKET_REPLACEMENTS)
    df = (
        df.groupby(by=VAX_GROUP_COLUMNS, sort=False)
        .sum(numeric_only=True)
        .reset_index()
    )
    df["totale"] = df[M_SEX_KEY] + df[F_SEX_KEY]
    df["_id"] = (
        df[VAX_DATE_KEY].dt.strftime(VAX_DATE_FMT)
        + df[VAX_AREA_KEY]
        + df[VAX_AGE_KEY]
        + df[VAX_PROVIDER_KEY]
    )
    return df


def preprocess_vax_admins_summary_df(
    df: pd.DataFrame,
    population: dict = None,
) -> pd.DataFrame:
    """Resample vaccination summaries per area and attach population totals."""
    population = population or {}
    summary_frames = []
    for _, area_df in df.groupby(VAX_AREA_KEY, sort=False):
        area_df = area_df.set_index(VAX_DATE_KEY).resample("1D").asfreq()
        summary_frames.append(_fill_resampled_summary(area_df))

    out_df = pd.concat(summary_frames)
    out_df.reset_index(inplace=True)
    out_df["_id"] = out_df[VAX_DATE_KEY].dt.strftime(VAX_DATE_FMT) + out_df[VAX_AREA_KEY]
    out_df[POP_KEY] = out_df[VAX_AREA_KEY].apply(lambda x: population[OD_TO_PC_MAP[x]])
    return out_df


def _fill_resampled_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing resampled summary values using original column semantics."""
    df = df.copy()
    for col in df.columns:
        non_null_values = df[col].dropna()
        last_value = non_null_values.iloc[-1] if not non_null_values.empty else None
        if isinstance(last_value, str):
            df[col] = df[col].ffill()
        else:
            df[col] = df[col].fillna(0.0)
    return df
