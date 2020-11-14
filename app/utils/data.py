import re

from flask import current_app as app
from flask_babel import gettext

from app.db.collections import (
    NATIONAL_DATA, NATIONAL_TRENDS, NATIONAL_SERIES,
    REGIONAL_DATA, REGIONAL_TRENDS, REGIONAL_SERIES, REGIONAL_BREAKDOWN,
    PROVINCIAL_DATA, PROVINCIAL_TRENDS, PROVINCIAL_SERIES, PROVINCIAL_BREAKDOWN
)
from config import (
    PROVINCE_KEY, REGION_KEY, DATE_KEY, UPDATE_FMT, DASHBOARD_DATA,
    RUBBISH_NOTE_REGEX, NOTE_KEY, DAILY_POSITIVITY_INDEX
)


def latest_update(data_type="national"):
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
    doc = REGIONAL_TRENDS.find_one({REGION_KEY: region})
    return doc["trends"]


def get_provincial_cards(province):
    doc = PROVINCIAL_TRENDS.find_one({PROVINCE_KEY: province})
    return doc["trends"]


def get_regional_breakdown():
    return REGIONAL_BREAKDOWN.find_one({}, {"_id": False})


def get_provincial_breakdown(region):
    return PROVINCIAL_BREAKDOWN.find_one(
        {REGION_KEY: region}, {"_id": False})["breakdowns"]


def translate_series_lang(series):
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
