import datetime as dt


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
URL_PROVINCIAL_DATA = (
    "https://raw.githubusercontent.com/"
    "pcm-dpc/COVID-19/master/dati-json/"
    "dpc-covid19-ita-province.json"
)
ITEN_MAP = {
    "ricoverati_con_sintomi": "Hospitalized with symptoms",
    "terapia_intensiva": "Intensive Care Unit",
    "totale_ospedalizzati": "Hospitalized",
    "isolamento_domiciliare": "Self Isolation",
    "totale_positivi": "Total positive",
    "variazione_totale_positivi": "Total positive variation",
    "nuovi_positivi": "New positive",
    "dimessi_guariti": "Total Healed",
    "deceduti": "Total Deaths",
    "totale_casi": "Total cases",
    "tamponi": "Total Swabs"
}
MAIN_TYPES = [
    "nuovi_positivi", "variazione_totale_positivi",
    "terapia_intensiva", "ricoverati_con_sintomi"
]
REGION_KEY = "denominazione_regione"
PROVINCE_KEY = "denominazione_provincia"
DATE_FMT = "%Y-%m-%dT%H:%M:%S"
WEBSITE_TITLE = "Italian COVID Tracker"
PCM_DATE_KEY = "data"
LOCKDOWN_DAY = dt.datetime(2020, 3, 9)
