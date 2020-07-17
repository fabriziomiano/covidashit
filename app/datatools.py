import datetime as dt
import json

import requests
from flask import current_app
from flask_babel import gettext

from config import (
    CUSTOM_CARDS, CARD_MAP, CARD_TYPES, PROVINCES, PROVINCE_KEY,
    REGIONS, REGION_KEY, PCM_DATE_FMT, CHART_DATE_FMT, PCM_DATE_KEY,
    UPDATE_FMT, URL_NATIONAL_DATA, NATIONAL_DATA_FILE, URL_REGIONAL_DATA,
    REGIONAL_DATA_FILE, URL_PROVINCIAL_DATA, PROVINCIAL_DATE_FILE,
    DATA_TO_FRONTEND, VARS_CONFIG, LATEST_REGIONAL_DATA_FILE,
    URL_LATEST_REGIONAL_DATA, URL_LATEST_PROVINCIAL_DATA, TOTAL_CASES_KEY
)

DATES = []
ICU = []
HOSP_W_SYMPTS = []
TOT_DEATHS = []
TOT_HOSP = []
SELF_ISOL = []
TOT_POS = []
NEW_POS = []
TOT_SWABS = []
HEALED = []
TOT_CASES = []
TOT_POS_VAR = []
EXP_STATUS = []
ALL_DATA = [
    DATES, ICU, HOSP_W_SYMPTS, TOT_DEATHS, TOT_HOSP, SELF_ISOL, TOT_POS,
    NEW_POS, TOT_SWABS, HEALED, TOT_CASES, TOT_POS_VAR, EXP_STATUS
]


def read_cached_data(data_filepath):
    """
    Read .json file
    :param data_filepath:
    :return: JSON-serialised object
    """
    with open(data_filepath, 'r') as data_file:
        data = json.load(data_file)
    return data


def cache_data(data, data_filepath):
    """
    Save JSON-serialized object to file
    :param data:
    :param data_filepath:
    :return: None
    """
    with open(data_filepath, 'w') as data_file:
        json.dump(data, data_file)


def get_stats(key, last, penultimate, third_tolast):
    """
    Return count and status of a given data type
    :param key: str
    :param last: dict
    :param penultimate: dict
    :param third_tolast: dict
    :return: dict
    """
    if key not in CUSTOM_CARDS:
        count = last[key]
        if int(penultimate[key]) > int(last[key]):
            status = "decrease"
        elif penultimate[key] == last[key]:
            status = "stable"
        else:
            status = "increase"
    else:
        count = int(last[CARD_MAP[key]]) - int(penultimate[CARD_MAP[key]])
        today_diff = int(last[CARD_MAP[key]]) - int(penultimate[CARD_MAP[key]])
        yesterday_count = int(penultimate[CARD_MAP[key]])
        day_before_yesterday_count = int(third_tolast[CARD_MAP[key]])
        yesterday_diff = yesterday_count - day_before_yesterday_count
        if today_diff < yesterday_diff:
            status = "decrease"
        elif today_diff == yesterday_diff:
            status = "stable"
        else:
            status = "increase"
    stats = {
        "count": count,
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
            "tooltip": VARS_CONFIG[key][stats["status"]]["tooltip"]
        })
    return trend_cards


def fill_series(province=False):
    """
    Return the series array to be used in the chart
    :return: list
    """
    if not province:
        series1 = {
            "name": gettext(VARS_CONFIG["nuovi_positivi"]["title"]),
            "data": NEW_POS
        }
        series2 = {
            "name": gettext(
                VARS_CONFIG["variazione_totale_positivi"]["title"]),
            "data": TOT_POS_VAR
        }
        series3 = {
            "name": gettext(VARS_CONFIG["terapia_intensiva"]["title"]),
            "data": ICU
        }
        series4 = {
            "name": gettext(VARS_CONFIG["deceduti"]["title"]),
            "data": TOT_DEATHS
        }
        series5 = {
            "name": gettext(VARS_CONFIG["dimessi_guariti"]["title"]),
            "data": HEALED
        }
        series6 = {
            "name": gettext(VARS_CONFIG["ricoverati_con_sintomi"]["title"]),
            "data": HOSP_W_SYMPTS
        }
        series7 = {
            "name": gettext(VARS_CONFIG["totale_ospedalizzati"]["title"]),
            "data": TOT_HOSP
        }
        series8 = {
            "name": gettext(VARS_CONFIG["isolamento_domiciliare"]["title"]),
            "data": SELF_ISOL
        }
        series9 = {
            "name": gettext(VARS_CONFIG["totale_positivi"]["title"]),
            "data": TOT_POS,
            "visible": "true"
        }
        series10 = {
            "name": gettext(VARS_CONFIG["totale_casi"]["title"]),
            "data": TOT_CASES
        }
        series11 = {
            "name": gettext(VARS_CONFIG["tamponi"]["title"]),
            "data": TOT_SWABS
        }
        series = [
            series1, series2, series3, series4, series5,
            series6, series7, series8, series9, series10,
            series11
        ]
    else:
        series = [{
            "name": gettext(VARS_CONFIG["totale_casi"]["title"]),
            "data": TOT_CASES,
            "visible": "true"
        }]
    return series


def parse_data(data, area=None):
    """
    Return dates, series, trend_cards
    :param data: dict
    :param area: str
    :return:
        DATES: list,
        series: list,
        trend_cards: list
    """
    series = []
    trend_cards = []
    if area is None:
        national_data = data["national"]
        trend_cards = get_trends(national_data)
        for d in national_data:
            fill_data(d)
        series = fill_series()
    else:
        if area in PROVINCES:
            provincial_data = data["provincial"]
            subset = [
                r for r in provincial_data
                if r[PROVINCE_KEY] == area
            ]
            trend_cards = get_trends(subset, province=True)
            for d in provincial_data:
                if area == d[PROVINCE_KEY]:
                    fill_data(d, province=True)
            series = fill_series(province=True)
        elif area in REGIONS:
            regional_data = data["regional"]
            subset = [r for r in regional_data if r[REGION_KEY] == area]
            trend_cards = get_trends(subset)
            for d in regional_data:
                if area == d[REGION_KEY]:
                    fill_data(d)
            series = fill_series()
    return DATES, series, trend_cards


def fill_data(datum, province=False):
    """
    Fill the data series lists
    :param datum: dict
    :param province: bool
    :return: None
    """
    if not province:
        ICU.append(datum["terapia_intensiva"])
        HOSP_W_SYMPTS.append(datum["ricoverati_con_sintomi"])
        TOT_DEATHS.append(datum["deceduti"])
        HEALED.append(datum["dimessi_guariti"])
        TOT_HOSP.append(datum["totale_ospedalizzati"])
        SELF_ISOL.append(datum["isolamento_domiciliare"])
        TOT_POS.append(datum["totale_positivi"])
        NEW_POS.append(datum["nuovi_positivi"])
        TOT_SWABS.append(datum["tamponi"])
        TOT_POS_VAR.append(datum["variazione_totale_positivi"])
        EXP_STATUS.append([datum["totale_casi"], datum["nuovi_positivi"]])
    date_dt = dt.datetime.strptime(datum["data"], PCM_DATE_FMT)
    date_str = date_dt.strftime(CHART_DATE_FMT)
    DATES.append(date_str)
    TOT_CASES.append(datum["totale_casi"])


def init_data():
    """
    Empty data series in DATA
    :return: None
    """
    for data_type in ALL_DATA:
        data_type.clear()


def latest_update(data):
    """
    Return the value of the key PCM_DATE_KEY of the last dict in data
    :param data: list
    :return: str
    """
    date_dt = dt.datetime.strptime(data[-1][PCM_DATE_KEY], PCM_DATE_FMT)
    return date_dt.strftime(UPDATE_FMT)


def get_national_data():
    """
    Return the national data from the "Protezione Civile" repository
    :return: dict
    """
    data = {}
    try:
        response = requests.get(URL_NATIONAL_DATA, timeout=3)
        status = response.status_code
        if status == 200:
            national_data = response.json()
            data["national"] = sorted(
                national_data, key=lambda x: x[PCM_DATE_KEY]
            )
            cache_data(data["national"], NATIONAL_DATA_FILE)
        else:
            current_app.logger.error(
                "Could not get data: ERROR {}".format(status)
            )
            data["national"] = read_cached_data(NATIONAL_DATA_FILE)
    except Exception as e:
        current_app.logger.error("Request Error {}".format(e))
        data["national"] = read_cached_data(NATIONAL_DATA_FILE)
    return data


def get_regional_data():
    """
    Return the regional data from the "Protezione Civile" repository
    :return: dict
    """
    data = {}
    try:
        response = requests.get(URL_REGIONAL_DATA, timeout=3)
        status = response.status_code
        if status == 200:
            regional_data = response.json()
            data["regional"] = sorted(
                regional_data, key=lambda x: x[PCM_DATE_KEY]
            )
            cache_data(data["regional"], REGIONAL_DATA_FILE)
        else:
            current_app.logger.error(
                "Could not get data: ERROR {}".format(status))
            data["regional"] = read_cached_data(REGIONAL_DATA_FILE)
    except Exception as e:
        current_app.logger.error("Request Error {}".format(e))
        data["regional"] = read_cached_data(REGIONAL_DATA_FILE)
    return data


def get_latest_regional_data():
    """
    Return the latest regional data from the "Protezione Civile" repository
    :return: dict
    """
    data = {}
    try:
        response = requests.get(URL_LATEST_REGIONAL_DATA, timeout=3)
        status = response.status_code
        if status == 200:
            latest_regional_data = response.json()
            data["latest_regional"] = sorted(
                latest_regional_data, key=lambda x: x[PCM_DATE_KEY]
            )
            cache_data(data["latest_regional"], LATEST_REGIONAL_DATA_FILE)
        else:
            current_app.logger.error(
                "Could not get data: ERROR {}".format(status))
            data["regional"] = read_cached_data(LATEST_REGIONAL_DATA_FILE)
    except Exception as e:
        current_app.logger.error("Request Error {}".format(e))
        data["latest_regional"] = read_cached_data(LATEST_REGIONAL_DATA_FILE)
    return data


def get_provincial_data():
    """
    Return the provincial data from the "Protezione Civile" repository
    :return: dict
    """
    data = {}
    try:
        response = requests.get(URL_PROVINCIAL_DATA, timeout=3)
        status = response.status_code
        if status == 200:
            prov_data = response.json()
            data["provincial"] = sorted(
                prov_data, key=lambda x: x[PCM_DATE_KEY]
            )
            cache_data(data["provincial"], PROVINCIAL_DATE_FILE)
        else:
            current_app.logger.error(
                "Could not get data: ERROR {}".format(status)
            )
            data["provincial"] = read_cached_data(PROVINCIAL_DATE_FILE)
    except Exception as e:
        current_app.logger.error("Request Error {}".format(e))
        data["provincial"] = read_cached_data(PROVINCIAL_DATE_FILE)
    return data


def get_latest_provincial_data():
    """
    Return the latest provincial data from the "Protezione Civile" repository
    :return: dict
    """
    data = {}
    try:
        response = requests.get(URL_LATEST_PROVINCIAL_DATA, timeout=3)
        status = response.status_code
        if status == 200:
            prov_data = response.json()
            data["latest_provincial"] = sorted(
                prov_data, key=lambda x: x[PCM_DATE_KEY]
            )
            cache_data(data["latest_provincial"], PROVINCIAL_DATE_FILE)
        else:
            current_app.logger.error(
                "Could not get data: ERROR {}".format(status)
            )
            data["latest_provincial"] = read_cached_data(PROVINCIAL_DATE_FILE)
    except Exception as e:
        current_app.logger.error("Request Error {}".format(e))
        data["latest_provincial"] = read_cached_data(PROVINCIAL_DATE_FILE)
    return data


def frontend_data(area=None, **data):
    """
    Return a data dict to be rendered which is an augmented copy of
    DATA_TO_FRONTEND defined in config.py
    :param area: optional, str
    :param data: **kwargs
    :return: dict
    """
    try:
        data["area"] = area
    except KeyError:
        pass
    data.update(DATA_TO_FRONTEND)
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
