import datetime as dt
import json
import re

import requests
from flask import current_app as app
from flask_babel import gettext

from app import mongo
from config import (
    CUSTOM_CARDS, CARD_MAP, CARD_TYPES, VARS_CONFIG, PROVINCES,
    PROVINCE_KEY, REGIONS, REGION_KEY, CP_DATE_FMT, CHART_DATE_FMT,
    CP_DATE_KEY, UPDATE_FMT, DASHBOARD_DATA, TOTAL_CASES_KEY,
    NEW_POSITIVE_KEY, CUMULATIVE_DATA_TYPES, RUBBISH_NOTE_REGEX, NOTE_KEY,
    NATIONAL_DATA_COLLECTION, REGIONAL_DATA_COLLECTION,
    PROVINCIAL_DATA_COLLECTION, URL_NATIONAL_DATA, URL_REGIONAL_DATA,
    URL_PROVINCIAL_DATA, URL_LATEST_REGIONAL_DATA, URL_LATEST_PROVINCIAL_DATA,
    LATEST_REGIONAL_DATA_COLLECTION, LATEST_PROVINCIAL_DATA_COLLECTION,
    CP_DATAFILE_MONITOR, TOTAL_SWABS_KEY
)

NATIONAL_COLLECTION = mongo.db[NATIONAL_DATA_COLLECTION]
REGIONAL_COLLECTION = mongo.db[REGIONAL_DATA_COLLECTION]
LATEST_REGIONAL_COLLECTION = mongo.db[LATEST_REGIONAL_DATA_COLLECTION]
PROVINCIAL_COLLECTION = mongo.db[PROVINCIAL_DATA_COLLECTION]
LATEST_PROVINCIAL_COLLECTION = mongo.db[LATEST_PROVINCIAL_DATA_COLLECTION]

DATES = []
EXP_STATUS = []


def read_cached_data(data_filepath):
    """
    Read .json file
    :param data_filepath: str
    :return: JSON-serialised object
    """
    app.logger.warning(
        "Reading cache data at {}".format(data_filepath)
    )
    with open(data_filepath, 'r') as data_file:
        data = json.load(data_file)
    return data


def cache_data(data, data_filepath):
    """
    Save JSON-serialized object to file
    :param data: list or dict
    :param data_filepath: str
    :return: None
    """
    app.logger.info("Caching data at {}".format(data_filepath))
    with open(data_filepath, 'w') as data_file:
        json.dump(data, data_file)


def get_stats(data_type, today_data, yesterday_data, three_days_ago_data):
    """
    Return the stats of a given data_type.
    For the quantities whose values are provided as cumulative
    by the civil protection, the daily counts are computed as:
    cumulative(today) - cumulative(yesterday)
    :param data_type: str
    :param today_data: dict
    :param yesterday_data: dict
    :param three_days_ago_data: dict
    :return: dict
    """
    if data_type in CUSTOM_CARDS:
        today_total = today_data[CARD_MAP[data_type]]
        yesterday_total = yesterday_data[CARD_MAP[data_type]]
        three_days_ago_total = three_days_ago_data[CARD_MAP[data_type]]
        today_count = today_total - yesterday_total
        yesterday_count = yesterday_total - three_days_ago_total
        today_yesterday_diff = today_count - yesterday_count
        count = today_count
    elif data_type in CUMULATIVE_DATA_TYPES:
        today_total = today_data[data_type]
        yesterday_total = yesterday_data[data_type]
        three_days_ago_total = three_days_ago_data[data_type]
        today_yesterday_diff = today_total - yesterday_total
        yesterday_count = yesterday_total - three_days_ago_total
        count = today_total
    else:
        today_count = today_data[data_type]
        yesterday_count = yesterday_data[data_type]
        today_yesterday_diff = today_count - yesterday_count
        count = today_count
    if today_yesterday_diff < 0:
        status = "decrease"
    elif today_yesterday_diff == 0:
        status = "stable"
    else:
        status = "increase"
    if yesterday_count == 0 or today_yesterday_diff == 0:
        percentage_difference = "0.0%" \
            if today_yesterday_diff == 0 else "&#8734;"
    else:
        percentage_difference = "{0:+}%".format(round(
            ((today_yesterday_diff / yesterday_count) * 100), 1
        ))
    stats = {
        "count": count,
        "today_yesterday_diff": "{0:+}".format(today_yesterday_diff),
        "percentage_difference": percentage_difference,
        "status": status
    }
    return stats


def get_trends(data, province=False):
    """
    Return a list of dicts of the daily trend wrt to the previous day
    :param data: ascending sorted list of daily dicts
    :param province: bool
    :return: list of dicts
    """
    app.logger.debug("Building trends")
    if not province:
        card_types = CARD_TYPES
    else:
        card_types = [TOTAL_CASES_KEY]
    last = data[-1]
    penultimate = data[-2]
    third_tolast = data[-3]
    trend_cards = []
    for key in card_types:
        stats = get_stats(key, last, penultimate, third_tolast)
        trend_cards.append({
            "id": key,
            "title": VARS_CONFIG[key]["title"],
            "desc": VARS_CONFIG[key]["desc"],
            "longdesc": VARS_CONFIG[key]["longdesc"],
            "count": stats["count"],
            "colour": VARS_CONFIG[key][stats["status"]]["colour"],
            "icon": VARS_CONFIG[key]["icon"],
            "status_icon": VARS_CONFIG[key][stats["status"]]["icon"],
            "tooltip": VARS_CONFIG[key][stats["status"]]["tooltip"],
            "percentage_difference": stats["percentage_difference"],
            "today_yesterday_diff": stats["today_yesterday_diff"]
        })
    return trend_cards


def fill_series(province=False):
    """
    Return the series array to be used in the chart
    :return: list
    """
    app.logger.debug("Filling series")
    if not province:
        series = [
            {
                "name": gettext(VARS_CONFIG[key]["title"]),
                "data": VARS_CONFIG[key]["data"]
            }
            for key in VARS_CONFIG if key not in CUSTOM_CARDS
        ]
    else:
        series = [{
            "name": gettext(VARS_CONFIG[TOTAL_CASES_KEY]["title"]),
            "data": VARS_CONFIG[TOTAL_CASES_KEY]["data"],
            "visible": "true"
        }]
    return series


def parse_national_data(national_data):
    """
    Return dates, series, trend_cards
    :param national_data: list of dicts
    :return:
        DATES: list,
        series: list,
        trend_cards: list
    """
    app.logger.debug("Parsing national data")
    trend_cards = get_trends(national_data)
    app.logger.debug("Filling national data")
    for d in national_data:
        fill_data(d)
    series = fill_series()
    return DATES, series, trend_cards


def parse_area_data(data, area):
    """
    Return dates, series, trend_cards
    :param data: dict
    :param area: str
    :return:
        DATES: list,
        series: list,
        trend_cards: list
    """
    app.logger.debug("Parsing area data")
    series, trend_cards = [], []
    if area in PROVINCES:
        app.logger.debug("Filling provincial data")
        subset = [
            r for r in data
            if r[PROVINCE_KEY] == area
        ]
        trend_cards = get_trends(subset, province=True)
        for d in data:
            if area == d[PROVINCE_KEY]:
                fill_data(d, province=True)
        series = fill_series(province=True)
    elif area in REGIONS:
        app.logger.debug("Filling regional data")
        subset = [r for r in data if r[REGION_KEY] == area]
        trend_cards = get_trends(subset)
        for d in data:
            if area == d[REGION_KEY]:
                fill_data(d)
        series = fill_series()
    return DATES, series, trend_cards


def fill_data(datum, province=False):
    """
    Fill the "data" lists in VARS_CONFIG
    :param datum: dict
    :param province: bool
    :return: None
    """
    if not province:
        for key in VARS_CONFIG:
            if key not in CUSTOM_CARDS:
                VARS_CONFIG[key]["data"].append(
                    datum[key] if datum[key] is not None else 0
                )
        EXP_STATUS.append([datum[TOTAL_CASES_KEY], datum[NEW_POSITIVE_KEY]])
    else:
        VARS_CONFIG[TOTAL_CASES_KEY][CP_DATE_KEY].append(
            datum[TOTAL_CASES_KEY]
        )
    date_dt = datum[CP_DATE_KEY]
    date_str = date_dt.strftime(CHART_DATE_FMT)
    DATES.append(date_str)


def init_data():
    """
    Empty all the "data" keys in VARS_CONFIG plus DATES and EXP_STATUS
    :return: None
    """
    app.logger.debug("Init dashboard data")
    for key in VARS_CONFIG:
        VARS_CONFIG[key]["data"] = []
    EXP_STATUS.clear()
    DATES.clear()


def latest_update(data):
    """
    Return the value of the key PCM_DATE_KEY of the last dict in data
    :param data: list
    :return: str
    """
    app.logger.debug("Getting latest update")
    date_dt = data[-1][CP_DATE_KEY]
    return date_dt.strftime(UPDATE_FMT)


def get_query_menu(area):
    """
    Return query_menu populated with the current day and the provided area
    :param area: str
    :return: dict
    """
    return {
        "national": {
            "full": {
                "collection": NATIONAL_COLLECTION,
                "query": {}
            }
        },
        "regional": {
            "full": {
                "collection": REGIONAL_COLLECTION,
                "query": {}
            },
            "area": {
                "collection": REGIONAL_COLLECTION,
                "query": {REGION_KEY: area}
            },
            "latest": {
                "collection": LATEST_REGIONAL_COLLECTION,
                "query": {}
            },
            "latest_area": {
                "collection": LATEST_REGIONAL_COLLECTION,
                "query": {REGION_KEY: area}
            }
        },
        "provincial": {
            "full": {
                "collection": PROVINCIAL_COLLECTION,
                "query": {}
            },
            "area": {
                "collection": PROVINCIAL_COLLECTION,
                "query": {PROVINCE_KEY: area}
            },
            "latest": {
                "collection": LATEST_PROVINCIAL_COLLECTION,
                "query": {}
            },
            "latest_area": {
                "collection": LATEST_PROVINCIAL_COLLECTION,
                "query": {PROVINCE_KEY: area}
            }
        },
    }


def get_covid_data(**menu):
    """
    Return data from the DB according to the provided menu
    :param menu: dict
    :return: list
    """
    area = menu.get("area")
    data_type = menu.get("data_type")
    query_type_dict = menu.get("query_type")
    query_menu = get_query_menu(area)
    query_type_dict = query_menu[data_type][query_type_dict]
    query = query_type_dict["query"]
    collection = query_type_dict["collection"]
    data = list(collection.find(query))
    app.logger.debug(
        "data_type {}, query {}, {}".format(data_type, query, len(data))
    )
    return data


def enrich_frontend_data(area=None, **data):
    """
    Return a data dict to be rendered which is an augmented copy of
    DASHBOARD_DATA defined in config.py
    :param area: optional, str
    :param data: **kwargs
    :return: dict
    """
    app.logger.debug("Enriching data to dashboard")
    try:
        data["area"] = area
    except KeyError:
        pass
    data.update(DASHBOARD_DATA)
    return data


def get_regional_breakdown(covid_data):
    """
    Return a dict whose keys are the COVID dataset variables
    and the values are lists of dicts whose keys are "region" and "count".
    Example:
    {
      'nuovi_positivi': [
        {'region': 'Abruzzo', 'count': 1}, ...{'region': 'Veneto', 'count': 55}
      ],
      'ricoverati_con_sintomi': [
        {'region': 'Abruzzo', 'count': 17}, ...
      ]
    }
    :param covid_data: list of dicts
    :return: dict
    """
    breakdown = {}
    for _type in CARD_TYPES:
        if _type not in CUSTOM_CARDS:
            breakdown[_type] = [{
                "area": d[REGION_KEY],
                "count": d[_type],
                "url": "/regions/{}".format(d[REGION_KEY])
            }
                for d in covid_data
                if d[_type] != 0 and d[REGION_KEY] in REGIONS
            ]
    return breakdown


def get_provincial_breakdown(covid_data, region):
    """
    Return a dict whose key is TOTAL_CASE_KEY and its value
    is a list of dicts each containing area and relative count
    :param covid_data: list of dicts
    :param region: str
    :return: dict
    """
    return {
        TOTAL_CASES_KEY: [{
            "area": d[PROVINCE_KEY],
            "count": d[TOTAL_CASES_KEY],
            "url": "/provinces/{}".format(d[PROVINCE_KEY])
        }
            for d in covid_data
            if d[REGION_KEY] == region and d[PROVINCE_KEY] in PROVINCES
        ]
    }


def get_positive_swabs_percentage(latest_data, area=None):
    """
    Return the percentage of positive swabs
    :param latest_data: list
    :param area: str
    :return: str
    """
    positive_swabs_percentage = "0%"
    latest_new_positive = latest_data[-1][NEW_POSITIVE_KEY]
    latest_daily_swabs = (
        latest_data[-1][TOTAL_SWABS_KEY] - latest_data[-2][TOTAL_SWABS_KEY]
    )
    if latest_daily_swabs != 0:
        if area is None:
            last_week_data = get_last_week_national_data()
        else:
            last_week_data = get_last_week_regional_data(area)
        last_week_daily_swabs = (
            last_week_data[1][TOTAL_SWABS_KEY] -
            last_week_data[0][TOTAL_SWABS_KEY])

        last_week_new_positive = last_week_data[1][NEW_POSITIVE_KEY]
        last_week_positive_swabs_percentage = (
            last_week_new_positive / last_week_daily_swabs
        )
        latest_positive_swabs_percentage = (
                latest_new_positive / latest_daily_swabs)
        positive_swabs_percentage = (
                latest_positive_swabs_percentage /
                last_week_positive_swabs_percentage
        )
        positive_swabs_percentage = round(positive_swabs_percentage, 1)
        positive_swabs_percentage = (
            "{0:+}%".format(positive_swabs_percentage))
    return positive_swabs_percentage


def rubbish_notes(notes):
    """
    Return True if note matches the regex, else otherwise
    :param notes: str
    :return: bool
    """
    regex = re.compile(RUBBISH_NOTE_REGEX)
    return regex.search(notes)


def get_notes(latest_data, area=None):
    """
    Return the notes from the 'note' key in the list of dicts 'latest_data'.
    Get the notes string from latest_data[0]['note'] if area is None
    and therefore latest_data is the latest national data (only 1 entry);
    otherwise, get the notes from the matching area in the data.
    Return the notes in the data otherwise empty string when
    the received note string is None or matches the RUBBISH_NOTE_REGEX
    :param latest_data: list
    :param area: str
    :return: str
    """
    notes = ""
    if area is None:
        notes = latest_data[0][NOTE_KEY]
    else:
        for d in latest_data:
            try:
                if d[REGION_KEY] == area:
                    notes = d[NOTE_KEY]
            except KeyError:
                if d[PROVINCE_KEY] == area:
                    notes = d[NOTE_KEY]
    return notes if notes is not None and not rubbish_notes(notes) else ""


def transform_data(data):
    """
    Return a list of dicts like the one passed with the only difference:
    each dict in data will have the value of its key, CP_DATE_KEY,
    string-parsed to a datetime object
     The
    :param data: list
    :return: data: list
    """
    for d in data:
        d[CP_DATE_KEY] = dt.datetime.strptime(d[CP_DATE_KEY], CP_DATE_FMT)
    return data


def drop_and_recreate(collection, data):
    """
    Drop a collection, recreate it and serially fill it with the given data
    :param collection: pymongo collection
    :param data: list
    :return: None
    """
    collection.drop()
    collection.insert_many(data, ordered=True)


def get_cp_data(url):
    """
    Get data from CP repo
    :param url: str
    :return: list
    """
    data = []
    try:
        data = requests.get(url).json()
    except Exception as e:
        app.logger.error("{}".format(e))
    return data


def update_collections():
    """
    Update the collections on mongo with the various data from the CP repo
    :return: None
    """
    national_cp_data = get_cp_data(URL_NATIONAL_DATA)
    regional_cp_data = get_cp_data(URL_REGIONAL_DATA)
    provincial_cp_data = get_cp_data(URL_PROVINCIAL_DATA)
    latest_regional_pc_data = get_cp_data(URL_LATEST_REGIONAL_DATA)
    latest_provincial_cp_data = get_cp_data(URL_LATEST_PROVINCIAL_DATA)
    national_data = transform_data(national_cp_data)
    regional_data = transform_data(regional_cp_data)
    provincial_data = transform_data(provincial_cp_data)
    latest_regional_data = transform_data(latest_regional_pc_data)
    latest_provincial_data = transform_data(latest_provincial_cp_data)
    app.logger.warning("Dropping and recreating national collection")
    drop_and_recreate(NATIONAL_COLLECTION, national_data)
    app.logger.warning("Dropping and recreating regional collection")
    drop_and_recreate(REGIONAL_COLLECTION, regional_data)
    app.logger.warning("Dropping and recreating provincial collection")
    drop_and_recreate(PROVINCIAL_COLLECTION, provincial_data)
    app.logger.warning("Dropping and recreating latest regional collection")
    drop_and_recreate(LATEST_REGIONAL_COLLECTION, latest_regional_data)
    app.logger.warning("Dropping and recreating latest provincial collection")
    drop_and_recreate(LATEST_PROVINCIAL_COLLECTION, latest_provincial_data)


def need_update(payload):
    """
    Return a bool do_update and a list of modified_files
    :param payload: dict
    :return:
        do_update: bool: if True will update collection, else will not
        modified_files: list: last civil-protection commit modified files
    """
    modified_files = []
    commits = payload.get("commits")
    do_update = False
    if commits is not None:
        for c in commits:
            commit_modified_files = c.get("modified")
            if commit_modified_files is not None:
                modified_files.extend(commit_modified_files)
        app.logger.debug("Modified files: {}".format(modified_files))
        if any(CP_DATAFILE_MONITOR in _file for _file in modified_files):
            do_update = True
    return do_update, modified_files


def get_last_week_national_data():
    """
    Return the national data of the week before the last record in the db
    :return: list
    """
    last_week_national_data = None
    try:
        cursor = NATIONAL_COLLECTION.find()
        last = list(cursor)[-1][CP_DATE_KEY]
        week_before_last = last - dt.timedelta(days=8)
        cursor = NATIONAL_COLLECTION.find({
            CP_DATE_KEY: {
                "$gte": week_before_last,
                "$lt": dt.datetime.today()
            }
        })
        last_week_national_data = list(cursor)
    except Exception as e:
        app.logger.error("{}".format(e))
    return last_week_national_data


def get_last_week_regional_data(area=None):
    """
    Return the all the regional data of the week before the last record in
    the db if area is None. Otherwise the data of the week before the last
    record in the db corresponding to the provided area
    :param area: str
    :return: dict or list
    """
    cursor = REGIONAL_COLLECTION.find()
    last = list(cursor)[-1][CP_DATE_KEY]
    week_before_last = last - dt.timedelta(days=7)
    if area is None:
        query = {}
    else:
        query = {
            REGION_KEY: area,
            CP_DATE_KEY: {
                "$gte": week_before_last,
                "$lt": dt.datetime.today()
            }
        }
    cursor = REGIONAL_COLLECTION.find(query)
    last_week_regional_data = list(cursor)
    return last_week_regional_data
