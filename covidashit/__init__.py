import datetime as dt
from flask import Flask
import requests
from config import (
    URL_NATIONAL_DATA, ITEN_MAP, MAIN_TYPES,
    REGION_KEY, DATE_FMT, URL_REGIONAL_DATA
)


def get_trend(data, region=None):
    """
    Return a list of dicts of the daily trend wrt to the previous day
    :param data: list
    :param region: str
    :return: list of dicts
    """
    if region is not None:
        data = [d for d in data if d[REGION_KEY] == region]
    last = data[-1]
    penultimate = data[-2]
    trend = []
    for key in last.keys():
        if key in MAIN_TYPES:
            if penultimate[key] > last[key]:
                status = "happy"
            elif penultimate[key] == last[key]:
                status = "neutral"
            else:
                status = "sad"
            trend.append({
                "name": ITEN_MAP[key],
                "count": last[key],
                "status": status
            })
    return trend


def get_data(region=None):
    """
    Get the data from PC URL and create series to be served
    to populate the highchart
    :return:
        dates:list,
        series1: dict,
        series2: dict,
        series3: dict
    """
    national_data = requests.get(URL_NATIONAL_DATA).json()
    regional_data = requests.get(URL_REGIONAL_DATA).json()
    national_data = sorted(national_data, key=lambda x: x["data"])
    regional_data = sorted(regional_data, key=lambda x: x["data"])
    dates = []
    intensive_care = []
    hospitalized_w_symptoms = []
    tot_dead = []
    tot_hospitalized = []
    isolated = []
    tot_curr_pos = []
    new_curr_pos = []
    tot_swabs = []
    healed = []
    total_cases = []
    if region is None:
        trend = get_trend(national_data)
        for d in national_data:
            date_dt = dt.datetime.strptime(d["data"], DATE_FMT)
            date_str = date_dt.strftime("%d %b")
            dates.append(date_str)
            intensive_care.append(d["terapia_intensiva"])
            hospitalized_w_symptoms.append(d["ricoverati_con_sintomi"])
            tot_dead.append(d["deceduti"])
            healed.append(d["dimessi_guariti"])
            tot_hospitalized.append(d["totale_ospedalizzati"])
            isolated.append(d["isolamento_domiciliare"])
            tot_curr_pos.append(d["totale_attualmente_positivi"])
            new_curr_pos.append(d["nuovi_attualmente_positivi"])
            tot_swabs.append(d["tamponi"])
            total_cases.append(d["totale_casi"])
    else:
        trend = get_trend(regional_data, region)
        for d in regional_data:
            if region == d[REGION_KEY]:
                date_dt = dt.datetime.strptime(d["data"], DATE_FMT)
                date_str = date_dt.strftime("%d %b")
                dates.append(date_str)
                intensive_care.append(d["terapia_intensiva"])
                hospitalized_w_symptoms.append(d["ricoverati_con_sintomi"])
                tot_dead.append(d["deceduti"])
                healed.append(d["dimessi_guariti"])
                tot_hospitalized.append(d["totale_ospedalizzati"])
                isolated.append(d["isolamento_domiciliare"])
                tot_curr_pos.append(d["totale_attualmente_positivi"])
                new_curr_pos.append(d["nuovi_attualmente_positivi"])
                tot_swabs.append(d["tamponi"])
                total_cases.append(d["totale_casi"])
    series1 = {"name": "New currently positive", "data": new_curr_pos, "visible": "true"}
    series2 = {"name": "Intensive Care Unit", "data": intensive_care}
    series3 = {"name": "Currently positive", "data": tot_curr_pos}
    series4 = {"name": "Hospitalized with symptoms", "data": hospitalized_w_symptoms}
    series5 = {"name": "Self Isolation", "data": isolated}
    series6 = {"name": "Total Healed", "data": healed}
    series7 = {"name": "Total Hospitalized", "data": tot_hospitalized}
    series8 = {"name": "Total Deaths", "data": tot_dead}
    series9 = {"name": "Total Cases", "data": total_cases}
    series10 = {"name": "Total Swabs", "data": tot_swabs}
    series = [
        series1, series2, series3, series4, series5,
        series6, series7, series8, series9, series10
    ]
    return dates, series, trend


app = Flask(__name__)

from covidashit import routes
