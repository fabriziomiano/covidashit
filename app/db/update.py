import pandas as pd
from flask import current_app as app

from app.db.collections import (
    NATIONAL_DATA, NATIONAL_TRENDS, NATIONAL_SERIES, REGIONAL_DATA,
    REGIONAL_TRENDS, REGIONAL_BREAKDOWN, REGIONAL_SERIES, PROVINCIAL_DATA,
    PROVINCIAL_TRENDS, PROVINCIAL_BREAKDOWN, PROVINCIAL_SERIES
)
from config import (
    CP_DATE_FMT, VARS, REGION_KEY, PROVINCE_KEY, PROVINCE_CODE,
    REGION_CODE, PROVINCES, REGIONS, DATE_KEY, CHART_DATE_FMT, URL_NATIONAL_DATA,
    URL_REGIONAL_DATA, URL_PROVINCIAL_DATA, DAILY_POSITIVITY_INDEX,
    DAILY_SWABS_KEY, NEW_POSITIVE_KEY, TOTAL_CASES_KEY
)

CUM_QUANTITIES = [
    qty for qty in VARS
    if VARS[qty]["type"] == "cum"]
NON_CUM_QUANTITIES = [
    qty for qty in VARS
    if VARS[qty]["type"] == "current"]
NON_CUM_DAILY_QUANTITIES = [
    qty for qty in VARS
    if VARS[qty]["type"] == "daily"]
HIGHCHARTS_SERIES_VARS = (
        CUM_QUANTITIES + NON_CUM_QUANTITIES + NON_CUM_DAILY_QUANTITIES)
HIGHCHARTS_PROV_SERIES_VARS = [
    TOTAL_CASES_KEY, NEW_POSITIVE_KEY, 'nuovi_positivi_perc', 'totale_casi_perc']
TREND_CARDS = CUM_QUANTITIES + NON_CUM_QUANTITIES + NON_CUM_DAILY_QUANTITIES
PROV_TREND_CARDS = [TOTAL_CASES_KEY, NEW_POSITIVE_KEY]


def preprocess_df(df):
    """
    Return df without the column 'stato' and with 'data' datetime-string parsed
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    df.drop(columns=['stato'], inplace=True)
    df['data'] = pd.to_datetime(df['data'], format=CP_DATE_FMT)
    return df


def add_delta(df):
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
    for col in VARS:
        try:
            diff_df = df[col].diff()
            df[col + "_perc"] = diff_df.div(df[col].shift(1)) * 100
        except KeyError:
            continue
    return df


def add_positivity_idx(df):
    df[DAILY_POSITIVITY_INDEX] = (
            df[NEW_POSITIVE_KEY].div(df[DAILY_SWABS_KEY]) * 100)
    return df


def clean_df(df):
    df = df.where(pd.notnull(df), None)
    df = df.fillna(value=0)
    return df


def augment_national_df(df):
    """
    Augment PC DataFrame adding the daily '_g' and percentage '_perc' columns
    :param df: pd.DataFrame
    :return: pd.DataFrame
    """
    df_augmented = df.copy()
    df_augmented = add_delta(df_augmented)
    df_augmented = add_percentages(df_augmented)
    df_augmented = add_positivity_idx(df_augmented)
    df_augmented = clean_df(df_augmented)
    return df_augmented


def augment_regional_df(df):
    dfs = []
    for cr in set(df[REGION_CODE]):
        df_region = df[df[REGION_CODE] == cr].copy()
        df_region = add_delta(df_region)
        df_region = add_percentages(df_region)
        df_region = add_positivity_idx(df_region)
        dfs.append(df_region)
    df_augmented = pd.concat(dfs)
    df_augmented = clean_df(df_augmented)
    return df_augmented


def augment_provincial_df(df):
    dfs = []
    for cp in set(df[PROVINCE_CODE]):
        dfp = df[df[PROVINCE_CODE] == cp].copy()
        dfp[NEW_POSITIVE_KEY] = dfp[TOTAL_CASES_KEY].diff()
        df_new_pos_diff = dfp[NEW_POSITIVE_KEY].diff()
        dfp["nuovi_positivi_perc"] = df_new_pos_diff.div(
            dfp[NEW_POSITIVE_KEY].shift(1)) * 100
        dfp["totale_casi_perc"] = (
                dfp[NEW_POSITIVE_KEY].div(dfp[TOTAL_CASES_KEY].shift(1)) * 100)
        dfs.append(dfp)
    df_augmented = pd.concat(dfs)
    df_augmented = clean_df(df_augmented)
    return df_augmented


def build_trends(df):
    trends = []
    for col in VARS:
        try:
            status = "stable"
            percentage_col = col + "_perc"
            count = int(df[col].values[-1])
            yesterday_count = int(df[col].values[-2])
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
                "type": VARS[col]["type"],
                "title": VARS[col]["title"],
                "desc": VARS[col]["desc"],
                "longdesc": VARS[col]["longdesc"],
                "count": round(count),
                "colour": VARS[col][status]["colour"],
                "icon": VARS[col]["icon"],
                "status_icon": VARS[col][status]["icon"],
                "tooltip": VARS[col][status]["tooltip"],
                "percentage_difference": percentage,
                "yesterday_count": yesterday_count
            }
            trends.append(t)
        except Exception as e:
            app.logger.error(f"{e}")
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
        for col in PROV_TREND_CARDS:
            try:
                status = "stable"
                percentage_col = col + "_perc"
                count = int(dfp[col].values[-1])
                yesterday_count = int(dfp[col].values[-2])
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
                    "type": VARS[col]["type"],
                    "title": VARS[col]["title"],
                    "desc": VARS[col]["desc"],
                    "longdesc": VARS[col]["longdesc"],
                    "count": round(count),
                    "colour": VARS[col][status]["colour"],
                    "icon": VARS[col]["icon"],
                    "status_icon": VARS[col][status]["icon"],
                    "tooltip": VARS[col][status]["tooltip"],
                    "percentage_difference": percentage,
                    "yesterday_count": yesterday_count
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
        for col in PROV_TREND_CARDS:
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
            "name": VARS[col]["title"],
            "data": df[col].values.tolist()
        }
        for col in NON_CUM_DAILY_QUANTITIES
    ]
    series_current = [
        {
            "name": VARS[col]["title"],
            "data": df[col].values.tolist()
        }
        for col in NON_CUM_QUANTITIES
    ]
    series_cum = [
        {
            "name": VARS[col]["title"],
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
                "name": VARS[col]["title"],
                "data": df_area[col].values.tolist()
            }
            for col in NON_CUM_DAILY_QUANTITIES
        ]
        series_current = [
            {
                "name": VARS[col]["title"],
                "data": df_area[col].values.tolist()
            }
            for col in NON_CUM_QUANTITIES
        ]
        series_cum = [
            {
                "name": VARS[col]["title"],
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
                "name": VARS["nuovi_positivi"]["title"],
                "data": df_area["nuovi_positivi"].values.tolist()
            }
        ]
        series_cum = [
            {
                "name": VARS["totale_casi"]["title"],
                "data": df_area["totale_casi"].values.tolist()
            }
        ]
        series.append({
            PROVINCE_KEY: df_area[PROVINCE_KEY].values[-1],
            "dates": dates,
            "daily": series_daily,
            "cum": series_cum
        })
    return series


def update_national_collections(response):
    """
    Update national collections
    :param response: dict
    :return: dict
    """
    df = pd.read_csv(URL_NATIONAL_DATA)
    df = preprocess_df(df)
    df_national_augmented = augment_national_df(df)

    national_records = df_national_augmented.to_dict(orient='records')
    try:
        app.logger.warning("Updating collection: national")
        NATIONAL_DATA.drop()
        NATIONAL_DATA.insert_many(national_records, ordered=True)
        response["collections_updated"].append("national")
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        response["status"] = "ok"

    national_trends = build_trends(df_national_augmented)
    try:
        app.logger.warning("Updating collection: national_trends")
        NATIONAL_TRENDS.drop()
        NATIONAL_TRENDS.insert_many(national_trends)
        response["collections_updated"].append("national_trends")
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        response["status"] = "ok"

    national_series = build_national_highcarts(df_national_augmented)
    try:
        app.logger.warning("Updating collection: national_series")
        NATIONAL_SERIES.drop()
        NATIONAL_SERIES.insert_one(national_series)
        response["collections_updated"].append("national_series")
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        response["status"] = "ok"
    return response


def update_regional_collections(response):
    """
    Update regional collections
    :param response: dict
    :return: dict
    """
    df = pd.read_csv(URL_REGIONAL_DATA)
    df = preprocess_df(df)
    df_regional_augmented = augment_regional_df(df)

    regional_records = df_regional_augmented.to_dict(orient='records')
    try:
        app.logger.warning("Updating collection: regional")
        REGIONAL_DATA.drop()
        REGIONAL_DATA.insert_many(regional_records, ordered=True)
        response["collections_updated"].append("regional")
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        response["status"] = "ok"

    regional_trends = build_regional_trends(df_regional_augmented)
    try:
        app.logger.warning("Updating collection: regional_trends")
        REGIONAL_TRENDS.drop()
        REGIONAL_TRENDS.insert_many(regional_trends)
        response["collections_updated"].append("regional_trends")
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        response["status"] = "ok"

    regional_breakdown = build_breakdown(df_regional_augmented)
    try:
        app.logger.warning("Updating collection: regional_breakdown")
        REGIONAL_BREAKDOWN.drop()
        REGIONAL_BREAKDOWN.insert_one(regional_breakdown)
        response["collections_updated"].append("regional_breakdown")
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        response["status"] = "ok"

    regional_series = build_regional_highcarts(df_regional_augmented)
    try:
        app.logger.warning("Updating collection: regional_series")
        REGIONAL_SERIES.drop()
        REGIONAL_SERIES.insert_many(regional_series)
        response["collections_updated"].append("regional_series")
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        response["status"] = "ok"
    return response


def update_provincial_collections(response):
    """
    Update provincial collections
    :param response: dict
    :return: dict
    """
    df = pd.read_csv(URL_PROVINCIAL_DATA)
    df = preprocess_df(df)
    df_provincial_augmented = augment_provincial_df(df)

    provincial_records = df_provincial_augmented.to_dict(orient='records')
    try:
        app.logger.warning("Updating collection: provincial")
        PROVINCIAL_DATA.drop()
        PROVINCIAL_DATA.insert_many(provincial_records, ordered=True)
        response["collections_updated"].append("provincial")
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        response["status"] = "ok"

    provincial_trends = build_provincial_trends(df_provincial_augmented)
    try:
        app.logger.warning("Updating collection: provincial_trends")
        PROVINCIAL_TRENDS.drop()
        PROVINCIAL_TRENDS.insert_many(provincial_trends)
        response["collections_updated"].append("provincial_trends")
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        response["status"] = "ok"

    provincial_breakdowns = build_provincial_breakdown(
        df_provincial_augmented)
    try:
        app.logger.warning("Updating collection: provincial_breakdowns")
        PROVINCIAL_BREAKDOWN.drop()
        PROVINCIAL_BREAKDOWN.insert_many(provincial_breakdowns)
        response["collections_updated"].append("provincial_breakdowns")
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        response["status"] = "ok"

    provincial_series = build_provincial_highcharts(
        df_provincial_augmented)
    try:
        app.logger.warning("Updating collection: provincial_series")
        PROVINCIAL_SERIES.drop()
        PROVINCIAL_SERIES.insert_many(provincial_series)
        response["collections_updated"].append("provincial_series")
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        response["status"] = "ok"
    return response
