import requests

URL_NATIONAL_DATA = (
    "https://raw.githubusercontent.com"
    "/pcm-dpc/COVID-19/master/dati-json/"
    "dpc-covid19-ita-andamento-nazionale.json"
)
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
MAIN_TYPES = [
    "terapia_intensiva", "isolamento_domiciliare",
    "nuovi_attualmente_positivi", "ricoverati_con_sintomi"
]
REGION_KEY = "denominazione_regione"
DATE_FMT = "%Y-%m-%dT%H:%M:%S"
URL_REGIONAL_DATA = (
    "https://raw.githubusercontent.com/"
    "pcm-dpc/COVID-19/master/dati-json/"
    "dpc-covid19-ita-regioni.json"
)
REGIONS = sorted(
    list(set(r[REGION_KEY]
             for r in requests.get(URL_REGIONAL_DATA).json()))
)
WEBSITE_TITLE = "COVID-19 Italian Dashboard"