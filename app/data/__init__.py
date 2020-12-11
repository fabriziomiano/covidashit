"""
Data Module
"""
import datetime as dt

import pandas as pd
from flask import current_app as app

from app.db import (
    NAT_DATA_COLL, NAT_TRENDS_COLL,  NAT_SERIES_COLL, REG_DATA_COLL,
    REG_TRENDS_COLL, REG_SERIES_COLL, REG_BREAKDOWN_COLL, PROV_DATA_COLL,
    PROV_TRENDS_COLL, PROV_SERIES_COLL, PROV_BREAKDOWN_COLL
)
from app.utils import rubbish_notes, translate_series_lang
from config import (
    REGION_KEY, PROVINCE_KEY, DATE_KEY, NOTE_KEY, DAILY_POSITIVITY_INDEX,
    UPDATE_FMT, VARS, ITALY_MAP, VERSION, REGIONS, PROVINCES,
    CRITICAL_AREAS_DAY, PHASE3_DAY, PHASE2_DAY, LOCKDOWN_DAY, TOTAL_CASES_KEY,
    NEW_POSITIVE_KEY
)


DATA_SERIES = [VARS[key]["title"] for key in VARS]
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


CUM_QUANTITIES = [qty for qty in VARS if VARS[qty]["type"] == "cum"]
NON_CUM_QUANTITIES = [qty for qty in VARS if VARS[qty]["type"] == "current"]
DAILY_QUANTITIES = [qty for qty in VARS if VARS[qty]["type"] == "daily"]
TREND_CARDS = [qty for qty in VARS if not qty.endswith("_ma")]
PROV_TREND_CARDS = [TOTAL_CASES_KEY, NEW_POSITIVE_KEY]


def get_query_menu(area=None):
    """
    Return the query menu
    :param area: str
    :return: dict
    """
    return {
        "national": {
            "query": {},
            "collection": NAT_DATA_COLL
        },
        "regional": {
            "query": {REGION_KEY: area},
            "collection": REG_DATA_COLL
        },
        "provincial": {
            "query": {PROVINCE_KEY: area},
            "collection": PROV_DATA_COLL
        }
    }


def get_notes(notes_type="national", area=None):
    """
    Return the notes in the data otherwise empty string when
    the received note is 0 or matches the RUBBISH_NOTE_REGEX
    :param notes_type: str
    :param area: str
    :return: str
    """
    query_menu = get_query_menu(area)
    query = query_menu[notes_type]["query"]
    collection = query_menu[notes_type]["collection"]
    doc = next(collection.find(query).sort([(DATE_KEY, -1)]).limit(1))
    notes = doc[NOTE_KEY] if doc[NOTE_KEY] != 0 else None
    return notes if notes is not None and not rubbish_notes(notes) else ""


def get_national_cards():
    """Return national cards from DB"""
    return list(NAT_TRENDS_COLL.find({}))


def get_regional_cards(region):
    """
    Return a list of regional cards for a given region
    :param region: str
    :return: list
    """
    doc = REG_TRENDS_COLL.find_one({REGION_KEY: region})
    return doc["trends"]


def get_provincial_cards(province):
    """
    Return a list of provincial cards for a given province
    :param province: str
    :return: list
    """
    doc = PROV_TRENDS_COLL.find_one({PROVINCE_KEY: province})
    return doc["trends"]


def get_regional_breakdown():
    """Return regional breakdown from DB"""
    return REG_BREAKDOWN_COLL.find_one({}, {"_id": False})


def get_provincial_breakdown(region):
    """Return provincial breakdown from DB"""
    return PROV_BREAKDOWN_COLL.find_one(
        {REGION_KEY: region}, {"_id": False})["breakdowns"]


def get_national_series():
    """Return national series from DB"""
    series = NAT_SERIES_COLL.find_one({}, {"_id": False})
    return translate_series_lang(series)


def get_regional_series(region):
    """Return regional series from DB"""
    series = REG_SERIES_COLL.find_one({REGION_KEY: region}, {"_id": False})
    return translate_series_lang(series)


def get_provincial_series(province):
    """Return provincial series from DB"""
    series = PROV_SERIES_COLL.find_one(
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
    query_menu = get_query_menu(area)
    query = query_menu[area_type]["query"]
    collection = query_menu[area_type]["collection"]
    doc = next(collection.find(query).sort([(DATE_KEY, -1)]).limit(1))
    return f"{round(doc[DAILY_POSITIVITY_INDEX])}%"


def get_national_data():
    """Return a data frame of the national data from DB"""
    cursor = NAT_DATA_COLL.find({})
    return pd.DataFrame(list(cursor))


def get_region_data(region):
    """Return a data frame for a given region from the regional collection"""
    cursor = REG_DATA_COLL.find({REGION_KEY: region})
    return pd.DataFrame(list(cursor))


def get_province_data(province):
    """
    Return a data frame for a given province from the provincial collection
    """
    cursor = PROV_DATA_COLL.find({PROVINCE_KEY: province})
    return pd.DataFrame(list(cursor))


def get_latest_update(data_type="national"):
    """
    Return the value of the key PCM_DATE_KEY of the last dict in data
    :return: str
    """
    app.logger.debug("Getting latest update")
    query_menu = get_query_menu()
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
