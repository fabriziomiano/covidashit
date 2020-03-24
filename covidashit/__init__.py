import datetime as dt
from flask import Flask
import requests

URL = (
    "https://raw.githubusercontent.com"
    "/pcm-dpc/COVID-19/master/dati-json/"
    "dpc-covid19-ita-andamento-nazionale.json"
)
DATE_FMT = "%Y-%m-%d %H:%M:%S"


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
    series1 = {"name": "Intensive Care", "data": intensive_care, "visible": "true"}
    series2 = {"name": "Hospitalized with symptoms", "data": hospitalized_w_symptoms}
    series3 = {"name": "Dead", "data": tot_dead}
    series4 = {"name": "Healed", "data": healed}
    series5 = {"name": "Hospitalized", "data": tot_hospitalized}
    series6 = {"name": "Isolation", "data": isolated}
    series7 = {"name": "Currently positive", "data": tot_curr_pos}
    series8 = {"name": "New currently positive", "data": new_curr_pos}
    series9 = {"name": "Swabs", "data": tot_swabs}
    series10 = {"name": "Tot cases", "data": total_cases}
    return (
        dates, series1, series2, series3, series4, series5,
        series6, series7, series8, series9, series10
    )


app = Flask(__name__)

from covidashit import routes
