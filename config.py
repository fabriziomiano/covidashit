import os
import datetime as dt
from flask_babel import gettext

NATIONAL_DATA_FILE = "dpc-covid19-ita-andamento-nazionale.json"
REGIONAL_DATA_FILE = "dpc-covid19-ita-regioni.json"
PROVINCIAL_DATE_FILE = "dpc-covid19-ita-province.json"
BASE_URL_DATA = (
    "https://raw.githubusercontent.com"
    "/pcm-dpc/COVID-19/master/dati-json/"
)
URL_NATIONAL_DATA = os.path.join(BASE_URL_DATA, NATIONAL_DATA_FILE)
URL_REGIONAL_DATA = os.path.join(BASE_URL_DATA, REGIONAL_DATA_FILE)
URL_PROVINCIAL_DATA = os.path.join(BASE_URL_DATA, PROVINCIAL_DATE_FILE)
ITEN_MAP = {
    "ricoverati_con_sintomi": {
        "title": gettext("Hospitalized with symptoms"),
        "desc": gettext("# of People currently in hospital with symptoms"),
        "longdesc": gettext(
            "Total count of people currently in hospital with symptoms")
    },
    "terapia_intensiva": {
        "title": gettext("Intensive Care Unit"),
        "desc": gettext("# of people in ICU"),
        "longdesc": gettext(
            "Total count of people currently in ICU  and positive to COVID-19"
        )
    },
    "totale_ospedalizzati": {
        "title": gettext("Total Hospitalized"),
        "desc": gettext("# of people hospitalized (today)"),
        "longdesc": gettext(
            "Total count of people currently hospitalized. "
            "It takes into account ICU")
    },
    "isolamento_domiciliare": {
        "title": gettext("Self Isolation"),
        "desc": "",
        "longdesc": ""
    },
    "totale_positivi": {
        "title": gettext("Total positive"),
        "desc": gettext("Hospitalized with symptoms + ICU + Self Isolation"),
        "longdesc": gettext(
            "People currently positive. "
            "Unlike 'Total Cases' it does not take into account "
            "'healed' and 'deaths'. By the end of the outbreak "
            "this should tend to zero. In particular, it is "
            "total positive = total cases - total healed - total deaths"
        )
    },
    "variazione_totale_positivi": {
        "title": gettext("Total positive variation"),
        "desc": gettext("Tot Positive (Today) - Tot Positive (Yesterday)"),
        "longdesc": gettext(
            "Variation of the number of people currently positive "
            "with respect to the previous day. It is negative when the number "
            "of daily healed and deaths is larger than 'New positive'"
        )
    },
    "nuovi_positivi": {
        "title": gettext("New positive"),
        "desc": gettext("Tot Cases (Today) - Tot cases (Yesterday)"),
        "longdesc": gettext("Daily count of new positve cases")
    },
    "dimessi_guariti": {
        "title": gettext("Total Healed"),
        "desc": "",
        "longdesc": ""
    },
    "deceduti": {
        "title": gettext("Total Deaths"),
        "desc": "",
        "longdesc": ""
    },
    "totale_casi": {
        "title": gettext("Total cases"),
        "desc": gettext("Self isolation + Tot Hospitalized + Tot Healed + Tot Deaths"),
        "longdesc": gettext(
            "Total count of the positive tests since the beginning of the outbreak"
        )
    },
    "tamponi": {
        "title": gettext("Total Swabs"),
        "desc": "",
        "longdesc": ""
    }
}
CARD_TYPES = [
    "totale_casi", "nuovi_positivi",
    "totale_positivi", "variazione_totale_positivi",
    "terapia_intensiva", "totale_ospedalizzati"
]
REGION_KEY = "denominazione_regione"
PROVINCE_KEY = "denominazione_provincia"
PROVINCES_TOAVOID = ["In fase di definizione/aggiornamento"]
DATE_FMT = "%Y-%m-%dT%H:%M:%S"
WEBSITE_TITLE = gettext("Italian COVID Tracker")
PCM_DATE_KEY = "data"
LOCKDOWN_DAY = dt.datetime(2020, 3, 9)
LANGUAGES = {
    "en": "English",
    "it_IT": "Italiano"
}
