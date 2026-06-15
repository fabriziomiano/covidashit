"""Extract orchestration for Italia Open Data vaccination data."""

from dataclasses import dataclass

import pandas as pd

from covidashflow.common.dataframes import read_csv_frame
from covidashflow.common.logging import get_logger
from covidashflow.common.urls import (
    URL_VAX_ADMINS_DATA,
    URL_VAX_ADMINS_SUMMARY_DATA,
    URL_VAX_POP_DATA,
)
from covidashflow.common.vars import VAX_DATE_KEY

logger = get_logger(__name__)


@dataclass(frozen=True)
class OpenDataSources:
    """Source URLs for all Italia Open Data vaccination datasets."""

    vax_admins_url: str = URL_VAX_ADMINS_DATA
    vax_admins_summary_url: str = URL_VAX_ADMINS_SUMMARY_DATA
    population_url: str = URL_VAX_POP_DATA


def extract_opendata_frame(
    url: str,
    *,
    parse_dates: bool = False,
    low_memory: bool = True,
) -> pd.DataFrame:
    """Read an Italia Open Data CSV source into a timestamped dataframe."""
    logger.info("Extracting Open Data at %s", url)
    df = read_csv_frame(
        url,
        date_column=VAX_DATE_KEY if parse_dates else None,
        low_memory=low_memory,
    )
    logger.info("Read %s Open Data records", len(df.index))
    return df
