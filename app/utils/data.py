import re

from flask import current_app as app

from app.db.collections import (
    NATIONAL_DATA, NATIONAL_TRENDS, NATIONAL_SERIES,
    REGIONAL_DATA, REGIONAL_TRENDS, REGIONAL_SERIES, REGIONAL_BREAKDOWN,
    PROVINCIAL_DATA, PROVINCIAL_TRENDS, PROVINCIAL_SERIES, PROVINCIAL_BREAKDOWN
)
from config import (
    PROVINCE_KEY, REGION_KEY, DATE_KEY, UPDATE_FMT,
    DASHBOARD_DATA, RUBBISH_NOTE_REGEX, NOTE_KEY
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


def get_national_series():
    return NATIONAL_SERIES.find_one({}, {"_id": False})


def get_regional_series(region):
    return REGIONAL_SERIES.find_one(
        {REGION_KEY: region}, {"_id": False})


def get_provincial_series(province):
    return PROVINCIAL_SERIES.find_one(
        {PROVINCE_KEY: province}, {"_id": False})


def get_swabs_percentage(area_type="national"):
    query_menu = {
        "national": {
            "collection": NATIONAL_DATA
        },
        "regional": {
            "collection": REGIONAL_DATA
        }
    }
    collection = query_menu[area_type]["collection"]
    doc = next(collection.find().sort([(DATE_KEY, -1)]).limit(1))
    return "{0:+}%".format(round(doc["tamponi_perc"]))
