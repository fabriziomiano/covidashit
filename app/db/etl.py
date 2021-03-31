"""
Where the ETL happens
"""
import pandas as pd
from flask import current_app as app

from app.data import (
    CUM_QUANTITIES, NON_CUM_QUANTITIES, DAILY_QUANTITIES, TREND_CARDS,
    PROV_TREND_CARDS
)
from constants import (
    VARS, DAILY_POSITIVITY_INDEX, NEW_POSITIVE_KEY, DAILY_SWABS_KEY,
    REGION_CODE, PROVINCE_CODE, TOTAL_CASES_KEY, REGION_KEY, PROVINCE_KEY,
    REGIONS, PROVINCES, DATE_KEY, CHART_DATE_FMT, STATE_KEY,
    NEW_POSITIVE_MA_KEY, VAX_AGE_KEY, M_SEX_KEY, F_SEX_KEY, VAX_DATE_KEY,
    VAX_DATE_FMT, VAX_AREA_KEY, VAX_TYPE_KEY, ITALY_POPULATION, OD_TO_PC_MAP,
    POP_KEY
)

COLUMNS_TO_DROP = [STATE_KEY]


def load_df(url):
    """
    Return a CP dataframe without the columns defined in COLUMNS_TO_DROP
    :param url: str: CP-repository data URL
    :return: pd.DataFrame
    """
    df = pd.read_csv(url, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
    return df


def add_delta(df):
    """
    Add a difference column "*_g" for all the daily-type variables in VARS
    that also exist in df
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    columns = [
        col for col in VARS if VARS[col]["type"] != "daily"
    ]
    for col in columns:
        try:
            df[col + "_g"] = df[col].diff()
        except KeyError:
            continue
    return df


def add_percentages(df):
    """
    Add a percentage column "*_perc" for all the variables in VARS that exists
    in df
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    for col in VARS:
        try:
            diff_df = df[col].diff()
            df[col + "_perc"] = diff_df.div(df[col].shift(1).abs()) * 100
        except KeyError:
            continue
    return df


def add_positivity_idx(df):
    """
    Add a DAILY_POSITIVITY_INDEX as NEW_POSITIVE_KEY / DAILY_SWABS_KEY * 100
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    df[DAILY_POSITIVITY_INDEX] = (
            df[NEW_POSITIVE_KEY].div(df[DAILY_SWABS_KEY]) * 100)
    return df


def add_moving_avg(df):
    """Add weekly moving average to the daily quantities"""
    cols = [
        col for col in VARS
        if VARS[col]["type"] == "daily" and not col.endswith("_ma")
    ]
    for col in cols:
        try:
            df[col + '_ma'] = df[col].rolling(7).mean()
            df[col + '_ma'] = clean_df(df[col + '_ma'])
            df[col + '_ma'] = df[col + '_ma'].astype(int)
        except KeyError:
            continue
    return df


def clean_df(df):
    """
    Replace all nan values with None and then with 0
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    df = df.where(pd.notnull(df), None)
    df = df.fillna(value=0)
    return df


def augment_national_df(df):
    """
    Augment the national PC DataFrame:
     add the delta, the percentages, and the positivity index
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    df_augmented = df.copy()
    df_augmented = add_delta(df_augmented)
    df_augmented = add_moving_avg(df_augmented)
    df_augmented = add_percentages(df_augmented)
    df_augmented = add_positivity_idx(df_augmented)
    df_augmented = clean_df(df_augmented)
    return df_augmented


def augment_regional_df(df):
    """
    Augment the regional PC DataFrame:
     add the delta, the percentages, and the positivity index to every
     region sub-df
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    dfs = []
    for cr in set(df[REGION_CODE]):
        df_region = df[df[REGION_CODE] == cr].copy()
        df_region = add_delta(df_region)
        df_region = add_moving_avg(df_region)
        df_region = add_percentages(df_region)
        df_region = add_positivity_idx(df_region)
        dfs.append(df_region)
    df_augmented = pd.concat(dfs)
    df_augmented = clean_df(df_augmented)
    return df_augmented


def augment_provincial_df(df):
    """
    Augment the provincial PC DataFrame:
     add the new positive and the relevant percentage
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    dfs = []
    for cp in set(df[PROVINCE_CODE]):
        dfp = df[df[PROVINCE_CODE] == cp].copy()
        dfp[NEW_POSITIVE_KEY] = dfp[TOTAL_CASES_KEY].diff()
        df_new_pos_diff = dfp[NEW_POSITIVE_KEY].diff()
        dfp["nuovi_positivi_perc"] = df_new_pos_diff.div(
            dfp[NEW_POSITIVE_KEY].shift(1).abs()) * 100
        dfp["totale_casi_perc"] = (
                dfp[NEW_POSITIVE_KEY].div(
                    dfp[TOTAL_CASES_KEY].shift(1).abs()) * 100)
        dfp = add_moving_avg(dfp)
        dfs.append(dfp)
    df_augmented = pd.concat(dfs)
    df_augmented = clean_df(df_augmented)
    return df_augmented


def build_trend(df, col):
    """
    Return a trend object for a given df and variable col
    :param df: pd.DataFrame
    :param col: str
    :return: dict
    """
    status = "stable"
    perc_col = col + "_perc"
    df[col] = df[col].astype('int')
    count = df[col].to_numpy()[-1]
    yesterday_count = df[col].to_numpy()[-2]
    if VARS[col]["type"] in ("daily", "current", "cum"):
        count = "{0:+,d}".format(count)
        yesterday_count = "{0:+,d}".format(yesterday_count)
    try:
        df[perc_col].dropna(inplace=True)
        p = df[perc_col].to_numpy()[-1]
        percentage = "{0:+}%".format(round(p))
    except (OverflowError, TypeError):
        percentage = "n/a"
    if count < yesterday_count:
        status = "decrease"
    if count > yesterday_count:
        status = "increase"
    if count == yesterday_count:
        status = "stable"
    trend = {
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
        "yesterday_count": yesterday_count
    }
    return trend


def build_national_trends(df):
    """
    Return the list of national-trend variables for a given national df
    :param df: pd.DataFrame
    :return: list
    """
    trends = []
    for col in TREND_CARDS:
        try:
            t = build_trend(df, col)
            trends.append(t)
        except Exception as e:
            app.logger.error(f"{e}")
            continue
    return trends


def build_regional_trends(df):
    """
    Return the list of regional-trend variables for a given regional df
    :param df: pd.DataFrame
    :return: list
    """
    trends = []
    for cr in set(df[REGION_CODE]):
        df_r = df[df[REGION_CODE] == cr].copy()
        trend = {
            REGION_KEY: df_r[REGION_KEY].to_numpy()[-1],
            "trends": build_national_trends(df_r)
        }
        trends.append(trend)
    return trends


def build_provincial_trends(df):
    """
    Return the list of provincial-trend variables for a given provincial df
    :param df: pd.DataFrame
    :return: list
    """
    trends = []
    for cp in set(df[PROVINCE_CODE]):
        province_trends = []
        df_province = df[df[PROVINCE_CODE] == cp].copy()
        for col in PROV_TREND_CARDS:
            try:
                trend = build_trend(df_province, col)
                province_trends.append(trend)
            except KeyError as e:
                app.logger.error(f"Error in build_provincial_trends: {e}")
                continue
        trends.append({
            PROVINCE_KEY: df_province[PROVINCE_KEY].to_numpy()[-1],
            "trends": province_trends
        })
    return trends


def build_regional_breakdown(df):
    """
    Return a regional breakdown object for a given regional df
    :param df: pd.DataFrame
    :return: dict
    """
    breakdown = {}
    sub_url = 'regions'
    for col in TREND_CARDS:
        breakdown[col] = []
        for code in set(df[REGION_CODE]):
            df_area = df[df[REGION_CODE] == code].copy()
            area = df_area[REGION_KEY].to_numpy()[-1]
            if area not in REGIONS:
                continue
            count = int(df_area[col].to_numpy()[-1])
            url = "/{}/{}".format(sub_url, df_area[REGION_KEY].to_numpy()[-1])
            b = {
                "area": area,
                "count": count,
                "url": url
            }
            breakdown[col].append(b)
    return breakdown


def build_provincial_breakdowns(df):
    """
    Return a list of breakdown objects for all the provinces in
     a given provincial df
    :param df: pd.DataFrame
    :return: list
    """
    breakdowns = []
    for cr in set(df[REGION_CODE]):
        df_region = df[df[REGION_CODE] == cr].copy()
        region = df_region[REGION_KEY].to_numpy()[-1]
        if region not in REGIONS:
            continue
        breakdown = {
            REGION_KEY: region,
            "breakdowns": {}
        }
        for col in PROV_TREND_CARDS:
            breakdown["breakdowns"][col] = []
            for cp in set(df_region[PROVINCE_CODE]):
                df_province = df_region[df_region[PROVINCE_CODE] == cp].copy()
                province = df_province[PROVINCE_KEY].to_numpy()[-1]
                if province not in PROVINCES:
                    continue
                count = int(df_province[col].to_numpy()[-1])
                url = f"/provinces/{province}"
                prov_col_dict = {
                    "area": province,
                    "count": count,
                    "url": url
                }
                breakdown["breakdowns"][col].append(prov_col_dict)
        breakdowns.append(breakdown)
    return breakdowns


def build_series(df):
    """
    Return a series tuple where:
    the first element is a list of dates,
    the second element is the series of the daily-type variables,
    the third element is the series of the current-type variables,
    the fourth element is the series of the cum-type variables.
    :param df: pd.DataFrame
    :return: tuple
    """
    dates = df[DATE_KEY].apply(lambda x: x.strftime(CHART_DATE_FMT)).tolist()
    series_daily = sorted([
        {
            "id": col,
            "name": VARS[col]["title"],
            "data": df[col].to_numpy().tolist()
        }
        for col in DAILY_QUANTITIES
    ], key=lambda x: max(x[DATE_KEY]), reverse=True)
    series_cum = sorted([
        {
            "id": col,
            "name": VARS[col]["title"],
            "data": df[col].to_numpy().tolist()
        }
        for col in CUM_QUANTITIES
    ], key=lambda x: max(x[DATE_KEY]), reverse=True)
    series_current = sorted([
        {
            "id": col,
            "name": VARS[col]["title"],
            "data": df[col].to_numpy().tolist()
        }
        for col in NON_CUM_QUANTITIES
    ], key=lambda x: max(x[DATE_KEY]), reverse=True)
    series = (dates, series_daily, series_current, series_cum)
    return series


def build_national_series(df):
    """
    Return a series object for a given national df
    :param df: pd.DataFrame
    :return: dict
    """
    data_series = build_series(df)
    series = {
        "dates": data_series[0],
        "daily": data_series[1],
        "current": data_series[2],
        "cum": data_series[3]
    }
    return series


def build_regional_series(df):
    """
    Return a list of series object for each region in a given regional df.
    :param df: pd.DataFrame
    :return: list
    """
    regional_series = []
    for cr in set(df[REGION_CODE]):
        df_area = df[df[REGION_CODE] == cr].copy()
        series = build_series(df_area)
        regional_series.append({
            REGION_KEY: df_area[REGION_KEY].to_numpy()[-1],
            "dates": series[0],
            "daily": series[1],
            "current": series[2],
            "cum": series[3]
        })
    return regional_series


def build_provincial_series(df):
    """
    Return a list of series object for each province in a given provincial df.
    :param df: pd.DataFrame
    :return: list
    """
    provincial_series = []
    for cp in set(df[PROVINCE_CODE]):
        df_area = df[df[PROVINCE_CODE] == cp].copy()
        dates = df_area[DATE_KEY].apply(
            lambda x: x.strftime(CHART_DATE_FMT)).tolist()
        series_daily = [
            {
                "id": var,
                "name": VARS[var]["title"],
                "data": df_area[var].to_numpy().tolist()
            }
            for var in [NEW_POSITIVE_KEY, NEW_POSITIVE_MA_KEY]
        ]
        series_cum = [
            {
                "id": TOTAL_CASES_KEY,
                "name": VARS[TOTAL_CASES_KEY]["title"],
                "data": df_area[TOTAL_CASES_KEY].to_numpy().tolist()
            }
        ]
        provincial_series.append({
            PROVINCE_KEY: df_area[PROVINCE_KEY].to_numpy()[-1],
            "dates": dates,
            "daily": series_daily,
            "cum": series_cum
        })
    return provincial_series


def augment_vax_df(df):
    """
    Return a modified version of the input df.
    Add two columns '_id' and 'totale'.
    The former is computed as the concatenation of three strings
    VAX_DATE_KEY + VAX_AGE_KEY + VAX_TYPE_KEY, and the latter as the sum of
    the columns M_SEX_KEY + F_SEX_KEY
    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """
    df[VAX_AGE_KEY] = df[VAX_AGE_KEY].apply(lambda x: x.strip())
    df['totale'] = df[M_SEX_KEY] + df[F_SEX_KEY]
    df['_id'] = (
            df[VAX_DATE_KEY].apply(lambda x: x.strftime(VAX_DATE_FMT)) +
            df[VAX_AREA_KEY] +
            df[VAX_AGE_KEY] +
            df[VAX_TYPE_KEY]
    )
    return df


def augment_summary_vax_df(df):
    """
    Return a modified version of the input df.
    Add two columns '_id' and POP_TOT_KEY.
    The former is computed as the concatenation of two strings
    VAX_DATE_KEY + VAX_AREA_KEY, and the latter is taken from the
    ITALY_POPULATION dict.
    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """
    out_df = pd.DataFrame()
    for r in df[VAX_AREA_KEY].unique():
        reg_df = df[df[VAX_AREA_KEY] == r]
        reg_df = reg_df.set_index(VAX_DATE_KEY).resample('1D').asfreq()
        for col in reg_df:
            if isinstance(reg_df[col].to_numpy()[-1], str):
                reg_df[col].ffill(inplace=True)
        else:
            reg_df.fillna(0, inplace=True)
        out_df = out_df.append(reg_df)
    out_df.reset_index(inplace=True)
    out_df['_id'] = (
            out_df[VAX_DATE_KEY].apply(
                lambda x: x.strftime(VAX_DATE_FMT)) + out_df[VAX_AREA_KEY]
    )
    out_df[POP_KEY] = out_df[VAX_AREA_KEY].apply(
        lambda x: ITALY_POPULATION[OD_TO_PC_MAP[x]])
    return out_df
