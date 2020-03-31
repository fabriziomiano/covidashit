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
    "ricoverati_con_sintomi": {
        "title": "Hospitalized with symptoms",
        "desc": ""
    },
    "terapia_intensiva": {
        "title": "Intensive Care Unit",
        "desc": "# of people in ICU"
    },
    "totale_ospedalizzati": {
        "title": "Total Hospitalized",
        "desc": "# of people hospitalized (today)"
    },
    "isolamento_domiciliare": {
        "title": "Self Isolation",
        "desc": ""
    },
    "totale_positivi": {
        "title": "Total positive",
        "desc": "Hospitalized w/ symptoms + ICU + Self Isolation"
    },
    "variazione_totale_positivi": {
        "title": "Total positive variation",
        "desc": "Tot Positive (Today) - Tot Positive (Yesterday)"
    },
    "nuovi_positivi": {
        "title": "New positive",
        "desc": "Tot Cases (Today) - Tot cases (Yesterday)"
    },
    "dimessi_guariti": {
        "title": "Total Healed",
        "desc": ""
    },
    "deceduti": {
        "title": "Total Deaths",
        "desc": ""
    },
    "totale_casi": {
        "title": "Total cases",
        "desc": "Self isolation + Tot Hospitalized + Tot Healed + Tot Deaths"
    },
    "tamponi": {
        "title": "Total Swabs",
        "desc": ""
    }
}
CARD_TYPES = [
    "totale_casi", "nuovi_positivi",
    "totale_positivi", "variazione_totale_positivi",
    "terapia_intensiva", "totale_ospedalizzati"
]
REGION_KEY = "denominazione_regione"
PROVINCE_KEY = "denominazione_provincia"
DATE_FMT = "%Y-%m-%dT%H:%M:%S"
WEBSITE_TITLE = "Italian COVID Tracker"
PCM_DATE_KEY = "data"
LOCKDOWN_DAY = dt.datetime(2020, 3, 9)
