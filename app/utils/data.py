import datetime as dt
import json

import requests
from flask import current_app
from flask_babel import gettext

from config import (
    CUSTOM_CARDS, CARD_MAP, CARD_TYPES, VARS_CONFIG, PROVINCES,
    PROVINCE_KEY, REGIONS, REGION_KEY, PCM_DATE_FMT, CHART_DATE_FMT,
    PCM_DATE_KEY, UPDATE_FMT, DATA_TYPE, DASHBOARD_DATA, TOTAL_CASES_KEY
)

DATES = []
EXP_STATUS = []


def read_cached_data(data_filepath):
    """
    Read .json file
    :param data_filepath: str
    :return: JSON-serialised object
    """
    current_app.logger.warning(
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
    current_app.logger.info("Caching data at {}".format(data_filepath))
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
    if data_type not in CUSTOM_CARDS:
        today_count = today_data[data_type]
        yesterday_count = yesterday_data[data_type]
    else:
        today_total = today_data[CARD_MAP[data_type]]
        yesterday_total = yesterday_data[CARD_MAP[data_type]]
        three_days_ago_total = three_days_ago_data[CARD_MAP[data_type]]
        today_count = today_total - yesterday_total
        yesterday_count = yesterday_total - three_days_ago_total
    today_yesterday_diff = today_count - yesterday_count
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
            ((today_yesterday_diff / abs(yesterday_count)) * 100), 1
        ))
    stats = {
        "count": today_count,
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
    current_app.logger.debug("Building trends")
    if not province:
        card_types = CARD_TYPES
    else:
        card_types = ["totale_casi"]
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
    current_app.logger.debug("Filling series")
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
            "name": gettext(VARS_CONFIG["totale_casi"]["title"]),
            "data": VARS_CONFIG["totale_casi"]["data"],
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
    current_app.logger.debug("Parsing national data")
    trend_cards = get_trends(national_data)
    current_app.logger.debug("Filling national data")
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
    current_app.logger.debug("Parsing area data")
    series, trend_cards = [], []
    if area in PROVINCES:
        current_app.logger.debug("Filling provincial data")
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
        current_app.logger.debug("Filling regional data")
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
        EXP_STATUS.append([datum["totale_casi"], datum["nuovi_positivi"]])
    else:
        VARS_CONFIG["totale_casi"]["data"].append(datum["totale_casi"])
    date_dt = dt.datetime.strptime(datum["data"], PCM_DATE_FMT)
    date_str = date_dt.strftime(CHART_DATE_FMT)
    DATES.append(date_str)


def init_data():
    """
    Empty all the "data" keys in VARS_CONFIG plus DATES and EXP_STATUS
    :return: None
    """
    current_app.logger.debug("Init dashboard data")
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
    current_app.logger.debug("Getting latest update")
    date_dt = dt.datetime.strptime(data[-1][PCM_DATE_KEY], PCM_DATE_FMT)
    return date_dt.strftime(UPDATE_FMT)


def get_covid_data(data_type):
    """
    Return the national data from the "Protezione Civile" repository
    :return: list of dicts
    """
    current_app.logger.debug("Getting {} data".format(data_type))
    data_url = DATA_TYPE[data_type]["url"]
    cached_data_file = DATA_TYPE[data_type]["cache_file"]
    try:
        response = requests.get(data_url, timeout=3)
        status = response.status_code
        if status == 200:
            national_data = response.json()
            data = sorted(
                national_data, key=lambda x: x[PCM_DATE_KEY]
            )
            cache_data(data, cached_data_file)
        else:
            current_app.logger.error(
                "Could not get data: ERROR {}".format(status)
            )
            data = read_cached_data(cached_data_file)
    except Exception as e:
        current_app.logger.error("Request Error {}".format(e))
        data = read_cached_data(cached_data_file)
    return data


def enrich_frontend_data(area=None, **data):
    """
    Return a data dict to be rendered which is an augmented copy of
    DASHBOARD_DATA defined in config.py
    :param area: optional, str
    :param data: **kwargs
    :return: dict
    """
    current_app.logger.debug("Enriching data to dashboard")
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
