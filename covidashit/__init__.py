import datetime as dt
from flask import Flask, abort
import requests

URL_NATIONAL_DATA = (
    "https://raw.githubusercontent.com"
    "/pcm-dpc/COVID-19/master/dati-json/"
    "dpc-covid19-ita-andamento-nazionale.json"
)
URL_REGIONAL_DATA = (
    "https://raw.githubusercontent.com/"
    "pcm-dpc/COVID-19/master/dati-json/"
    "dpc-covid19-ita-regioni.json"
)
DATE_FMT = "%Y-%m-%dT%H:%M:%S"
REGION_KEY = "denominazione_regione"
MAIN_TYPES = [
    "terapia_intensiva", "isolamento_domiciliare",
    "nuovi_attualmente_positivi", "ricoverati_con_sintomi"
]
ITEN_MAP = {
    "ricoverati_con_sintomi": "Hospitalized with symptoms",
    "terapia_intensiva": "Intensive Care Unit",
    "totale_ospedalizzati": "Hospitalized",
    "isolamento_domiciliare": "Self Isolation",
    "totale_attualmente_positivi": "Currently positive",
    "nuovi_attualmente_positivi": "New currently positive",
    "dimessi_guariti": "Healed",
    "deceduti": "Dead",
    "totale_casi": "Tot cases",
    "tamponi": "Swabs"
}


def get_trend(data, region=None):
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
    regions = sorted(
        list(set(r[REGION_KEY] for r in regional_data))
    )
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
        if region not in regions:
            abort(404)
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
    series1 = {"name": "Intensive Care Unit", "data": intensive_care, "visible": "true"}
    series2 = {"name": "Hospitalized with symptoms", "data": hospitalized_w_symptoms}
    series3 = {"name": "Dead", "data": tot_dead}
    series4 = {"name": "Healed", "data": healed}
    series5 = {"name": "Hospitalized", "data": tot_hospitalized}
    series6 = {"name": "Self Isolation", "data": isolated}
    series7 = {"name": "Currently positive", "data": tot_curr_pos}
    series8 = {"name": "New currently positive", "data": new_curr_pos}
    series9 = {"name": "Swabs", "data": tot_swabs}
    series10 = {"name": "Tot cases", "data": total_cases}
    series = [
        series1, series2, series3, series4, series5,
        series6, series7, series8, series9, series10
    ]
    return dates, series, trend, regions


app = Flask(__name__)

from covidashit import routes
