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
    total_cases = []
    healed = []
    for d in data:
        date_dt = dt.datetime.strptime(d["data"], DATE_FMT)
        date_str = date_dt.strftime("%d %b")
        dates.append(date_str)
        intensive_care.append(d["terapia_intensiva"])
        hospitalized_w_symptoms.append(d["ricoverati_con_sintomi"])
        total_cases.append(d["deceduti"])
        healed.append(d["dimessi_guariti"])
    series1 = {"name": "Intensive Care", "data": intensive_care}
    series2 = {"name": "Hospitalized with symptoms", "data": hospitalized_w_symptoms}
    series3 = {"name": "Dead", "data": total_cases}
    series4 = {"name": "Healed", "data": healed}
    return dates, series1, series2, series3, series4


app = Flask(__name__)

from covidashit import routes
