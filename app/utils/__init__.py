"""
Utils
"""
import re
from functools import wraps

from flask import request, current_app as app, jsonify
from flask_babel import gettext

from config import ITALY_MAP, RUBBISH_NOTE_REGEX


def region_of_province(province_in: str) -> str:
    """
    Return the corresponding key in ITALY_MAP whose value contains province_in
    :param province_in: str
    :return: str
    """
    region = None
    for r in ITALY_MAP:
        for p in ITALY_MAP[r]:
            if province_in == p:
                region = r
    return region


def rubbish_notes(notes):
    """
    Return True if note matches the regex, else otherwise
    :param notes: str
    :return: bool
    """
    regex = re.compile(RUBBISH_NOTE_REGEX)
    return regex.search(notes)


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


def apikey_required(view_function):
    """Decorator to secure API"""
    @wraps(view_function)
    def f(*args, **kwargs):
        """API Auth decorator"""
        if (request.headers and
                request.headers.get("x-api-key") is not None and
                request.headers["x-api-key"] == app.config["SECRET_KEY"]):
            return view_function(*args, **kwargs)
        else:
            return jsonify({"errors": "Invalid API Key"})
    return f
