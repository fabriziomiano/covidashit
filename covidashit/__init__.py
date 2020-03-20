from flask import Flask
import requests
import datetime as dt


TODAY = dt.datetime.strftime(dt.datetime.now(), "%Y%m%d")

url = (
    "https://raw.githubusercontent.com"
    "/pcm-dpc/COVID-19/master/dati-json/"
    "dpc-covid19-ita-andamento-nazionale.json"
)
data = requests.get(url).json()
dates = []
intensive_care = []
hospitalized_w_symptoms = []
total_cases = []
healed = []
for d in data:
    date_str = d["data"]
    dates.append(date_str)
    intensive_care.append(d["terapia_intensiva"])
    hospitalized_w_symptoms.append(d["ricoverati_con_sintomi"])
    total_cases.append(d["deceduti"])
    healed.append(d["dimessi_guariti"])
series1 = {"name": "Intensive Care", "data": intensive_care}
series2 = {"name": "Hospitalized with symptoms", "data": hospitalized_w_symptoms}
series3 = {"name": "Dead", "data": total_cases}
series4 = {"name": "Healed", "data": healed}


app = Flask(__name__)

from covidashit import routes