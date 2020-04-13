import datetime as dt
import json

from flask_babel import gettext

from config import (
    REGION_KEY, CARD_TYPES, ITEN_MAP, PCM_DATE_FMT, PROVINCE_KEY,
    CHART_DATE_FMT, PCM_DATE_KEY, UPDATE_FMT, PROVINCES, REGIONS
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
SCATTER_DATA = []


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


def get_trend(data, province=False):
    """
    Return a list of dicts of the daily trend wrt to the previous day
    :param data: ascending sorted list of daily dicts
    :param province: bool
    :return: list of dicts
    """
    if not province:
        main_types = CARD_TYPES
    else:
        main_types = ["totale_casi"]
    last = data[-1]
    penultimate = data[-2]
    trend = []
    for key in main_types:
        if penultimate[key] > last[key]:
            status = "happy"
        elif penultimate[key] == last[key]:
            status = "neutral"
        else:
            status = "sad"
        trend.append({
            "title": ITEN_MAP[key]["title"],
            "desc": ITEN_MAP[key]["desc"],
            "longdesc": ITEN_MAP[key]["longdesc"],
            "count": last[key],
            "status": status
        })
    return trend


def fill_series(province=False):
    """
    Return the series array to be used in the chart
    :return: list
    """
    if not province:
        series1 = {
            "name": gettext(ITEN_MAP["nuovi_positivi"]["title"]),
            "data": NEW_POS,
            "visible": "true"
        }
        series2 = {
            "name": gettext(ITEN_MAP["variazione_totale_positivi"]["title"]),
            "data": TOT_POS_VAR,
            "visible": "true"
        }
        series3 = {
            "name": gettext(ITEN_MAP["terapia_intensiva"]["title"]),
            "data": ICU,
            "visible": "true"
        }
        series4 = {
            "name": gettext(ITEN_MAP["deceduti"]["title"]),
            "data": TOT_DEATHS
        }
        series5 = {
            "name": gettext(ITEN_MAP["dimessi_guariti"]["title"]),
            "data": HEALED
        }
        series6 = {
            "name": gettext(ITEN_MAP["ricoverati_con_sintomi"]["title"]),
            "data": HOSP_W_SYMPTS
        }
        series7 = {
            "name": gettext(ITEN_MAP["totale_ospedalizzati"]["title"]),
            "data": TOT_HOSP
        }
        series8 = {
            "name": gettext(ITEN_MAP["isolamento_domiciliare"]["title"]),
            "data": SELF_ISOL
        }
        series9 = {
            "name": gettext(ITEN_MAP["totale_positivi"]["title"]),
            "data": TOT_POS
        }
        series10 = {
            "name": gettext(ITEN_MAP["totale_casi"]["title"]),
            "data": TOT_CASES
        }
        series11 = {
            "name": gettext(ITEN_MAP["tamponi"]["title"]),
            "data": TOT_SWABS
        }
        series = [
            series1, series2, series3, series4, series5,
            series6, series7, series8, series9, series10,
            series11
        ]
    else:
        series = [{
            "name": gettext(ITEN_MAP["totale_casi"]["title"]),
            "data": TOT_CASES,
            "visible": "true"
        }]
    return series


def parse_data(data, territory=None):
    """
    Return dates, series, trend
    :param data: dict
    :param territory: str
    :return:
        DATES: list,
        series: list,
        trend: list
    """
    series = []
    trend = []
    if territory is None:
        national_data = data["national"]
        trend = get_trend(national_data)
        for d in national_data:
            fill_data(d)
        series = fill_series()
    else:
        if territory in PROVINCES:
            provincial_data = data["provincial"]
            subset = [r for r in provincial_data if r[PROVINCE_KEY] == territory]
            trend = get_trend(subset, province=True)
            for d in provincial_data:
                if territory == d[PROVINCE_KEY]:
                    fill_data(d, province=True)
            series = fill_series(province=True)
        elif territory in REGIONS:
            regional_data = data["regional"]
            subset = [r for r in regional_data if r[REGION_KEY] == territory]
            trend = get_trend(subset)
            for d in regional_data:
                if territory == d[REGION_KEY]:
                    fill_data(d)
            series = fill_series()
    return DATES, series, trend


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
        SCATTER_DATA.append([datum["totale_positivi"], datum["nuovi_positivi"]])
    date_dt = dt.datetime.strptime(datum["data"], PCM_DATE_FMT)
    date_str = date_dt.strftime(CHART_DATE_FMT)
    DATES.append(date_str)
    TOT_CASES.append(datum["totale_casi"])


def init_data():
    """
    Empty data series lists
    :return: None
    """
    DATES.clear()
    ICU.clear()
    HOSP_W_SYMPTS.clear()
    TOT_DEATHS.clear()
    TOT_HOSP.clear()
    SELF_ISOL.clear()
    TOT_POS.clear()
    NEW_POS.clear()
    TOT_SWABS.clear()
    HEALED.clear()
    TOT_CASES.clear()
    TOT_POS_VAR.clear()
    SCATTER_DATA.clear()


def init_chart(dates):
    """
    Return chart, x_axis, y_axis dicts to be served to the frontend
    :param dates: list
    :return:
        x_axis: dict,
        y_axis:  dict
    """
    x_axis = {"categories": dates}
    y_axis = {"title": {"text": gettext('# of people')}}
    return x_axis, y_axis


def latest_update(data):
    """
    Return the value of the key PCM_DATE_KEY of the last dict in data
    :param data: list
    :return: str
    """
    date_dt = dt.datetime.strptime(data[-1][PCM_DATE_KEY], PCM_DATE_FMT)
    return date_dt.strftime(UPDATE_FMT)
