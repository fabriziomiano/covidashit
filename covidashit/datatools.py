import datetime as dt
import json
import os
import time

import bar_chart_race as bcr
import pandas as pd
import requests
from flask import current_app
from flask_babel import gettext

from config import (
    CUSTOM_CARDS, CARD_MAP, CARD_TYPES, ITEN_MAP, PROVINCES, PROVINCE_KEY,
    REGIONS, REGION_KEY, PCM_DATE_FMT, CHART_DATE_FMT, PCM_DATE_KEY,
    UPDATE_FMT, URL_NATIONAL_DATA, NATIONAL_DATA_FILE, URL_REGIONAL_DATA,
    REGIONAL_DATA_FILE, URL_PROVINCIAL_DATA, PROVINCIAL_DATE_FILE,
    DATA_TO_FRONTEND, BARCHART_RACE_VARS
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
            "title": ITEN_MAP[key]["title"],
            "desc": ITEN_MAP[key]["desc"],
            "longdesc": ITEN_MAP[key]["longdesc"],
            "count": stats["count"],
            "colour": ITEN_MAP[key][stats["status"]]["colour"],
            "icon": ITEN_MAP[key]["icon"],
            "status_icon": ITEN_MAP[key][stats["status"]]["icon"],
            "tooltip": ITEN_MAP[key][stats["status"]]["tooltip"]
        })
    return trend_cards


def fill_series(province=False):
    """
    Return the series array to be used in the chart
    :return: list
    """
    if not province:
        series1 = {
            "name": gettext(ITEN_MAP["nuovi_positivi"]["title"]),
            "data": NEW_POS
        }
        series2 = {
            "name": gettext(ITEN_MAP["variazione_totale_positivi"]["title"]),
            "data": TOT_POS_VAR
        }
        series3 = {
            "name": gettext(ITEN_MAP["terapia_intensiva"]["title"]),
            "data": ICU
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
            "data": TOT_POS,
            "visible": "true"
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
    Return dates, series, trend_cards
    :param data: dict
    :param territory: str
    :return:
        DATES: list,
        series: list,
        trend_cards: list
    """
    series = []
    trend_cards = []
    if territory is None:
        national_data = data["national"]
        trend_cards = get_trends(national_data)
        for d in national_data:
            fill_data(d)
        series = fill_series()
    else:
        if territory in PROVINCES:
            provincial_data = data["provincial"]
            subset = [r for r in provincial_data if r[PROVINCE_KEY] == territory]
            trend_cards = get_trends(subset, province=True)
            for d in provincial_data:
                if territory == d[PROVINCE_KEY]:
                    fill_data(d, province=True)
            series = fill_series(province=True)
        elif territory in REGIONS:
            regional_data = data["regional"]
            subset = [r for r in regional_data if r[REGION_KEY] == territory]
            trend_cards = get_trends(subset)
            for d in regional_data:
                if territory == d[REGION_KEY]:
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
        response = requests.get(URL_NATIONAL_DATA, timeout=5)
        status = response.status_code
        if status == 200:
            national_data = response.json()
            data["national"] = sorted(national_data, key=lambda x: x[PCM_DATE_KEY])
            cache_data(data["national"], NATIONAL_DATA_FILE)
        else:
            current_app.logger.error("Could not get data: ERROR {}".format(status))
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
        response = requests.get(URL_REGIONAL_DATA, timeout=5)
        status = response.status_code
        if status == 200:
            regional_data = response.json()
            data["regional"] = sorted(regional_data, key=lambda x: x[PCM_DATE_KEY])
            cache_data(data["regional"], REGIONAL_DATA_FILE)
        else:
            current_app.logger.error("Could not get data: ERROR {}".format(status))
            data["regional"] = read_cached_data(REGIONAL_DATA_FILE)
    except Exception as e:
        current_app.logger.error("Request Error {}".format(e))
        data["regional"] = read_cached_data(REGIONAL_DATA_FILE)
    return data


def get_provincial_data():
    """
    Return the provincial data from the "Protezione Civile" repository
    :return: dict
    """
    data = {}
    try:
        response = requests.get(URL_PROVINCIAL_DATA, timeout=5)
        status = response.status_code
        if status == 200:
            prov_data = response.json()
            data["provincial"] = sorted(prov_data, key=lambda x: x[PCM_DATE_KEY])
            cache_data(data["provincial"], PROVINCIAL_DATE_FILE)
        else:
            current_app.logger.error("Could not get data: ERROR {}".format(status))
            data["provincial"] = read_cached_data(PROVINCIAL_DATE_FILE)
    except Exception as e:
        current_app.logger.error("Request Error {}".format(e))
        data["provincial"] = read_cached_data(PROVINCIAL_DATE_FILE)
    return data


def populate_data_to_frontend(
        dates,
        trend_cards,
        series,
        updated_at,
        data_series,
        territory=None
):
    """
    Return a data dict to be rendered which is an augmented copy of
    DATA_TO_FRONTEND defined in config.py
    :param dates: list
    :param trend_cards: list
    :param series: list
    :param territory: str
    :param updated_at: str
    :param data_series: list
    :return: dict
    """
    data = {
        "dates": dates,
        "trend_cards": trend_cards,
        "series": series,
        "ts": str(time.time()),
        "latest_update": updated_at,
        "data_series": data_series,
        "territory": territory,
        "navtitle": territory,
        "scatterplot_series": {
            "name": gettext("New Positive VS Total Cases"),
            "data": EXP_STATUS
        }
    }
    data.update(DATA_TO_FRONTEND)
    return data


def barchartrace_to_html():
    """
    Generate HTML files of the bar-chart races of all the relevant
    variables defined in the config
    :return: None
    """
    data = get_regional_data()["regional"]
    dates = sorted(set([d["data"] for d in data]))
    dates = [
        dt.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S").strftime("%d %b")
        for d in dates
    ]
    for var in BARCHART_RACE_VARS:
        new_data = {}
        print("Doing {}".format(var))
        for d in data:
            region = d["denominazione_regione"]
            if region not in new_data:
                new_data[region] = [d[var]]
            else:
                new_data[region].append(d[var])
        df = pd.DataFrame.from_dict(new_data, orient='index', columns=dates)
        df = df.transpose()
        bcr_html = bcr.bar_chart_race(
            df=df,
            title=ITEN_MAP[var]["title"],
            period_summary_func=lambda v, r: {
                'x': .99, 'y': .18,
                's': f'Tot: {v.nlargest(6).sum():,.0f}',
                'ha': 'right', 'size': 8
            },
            period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'}
        )
        str_to_replace = '<video width="988" height="504"'
        str_replacement = '<video width="100%" height="auto"'
        bcr_html = bcr_html.replace(str_to_replace, str_replacement)
        filename = "{}.html".format(var)
        file_rel_path = (
            'covidashit/templates/dashboard/barChartRace/{}'.format(filename)
        )
        file_abs_path = os.path.join(os.getcwd(), file_rel_path)
        with open(file_abs_path, "w") as file_out:
            file_out.write(bcr_html)
        print("Saved {}".format(file_abs_path))
