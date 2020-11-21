import datetime as dt
import re

import pandas as pd
from flask import current_app as app
from flask_babel import gettext

from app.db.collections import (
    NATIONAL_DATA, NATIONAL_TRENDS, NATIONAL_SERIES,
    REGIONAL_DATA, REGIONAL_TRENDS, REGIONAL_SERIES, REGIONAL_BREAKDOWN,
    PROVINCIAL_DATA, PROVINCIAL_TRENDS, PROVINCIAL_SERIES,
    PROVINCIAL_BREAKDOWN
)
from config import (
    PROVINCE_KEY, REGION_KEY, DATE_KEY, UPDATE_FMT, RUBBISH_NOTE_REGEX, NOTE_KEY,
    DAILY_POSITIVITY_INDEX, REGIONS, PROVINCES, CRITICAL_AREAS_DAY, PHASE3_DAY,
    PHASE2_DAY, LOCKDOWN_DAY, VARS, VERSION, ITALY_MAP
)

DATA_SERIES = [
    VARS[key]["title"]
    for key in VARS
]
DASHBOARD_DATA = {
    "vars_config": VARS,
    "data_series": DATA_SERIES,
    "italy_map": ITALY_MAP,
    "VERSION": VERSION,
    "regions": REGIONS,
    "provinces": PROVINCES,
    "days_in_phase3": (CRITICAL_AREAS_DAY - PHASE3_DAY).days,
    "days_in_phase2": (PHASE3_DAY - PHASE2_DAY).days,
    "days_in_lockdown": (PHASE2_DAY - LOCKDOWN_DAY).days,
    "days_since_critical_areas": (
            dt.datetime.today() - CRITICAL_AREAS_DAY).days
}


def get_latest_update(data_type="national"):
    """
    Return the value of the key PCM_DATE_KEY of the last dict in data
    :return: str
    """
    app.logger.debug("Getting latest update")
    query_menu = {
        "national": {
            "collection": NATIONAL_DATA
        },
        "regional": {
            "collection": REGIONAL_DATA
        },
        "provincial": {
            "collection": PROVINCIAL_DATA
        }
    }
    collection = query_menu[data_type]["collection"]
    doc = next(collection.find({}).sort([(DATE_KEY, -1)]).limit(1))
    return doc[DATE_KEY].strftime(UPDATE_FMT)


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


def rubbish_notes(notes):
    """
    Return True if note matches the regex, else otherwise
    :param notes: str
    :return: bool
    """
    regex = re.compile(RUBBISH_NOTE_REGEX)
    return regex.search(notes)


def get_notes(notes_type="national", area=None):
    """
    Return the notes in the data otherwise empty string when
    the received note is 0 or matches the RUBBISH_NOTE_REGEX
    :param notes_type: str
    :param area: str
    :return: str
    """
    query_menu = {
        "national": {
            "query": {},
            "collection": NATIONAL_DATA
        },
        "regional": {
            "query": {REGION_KEY: area},
            "collection": REGIONAL_DATA
        },
        "provincial": {
            "query": {PROVINCE_KEY: area},
            "collection": PROVINCIAL_DATA
        }
    }
    query = query_menu[notes_type]["query"]
    collection = query_menu[notes_type]["collection"]
    doc = next(collection.find(query).sort([(DATE_KEY, -1)]).limit(1))
    notes = doc[NOTE_KEY] if doc[NOTE_KEY] != 0 else None
    return notes if notes is not None and not rubbish_notes(notes) else ""


def get_national_cards():
    return list(NATIONAL_TRENDS.find({}))


def get_regional_cards(region):
    """
    Return a list of regional cards for a given region
    :param region: str
    :return: list
    """
    doc = REGIONAL_TRENDS.find_one({REGION_KEY: region})
    return doc["trends"]


def get_provincial_cards(province):
    """
    Return a list of provincial cards for a given province
    :param province: str
    :return: list
    """
    doc = PROVINCIAL_TRENDS.find_one({PROVINCE_KEY: province})
    return doc["trends"]


def get_regional_breakdown():
    return REGIONAL_BREAKDOWN.find_one({}, {"_id": False})


def get_provincial_breakdown(region):
    return PROVINCIAL_BREAKDOWN.find_one(
        {REGION_KEY: region}, {"_id": False})["breakdowns"]


def translate_series_lang(series):
    """
    Return a modified version of the series input dict with the
    "name" values babel translated
    :param series: dict
    :return: dict
    """
    daily_series = series.get("daily")
    current_series = series.get("current")
    cum_series = series.get("cum")
    if daily_series is not None:
        for s in daily_series:
            s["name"] = gettext(s["name"])
    if current_series is not None:
        for s in current_series:
            s["name"] = gettext(s["name"])
    if cum_series is not None:
        for s in cum_series:
            s["name"] = gettext(s["name"])
    return series


def get_national_series():
    series = NATIONAL_SERIES.find_one({}, {"_id": False})
    return translate_series_lang(series)


def get_regional_series(region):
    series = REGIONAL_SERIES.find_one({REGION_KEY: region}, {"_id": False})
    return translate_series_lang(series)


def get_provincial_series(province):
    series = PROVINCIAL_SERIES.find_one(
        {PROVINCE_KEY: province}, {"_id": False})
    return translate_series_lang(series)


def get_positivity_idx(area_type="national", area=None):
    """
    Return the positivity index for either the national or the regional
    views
    :param area_type: str: "national" or "regional"
    :param area: str
    :return: str
    """
    query_menu = {
        "national": {
            "collection": NATIONAL_DATA,
            "query": {}
        },
        "regional": {
            "collection": REGIONAL_DATA,
            "query": {REGION_KEY: area}
        }
    }
    query = query_menu[area_type]["query"]
    collection = query_menu[area_type]["collection"]
    doc = next(collection.find(query).sort([(DATE_KEY, -1)]).limit(1))
    return f"{round(doc[DAILY_POSITIVITY_INDEX])}%"


def get_national_data():
    cursor = NATIONAL_DATA.find({})
    return pd.DataFrame(list(cursor))


def get_region_data(region):
    cursor = REGIONAL_DATA.find({REGION_KEY: region})
    return pd.DataFrame(list(cursor))


def get_province_data(province):
    cursor = PROVINCIAL_DATA.find({PROVINCE_KEY: province})
    return pd.DataFrame(list(cursor))
