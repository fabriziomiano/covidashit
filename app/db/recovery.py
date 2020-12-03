import pandas as pd
from flask import current_app as app

from app.data.etl import (
    augment_national_df, augment_regional_df, augment_provincial_df,
    build_national_trends, build_regional_trends, build_provincial_trends,
    build_regional_breakdown, build_provincial_breakdowns,
    build_national_series, build_regional_series, build_provincial_series,
    COLUMNS_TO_DROP
)
from app.db.collections import (
    NATIONAL_DATA, NATIONAL_TRENDS, NATIONAL_SERIES, REGIONAL_DATA,
    REGIONAL_TRENDS, REGIONAL_BREAKDOWN, REGIONAL_SERIES, PROVINCIAL_DATA,
    PROVINCIAL_TRENDS, PROVINCIAL_BREAKDOWN, PROVINCIAL_SERIES
)
from config import (
    URL_NATIONAL_DATA, URL_REGIONAL_DATA, URL_PROVINCIAL_DATA, DATE_KEY
)


def create_national_collections(response):
    """
    Update national collections
    :param response: dict
    :return: dict
    """
    df = pd.read_csv(URL_NATIONAL_DATA, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
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

    national_trends = build_national_trends(df_national_augmented)
    try:
        app.logger.warning("Updating collection: national_trends")
        NATIONAL_TRENDS.drop()
        NATIONAL_TRENDS.insert_many(national_trends)
        response["collections_updated"].append("national_trends")
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        response["status"] = "ok"

    national_series = build_national_series(df_national_augmented)
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


def create_regional_collections(response):
    """
    Update regional collections
    :param response: dict
    :return: dict
    """
    df = pd.read_csv(URL_REGIONAL_DATA, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
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

    regional_breakdown = build_regional_breakdown(df_regional_augmented)
    try:
        app.logger.warning("Updating collection: regional_breakdown")
        REGIONAL_BREAKDOWN.drop()
        REGIONAL_BREAKDOWN.insert_one(regional_breakdown)
        response["collections_updated"].append("regional_breakdown")
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        response["status"] = "ok"

    regional_series = build_regional_series(df_regional_augmented)
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


def create_provincial_collections(response):
    """
    Update provincial collections
    :param response: dict
    :return: dict
    """
    df = pd.read_csv(URL_PROVINCIAL_DATA, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
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

    provincial_breakdowns = build_provincial_breakdowns(
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

    provincial_series = build_provincial_series(
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
