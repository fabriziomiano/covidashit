"""
DB Recovery
"""
import pandas as pd
from flask import current_app as app

from app.db.etl import (
    augment_national_df, augment_regional_df, augment_provincial_df,
    build_national_trends, build_regional_trends, build_provincial_trends,
    build_regional_breakdown, build_provincial_breakdowns,
    build_national_series, build_regional_series, build_provincial_series,
    COLUMNS_TO_DROP, augment_vax_df, augment_summary_vax_df
)
from app.db import (
    NAT_DATA_COLL, NAT_TRENDS_COLL, NAT_SERIES_COLL, REG_DATA_COLL,
    REG_TRENDS_COLL, REG_SERIES_COLL, REG_BREAKDOWN_COLL, PROV_DATA_COLL,
    PROV_TRENDS_COLL, PROV_SERIES_COLL, PROV_BREAKDOWN_COLL, VAX_COLL,
    VAX_SUMMARY_COLL
)
from constants import (
    URL_NATIONAL, URL_REGIONAL, URL_PROVINCIAL, DATE_KEY, URL_VAX_DATA,
    URL_VAX_ADMINS_SUMMARY_DATA, VAX_DATE_KEY
)


def create_national_collection():
    """Drop and recreate national data collection"""
    response = {"status": "ko", "collections_created": [], "errors": []}
    df = pd.read_csv(URL_NATIONAL, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
    df_national_augmented = augment_national_df(df)
    national_records = df_national_augmented.to_dict(orient='records')
    try:
        app.logger.info("Doing national collection")
        NAT_DATA_COLL.drop()
        NAT_DATA_COLL.insert_many(national_records, ordered=True)
        response["collections_created"].append("national")
        response["status"] = "ok"
        status = 200
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        status = 500
    return response, status


def create_national_trends_collection():
    """Drop and recreate national trends data collection"""
    response = {"status": "ko", "collections_created": [], "errors": []}
    df = pd.read_csv(URL_NATIONAL, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
    df_national_augmented = augment_national_df(df)
    national_trends = build_national_trends(df_national_augmented)
    try:
        app.logger.info("Doing national trends collection")
        NAT_TRENDS_COLL.drop()
        NAT_TRENDS_COLL.insert_many(national_trends)
        response["collections_created"].append("national_trends")
        response["status"] = "ok"
        status = 200
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        status = 500
    return response, status


def create_national_series_collection():
    """Drop and recreate national series data collection"""
    response = {"status": "ko", "collections_created": [], "errors": []}
    df = pd.read_csv(URL_NATIONAL, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
    df_national_augmented = augment_national_df(df)
    national_series = build_national_series(df_national_augmented)
    try:
        app.logger.info("Doing national series collection")
        NAT_SERIES_COLL.drop()
        NAT_SERIES_COLL.insert_one(national_series)
        response["collections_created"].append("national_series")
        response["status"] = "ok"
        status = 200
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
        status = 500
    return response, status


def create_regional_collection():
    """Drop and recreate regional data collection"""
    status = 500
    response = {"status": "ko", "collections_created": [], "errors": []}
    df = pd.read_csv(URL_REGIONAL, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
    df_regional_augmented = augment_regional_df(df)
    regional_records = df_regional_augmented.to_dict(orient='records')
    try:
        app.logger.info("Doing regional collection")
        REG_DATA_COLL.drop()
        REG_DATA_COLL.insert_many(regional_records, ordered=True)
        response["collections_created"].append("regional")
        response["status"] = "ok"
        status = 200
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
    return response, status


def create_regional_breakdown_collection():
    """Drop and recreate regional breakdown data collection"""
    status = 500
    response = {"status": "ko", "collections_created": [], "errors": []}
    df = pd.read_csv(URL_REGIONAL, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
    df_regional_augmented = augment_regional_df(df)
    regional_breakdown = build_regional_breakdown(df_regional_augmented)
    try:
        app.logger.info("Doing regional breakdown collection")
        REG_BREAKDOWN_COLL.drop()
        REG_BREAKDOWN_COLL.insert_one(regional_breakdown)
        response["collections_created"].append("regional_breakdown")
        response["status"] = "ok"
        status = 200
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
    return response, status


def create_regional_series_collection():
    """Drop and recreate regional series data collection"""
    status = 500
    response = {"status": "ko", "collections_created": [], "errors": []}
    df = pd.read_csv(URL_REGIONAL, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
    df_regional_augmented = augment_regional_df(df)
    regional_series = build_regional_series(df_regional_augmented)
    try:
        app.logger.info("Doing regional series collection")
        REG_SERIES_COLL.drop()
        REG_SERIES_COLL.insert_many(regional_series)
        response["collections_created"].append("regional_series")
        response["status"] = "ok"
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
    return response, status


def create_regional_trends_collection():
    """Drop and recreate regional trends data collection"""
    status = 500
    response = {"status": "ko", "collections_created": [], "errors": []}
    df = pd.read_csv(URL_REGIONAL, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
    df_regional_augmented = augment_regional_df(df)
    regional_trends = build_regional_trends(df_regional_augmented)
    try:
        app.logger.info("Doing regional trends collection")
        REG_TRENDS_COLL.drop()
        REG_TRENDS_COLL.insert_many(regional_trends)
        response["collections_created"].append("regional_trends")
        response["status"] = "ok"
        status = 200
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
    return response, status


def create_provincial_collections():
    """Drop and recreate provincial collection"""
    status = 500
    response = {"status": "ko", "collections_created": [], "errors": []}
    df = pd.read_csv(URL_PROVINCIAL, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
    df_provincial_augmented = augment_provincial_df(df)
    provincial_records = df_provincial_augmented.to_dict(orient='records')
    try:
        app.logger.info("Doing provincial")
        PROV_DATA_COLL.drop()
        PROV_DATA_COLL.insert_many(provincial_records, ordered=True)
        response["collections_created"].append("provincial")
        response["status"] = "ok"
        status = 200
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
    return response, status


def create_provincial_breakdown_collection():
    """Drop and create provincial breakdown collection"""
    status = 500
    response = {"status": "ko", "collections_created": [], "errors": []}
    df = pd.read_csv(URL_PROVINCIAL, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
    df_provincial_augmented = augment_provincial_df(df)
    provincial_breakdowns = build_provincial_breakdowns(
        df_provincial_augmented)
    try:
        app.logger.info("Doing provincial breakdowns collection")
        PROV_BREAKDOWN_COLL.drop()
        PROV_BREAKDOWN_COLL.insert_many(provincial_breakdowns)
        response["collections_created"].append("provincial_breakdowns")
        response["status"] = "ok"
        status = 200
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
    return response, status


def create_provincial_series_collection():
    """Drop and recreate provincial series data collection"""
    status = 500
    response = {"status": "ko", "collections_created": [], "errors": []}
    df = pd.read_csv(URL_PROVINCIAL, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
    df_provincial_augmented = augment_provincial_df(df)
    provincial_series = build_provincial_series(
        df_provincial_augmented)
    try:
        app.logger.info("Doing provincial series collection")
        PROV_SERIES_COLL.drop()
        PROV_SERIES_COLL.insert_many(provincial_series)
        response["collections_created"].append("provincial_series")
        response["status"] = "ok"
        status = 200
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
    return response, status


def create_provincial_trends_collection():
    """Create provincial trends data collection"""
    status = 500
    response = {"status": "ko", "collections_created": [], "errors": []}
    df = pd.read_csv(URL_PROVINCIAL, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
    df_provincial_augmented = augment_provincial_df(df)
    provincial_trends = build_provincial_trends(df_provincial_augmented)
    try:
        app.logger.info("Doing provincial trends collection")
        PROV_TRENDS_COLL.drop()
        PROV_TRENDS_COLL.insert_many(provincial_trends)
        response["collections_created"].append("provincial_trends")
        response["status"] = "ok"
        status = 200
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
    return response, status


def create_vax_collection(summary=False):
    """Create vaccine-data colleciton"""
    url = URL_VAX_DATA if not summary else URL_VAX_ADMINS_SUMMARY_DATA
    coll = VAX_COLL if not summary else VAX_SUMMARY_COLL
    df = pd.read_csv(url, parse_dates=[VAX_DATE_KEY])
    df = augment_vax_df(df) if not summary else augment_summary_vax_df(df)
    if summary:
        info_msg = "Doing vax summary collection"
    else:
        info_msg = "Doing vax collection"
    status = 500
    response = {"status": "ko", "collections_created": [], "errors": []}
    records = df.to_dict(orient='records')
    try:
        app.logger.info(info_msg)
        coll.drop()
        coll.insert_many(records, ordered=True)
        response["collections_created"].append(coll.name)
        response["status"] = "ok"
        status = 200
    except Exception as e:
        app.logger.error(f"While creating vax collection: {e}")
        response["errors"].append(f"{e}")
    return response, status
