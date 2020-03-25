import datetime as dt
from flask import Flask
import requests

URL = (
    "https://raw.githubusercontent.com"
    "/pcm-dpc/COVID-19/master/dati-json/"
    "dpc-covid19-ita-andamento-nazionale.json"
)
DATE_FMT = "%Y-%m-%dT%H:%M:%S"
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


def get_trend(data):
    last = data[0]
    penultimate = data[1]
    statuses = []
    for key in last.keys():
        if key in MAIN_TYPES:
            if penultimate[key] > last[key]:
                status = "happy"
            elif penultimate[key] == last[key]:
                status = "neutral"
            else:
                status = "sad"
            statuses.append({
                "name": ITEN_MAP[key],
                "count": last[key],
                "status": status
            })
    return statuses


def get_data():
    """
    Get the data from PC URL and create series to be served
    to populate the highchart
    :return:
        dates:list,
        series1: dict,
        series2: dict,
        series3: dict
    """
    data = requests.get(URL).json()
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
    for d in data:
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
    data = sorted(data, key=lambda x: x["data"], reverse=True)
    return (
        dates, series1, series2, series3, series4, series5,
        series6, series7, series8, series9, series10, get_trend(data)
    )


app = Flask(__name__)

from covidashit import routes
