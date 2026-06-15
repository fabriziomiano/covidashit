"""Extract orchestration for PCM-DPC COVID-19 data."""

from dataclasses import dataclass

import pandas as pd

from covidashflow.common.dataframes import read_csv_frame
from covidashflow.common.logging import get_logger
from covidashflow.common.urls import URL_NATIONAL, URL_PROVINCIAL, URL_REGIONAL
from covidashflow.common.vars import DATE_KEY
from covidashflow.dpc.transform import COLUMNS_TO_DROP

logger = get_logger(__name__)


@dataclass(frozen=True)
class DpcSources:
    """Source URLs for all PCM-DPC datasets consumed by the pipeline."""

    national_url: str = URL_NATIONAL
    regional_url: str = URL_REGIONAL
    provincial_url: str = URL_PROVINCIAL


def extract_dpc_frame(
    url: str,
    *,
    parse_dates: bool = True,
    drop_columns: bool = False,
) -> pd.DataFrame:
    """Read a PCM-DPC CSV source into a timestamped dataframe."""
    logger.info("Extracting DPC data at %s", url)
    df = read_csv_frame(
        url,
        date_column=DATE_KEY if parse_dates else None,
        low_memory=False,
        drop_columns=COLUMNS_TO_DROP if drop_columns else None,
    )
    logger.info("Read %s DPC records", len(df.index))
    return df
