import pandas as pd
from flask import jsonify, current_app as app

from app.api import api
from app.db.collections import (
    NATIONAL_DATA, NATIONAL_TRENDS, NATIONAL_SERIES,
    REGIONAL_DATA, REGIONAL_TRENDS, REGIONAL_SERIES, REGIONAL_BREAKDOWN,
    PROVINCIAL_DATA, PROVINCIAL_TRENDS, PROVINCIAL_SERIES,
    PROVINCIAL_BREAKDOWN, BARCHART_COLLECTION
)
from app.db.update import (
    augment_df, preprocess_df, augment_regional_df, augment_provincial_df,
    build_trends, build_regional_trends, build_provincial_trends,
    build_breakdown, build_provincial_breakdown, build_national_highcarts,
    build_regional_highcarts, build_provincial_highcharts
)
from config import (
    BARCHART_DB_KEY, UPDATE_FMT,
    URL_NATIONAL_DATA, URL_REGIONAL_DATA, URL_PROVINCIAL_DATA
)


@api.route("/bcr/<string:var_name>")
def get_bcr(var_name):
    """
    Bar-chart race API. Return a JSON with fields "html" and "ts".
    The former contains the HTML code of the bar-chart race video,
    the latter the timestamp at which the bar-chart race was created on the DB
    :param: var_name: str
    :return: flask.jsonify()
    """
    data = {}
    try:
        app.logger.info("Getting {} bcr from mongo".format(var_name))
        data = next(BARCHART_COLLECTION.find({BARCHART_DB_KEY: var_name}))
        data["ts"] = data["ts"].strftime(UPDATE_FMT)
        data["status"] = "ok"
    except StopIteration:
        err_msg = "No {} bcr data in mongo".format(var_name)
        app.logger.error(err_msg)
        data["status"] = "ko"
        data["error"] = err_msg
    return jsonify(**data)


def update_national_collections(response):
    """
    Update national collections
    :param response: dict
    :return: dict
    """
    df = pd.read_csv(URL_NATIONAL_DATA)
    df = preprocess_df(df)
    df_national_augmented = augment_df(df)

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


@api.route("/update/<coll>", methods=["POST"])
def update_db(coll):
    """
    Trigger db-collection updates
    :param coll: str
    :return: json str
    """
    response = {"status": "ok", "collections_updated": [], "errors": []}
    if coll == "national":
        response = update_national_collections(response)
    if coll == "regional":
        response = update_regional_collections(response)
    if coll == "provincial":
        response = update_provincial_collections(response)
    return jsonify(**response)
