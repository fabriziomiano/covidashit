"""
DB Recovery
"""
import pandas as pd
from flask import current_app as app

from app.data.etl import (
    augment_national_df, augment_regional_df, augment_provincial_df,
    build_national_trends, build_regional_trends, build_provincial_trends,
    build_regional_breakdown, build_provincial_breakdowns,
    build_national_series, build_regional_series, build_provincial_series,
    COLUMNS_TO_DROP
)
from app.db import (
    NAT_DATA_COLL, NAT_TRENDS_COLL, NAT_SERIES_COLL, REG_DATA_COLL,
    REG_TRENDS_COLL, REG_SERIES_COLL, REG_BREAKDOWN_COLL, PROV_DATA_COLL,
    PROV_TRENDS_COLL, PROV_SERIES_COLL, PROV_BREAKDOWN_COLL
)
from config import (
    URL_NATIONAL, URL_REGIONAL, URL_PROVINCIAL, DATE_KEY
)


def create_national_collection():
    """Drop and recreate national data collection"""
    response = {"status": "ko", "collections_created": [], "errors": []}
    df = pd.read_csv(URL_NATIONAL, parse_dates=[DATE_KEY])
    df.drop(columns=COLUMNS_TO_DROP, inplace=True)
    df_national_augmented = augment_national_df(df)
    national_records = df_national_augmented.to_dict(orient='records')
    try:
        app.logger.warning("Doing national")
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
        app.logger.warning("Doing national_trends")
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
        app.logger.warning("Doing national_series")
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
        app.logger.warning("Doing regional")
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
        app.logger.warning("Doing regional_breakdown")
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
        app.logger.warning("Doing regional_series")
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
        app.logger.warning("Doing regional_trends")
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
        app.logger.warning("Doing provincial")
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
        app.logger.warning("Doing provincial_breakdowns")
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
        app.logger.warning("Doing provincial_series")
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
        app.logger.warning("Doing provincial_trends")
        PROV_TRENDS_COLL.drop()
        PROV_TRENDS_COLL.insert_many(provincial_trends)
        response["collections_created"].append("provincial_trends")
        response["status"] = "ok"
        status = 200
    except Exception as e:
        app.logger.error(e)
        response["errors"].append("{}".format(e))
    return response, status
