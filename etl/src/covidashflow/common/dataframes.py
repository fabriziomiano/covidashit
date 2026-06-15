"""Small dataframe IO and cleanup helpers shared by ETL pipelines."""

import datetime as dt
from typing import List, Optional

import pandas as pd


def read_csv_frame(
    url: str,
    *,
    date_column: Optional[str] = None,
    low_memory: bool = False,
    drop_columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Read a CSV source into a dataframe and stamp extraction time."""
    read_kwargs = {"low_memory": low_memory}
    if date_column:
        read_kwargs["parse_dates"] = [date_column]

    df = pd.read_csv(url, **read_kwargs)

    if drop_columns:
        df = df.drop(columns=drop_columns)

    df["extracted_at"] = dt.datetime.now()
    return df


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Replace null-like values with zeros in a dataframe."""
    return df.where(pd.notnull(df), None).fillna(value=0)
