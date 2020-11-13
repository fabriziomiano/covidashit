import pandas as pd

from config import (
    CP_DATE_FMT, VARS_CONFIG, REGION_KEY, PROVINCE_KEY,
    PROVINCE_CODE, REGION_CODE, PROVINCES, REGIONS, DATE_KEY, CHART_DATE_FMT
)

CUM_QUANTITIES = [
    qty for qty in VARS_CONFIG
    if VARS_CONFIG[qty]["type"] == "cum"]
NON_CUM_QUANTITIES = [
    qty for qty in VARS_CONFIG
    if VARS_CONFIG[qty]["type"] == "current"]
NON_CUM_DAILY_QUANTITIES = [
    qty for qty in VARS_CONFIG
    if VARS_CONFIG[qty]["type"] == "daily"]
HIGHCHARTS_SERIES_VARS = (
        CUM_QUANTITIES + NON_CUM_QUANTITIES + NON_CUM_DAILY_QUANTITIES)
HIGHCHARTS_PROV_SERIES_VARS = [
    'totale_casi', 'nuovi_positivi', 'nuovi_positivi_g',
    'nuovi_positivi_perc', 'nuovi_positivi_g_perc', 'totale_casi_perc']
TREND_CARDS = CUM_QUANTITIES + NON_CUM_QUANTITIES + NON_CUM_DAILY_QUANTITIES
TREND_PROV_CARDS = ['totale_casi', 'nuovi_positivi', 'nuovi_positivi_g']


def preprocess_df(df):
    """
    Return df without the column 'stato' and with 'data' datetime-string parsed
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    df.drop(columns=['stato'], inplace=True)
    df['data'] = pd.to_datetime(df['data'], format=CP_DATE_FMT)
    return df


def augment_df(df):
    """
    Augment PC DataFrame adding the daily '_g' columns and
    percentage '_perc' columns
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    df_augmented = df.copy()
    for col in CUM_QUANTITIES + NON_CUM_QUANTITIES:
        df_augmented[col + "_g"] = df_augmented[col].diff()
    for col in CUM_QUANTITIES:
        df_augmented[col + "_perc"] = df_augmented[col + "_g"].div(
            df_augmented[col + "_g"].shift(1)) * 100
    for col in NON_CUM_QUANTITIES:
        df_augmented[col + "_perc"] = df_augmented[col + "_g"].div(
            df_augmented[col].shift(1)) * 100
    for col in NON_CUM_DAILY_QUANTITIES:
        df_augmented[col + "_perc"] = df_augmented[col].div(
            df_augmented[col].shift(1)) * 100
    df_augmented["tamponi_perc"] = df_augmented["tamponi_g"].div(
        df_augmented["tamponi"].shift(7)) * 100
    df_augmented["tamponi_g_perc"] = df_augmented["tamponi_g"].div(
        df_augmented["tamponi_g"].shift(7)) * 100
    df_augmented = df_augmented.where(pd.notnull(df_augmented), None)
    df_augmented = df_augmented.fillna(value=0)
    return df_augmented


def augment_regional_df(df):
    dfs = []
    for cr in set(df[REGION_CODE]):
        df_region = df[df[REGION_CODE] == cr].copy()
        for col in CUM_QUANTITIES + NON_CUM_QUANTITIES:
            df_region[col + "_g"] = df_region[col].diff()
        for col in CUM_QUANTITIES:
            df_region[col + "_perc"] = df_region[col + "_g"].div(
                df_region[col + "_g"].shift(1)) * 100
        for col in NON_CUM_QUANTITIES:
            df_region[col + "_perc"] = df_region[col + "_g"].div(
                df_region[col].shift(1)) * 100
        df_region["tamponi_perc"] = df_region["tamponi_g"].div(
            df_region["tamponi"].shift(7)) * 100
        df_region["tamponi_g_perc"] = df_region["tamponi_g"].div(
            df_region["tamponi_g"].shift(7)) * 100
        for col in NON_CUM_DAILY_QUANTITIES:
            df_region[col + "_perc"] = df_region[col].div(
                df_region[col].shift(1)) * 100
        dfs.append(df_region)
    df_augmented = pd.concat(dfs)
    df_augmented = df_augmented.where(pd.notnull(df_augmented), None)
    df_augmented = df_augmented.fillna(value=0)
    return df_augmented


def augment_provincial_df(df):
    dfs = []
    for cp in set(df[PROVINCE_CODE]):
        dfp = df[df[PROVINCE_CODE] == cp].copy()
        dfp["nuovi_positivi"] = dfp["totale_casi"].diff()
        dfp["nuovi_positivi_g"] = dfp["nuovi_positivi"].diff()
        dfp["nuovi_positivi_perc"] = dfp["nuovi_positivi"].diff().div(
            dfp["nuovi_positivi"].shift(1)) * 100
        dfp["nuovi_positivi_g_perc"] = dfp["nuovi_positivi_g"].diff().div(
            dfp["nuovi_positivi_g"].shift(1)) * 100
        dfp["totale_casi_perc"] = dfp["nuovi_positivi"].div(
            dfp["nuovi_positivi"].shift(1)) * 100
        dfs.append(dfp)
    df_augmented = pd.concat(dfs)
    df_augmented = df_augmented.where(pd.notnull(df_augmented), None)
    df_augmented = df_augmented.fillna(value=0)
    return df_augmented


def build_trends(df):
    trends = []
    for col in TREND_CARDS:
        try:
            status = "stable"
            percentage_col = col + "_perc"
            diff = "{0:+}".format(
                round(df[col].values[-1] - df[col].values[-2]))
            try:
                percentage = "{0:+}%".format(
                    round(df[percentage_col].values[-1]))
            except (OverflowError, TypeError):
                percentage = "n/a"
            if df[col].values[-1] < df[col].values[-2]:
                status = "decrease"
            if df[col].values[-1] > df[col].values[-2]:
                status = "increase"
            if df[col].values[-1] == df[col].values[-2]:
                status = "stable"
            t = {
                "id": col,
                "type": VARS_CONFIG[col]["type"],
                "title": VARS_CONFIG[col]["title"],
                "desc": VARS_CONFIG[col]["desc"],
                "longdesc": VARS_CONFIG[col]["longdesc"],
                "count": round(df[col].values[-1]),
                "colour": VARS_CONFIG[col][status]["colour"],
                "icon": VARS_CONFIG[col]["icon"],
                "status_icon": VARS_CONFIG[col][status]["icon"],
                "tooltip": VARS_CONFIG[col][status]["tooltip"],
                "percentage_difference": percentage,
                "today_yesterday_diff": diff
            }
            trends.append(t)
        except KeyError as e:
            print(e)
            continue
    return trends


def build_regional_trends(df):
    trends = []
    for cr in set(df[REGION_CODE]):
        df_r = df[df[REGION_CODE] == cr].copy()
        trend = {
            REGION_KEY: df_r[REGION_KEY].values[-1],
            "trends": build_trends(df_r)
        }
        trends.append(trend)
    return trends


def build_provincial_trends(df):
    trends = []
    for cp in set(df[PROVINCE_CODE]):
        province_trends = []
        dfp = df[df[PROVINCE_CODE] == cp].copy()
        for col in TREND_PROV_CARDS:
            try:
                status = "stable"
                percentage_col = col + "_perc"
                diff = "{0:+}".format(
                    round(dfp[col].values[-1] - dfp[col].values[-2]))
                try:
                    percentage = "{0:+}%".format(
                        round(dfp[percentage_col].values[-1]))
                except (OverflowError, TypeError):
                    percentage = "n/a"
                if dfp[col].values[-1] < dfp[col].values[-2]:
                    status = "decrease"
                if dfp[col].values[-1] > dfp[col].values[-2]:
                    status = "increase"
                if dfp[col].values[-1] == dfp[col].values[-2]:
                    status = "stable"
                t = {
                    "id": col,
                    "type": VARS_CONFIG[col]["type"],
                    "title": VARS_CONFIG[col]["title"],
                    "desc": VARS_CONFIG[col]["desc"],
                    "longdesc": VARS_CONFIG[col]["longdesc"],
                    "count": round(dfp[col].values[-1]),
                    "colour": VARS_CONFIG[col][status]["colour"],
                    "icon": VARS_CONFIG[col]["icon"],
                    "status_icon": VARS_CONFIG[col][status]["icon"],
                    "tooltip": VARS_CONFIG[col][status]["tooltip"],
                    "percentage_difference": percentage,
                    "today_yesterday_diff": diff
                }
                province_trends.append(t)
            except KeyError as e:
                print(e)
                continue
        trends.append({
            PROVINCE_KEY: dfp[PROVINCE_KEY].values[-1],
            "trends": province_trends
        })
    return trends


def build_breakdown(df):
    breakdown = {}
    sub_url = 'regions'
    for col in TREND_CARDS:
        breakdown[col] = []
        for code in set(df[REGION_CODE]):
            df_area = df[df[REGION_CODE] == code].copy()
            area = df_area[REGION_KEY].values[-1]
            if area not in REGIONS:
                continue
            count = int(df_area[col].values[-1])
            url = "/{}/{}".format(sub_url, df_area[REGION_KEY].values[-1])
            b = {
                "area": area,
                "count": count,
                "url": url
            }
            breakdown[col].append(b)
    return breakdown


def build_provincial_breakdown(df):
    breakdowns = []
    for cr in set(df[REGION_CODE]):
        df_region = df[df[REGION_CODE] == cr].copy()
        region = df_region[REGION_KEY].values[-1]
        if region not in REGIONS:
            continue
        breakdown = {
            REGION_KEY: region,
            "breakdowns": {}
        }
        for col in TREND_PROV_CARDS:
            breakdown["breakdowns"][col] = []
            for cp in set(df_region[PROVINCE_CODE]):
                df_province = df_region[df_region[PROVINCE_CODE] == cp].copy()
                province = df_province[PROVINCE_KEY].values[-1]
                if province not in PROVINCES:
                    continue
                count = int(df_province[col].values[-1])
                url = f"/provinces/{province}"
                prov_col_dict = {
                    "area": province,
                    "count": count,
                    "url": url
                }
                breakdown["breakdowns"][col].append(prov_col_dict)
        breakdowns.append(breakdown)
    return breakdowns


def build_national_highcarts(df):
    dates = df[DATE_KEY].apply(lambda x: x.strftime(CHART_DATE_FMT)).tolist()
    series_daily = [
        {
            "name": VARS_CONFIG[col]["title"],
            "data": df[col].values.tolist()
        }
        for col in NON_CUM_DAILY_QUANTITIES
    ]
    series_current = [
        {
            "name": VARS_CONFIG[col]["title"],
            "data": df[col].values.tolist()
        }
        for col in NON_CUM_QUANTITIES
    ]
    series_cum = [
        {
            "name": VARS_CONFIG[col]["title"],
            "data": df[col].values.tolist()
        }
        for col in CUM_QUANTITIES
    ]
    series = {
        "dates": dates,
        "daily": series_daily,
        "current": series_current,
        "cum": series_cum
    }
    return series


def build_regional_highcarts(df):
    series = []
    for cr in set(df[REGION_CODE]):
        df_area = df[df[REGION_CODE] == cr].copy()
        dates = df_area[DATE_KEY].apply(
            lambda x: x.strftime(CHART_DATE_FMT)).tolist()
        series_daily = [
            {
                "name": VARS_CONFIG[col]["title"],
                "data": df_area[col].values.tolist()
            }
            for col in NON_CUM_DAILY_QUANTITIES
        ]
        series_current = [
            {
                "name": VARS_CONFIG[col]["title"],
                "data": df_area[col].values.tolist()
            }
            for col in NON_CUM_QUANTITIES
        ]
        series_cum = [
            {
                "name": VARS_CONFIG[col]["title"],
                "data": df_area[col].values.tolist()
            }
            for col in CUM_QUANTITIES
        ]
        s = {
            REGION_KEY: df_area[REGION_KEY].values[-1],
            "dates": dates,
            "daily": series_daily,
            "current": series_current,
            "cum": series_cum
        }
        series.append(s)
    return series


def build_provincial_highcharts(df):
    series = []
    for cp in set(df[PROVINCE_CODE]):
        df_area = df[df[PROVINCE_CODE] == cp].copy()
        dates = df_area[DATE_KEY].apply(
            lambda x: x.strftime(CHART_DATE_FMT)).tolist()
        series_daily = [
            {
                "name": VARS_CONFIG[col]["title"],
                "data": df_area[col].values.tolist()
            }
            for col in ['nuovi_positivi_g']
        ]
        series_current = [
            {
                "name": VARS_CONFIG[col]["title"],
                "data": df_area[col].values.tolist()
            }
            for col in ['nuovi_positivi']
        ]
        series_cum = [
            {
                "name": VARS_CONFIG[col]["title"],
                "data": df_area[col].values.tolist()
            }
            for col in ['totale_casi']
        ]
        series.append({
            PROVINCE_KEY: df_area[PROVINCE_KEY].values[-1],
            "dates": dates,
            "daily": series_daily,
            "current": series_current,
            "cum": series_cum
        })
    return series
