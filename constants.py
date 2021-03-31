"""
General configuration file
"""
import datetime as dt
import os
from collections import OrderedDict

from flask_babel import gettext

VERSION = "4.8"
PAGE_BASE_TITLE = gettext("COVID-19 Italy")
HOSPITALIZED_WITH_SYMPTOMS_KEY = "ricoverati_con_sintomi"
ICU_KEY = "terapia_intensiva"
DAILY_ICU_KEY = "ingressi_terapia_intensiva"
DAILY_ICU_MA_KEY = "ingressi_terapia_intensiva_ma"
TOTAL_HOSPITALIZED_KEY = "totale_ospedalizzati"
DAILY_HOSPITALIZED_KEY = "totale_ospedalizzati_g"
DAILY_HOSPITALIZED_MA_KEY = "totale_ospedalizzati_g_ma"
SELF_ISOLATION_KEY = "isolamento_domiciliare"
TOTAL_POSITIVE_KEY = "totale_positivi"
NEW_POSITIVE_KEY = "nuovi_positivi"
NEW_POSITIVE_MA_KEY = "nuovi_positivi_ma"
TOTAL_HEALED_KEY = "dimessi_guariti"
TOTAL_DEATHS_KEY = "deceduti"
DAILY_DEATHS_KEY = "deceduti_g"
DAILY_DEATHS_MA_KEY = "deceduti_g_ma"
TOTAL_CASES_KEY = "totale_casi"
TOTAL_SWABS_KEY = "tamponi"
DAILY_SWABS_KEY = "tamponi_g"
DAILY_SWABS_MA_KEY = "tamponi_g_ma"
DAILY_POSITIVITY_INDEX = "indice_positivita"
REGION_KEY = "denominazione_regione"
PROVINCE_KEY = "denominazione_provincia"
REGION_CODE = "codice_regione"
PROVINCE_CODE = "codice_provincia"
VAX_LATEST_UPDATE_KEY = "ultimo_aggiornamento"
CP_DATE_FMT = "%Y-%m-%dT%H:%M:%S"
VAX_DATE_FMT = "%Y-%m-%dT%H:%M:%S.%f%z"
CHART_DATE_FMT = "%d %b '%y"
UPDATE_FMT = "%d/%m/%Y"
VAX_UPDATE_FMT = "%d/%m/%Y %H:%M"
DATE_KEY = "data"
NOTE_KEY = "note"
STATE_KEY = "stato"
VAX_DATE_KEY = "data_somministrazione"
VAX_AREA_KEY = "area"
VAX_TYPE_KEY = "fornitore"
VAX_AGE_KEY = "fascia_anagrafica"
POP_KEY = "popolazione"
ADMINS_DOSES_KEY = "dosi_somministrate"
DELIVERED_DOSES_KEY = "dosi_consegnate"
VAX_ADMINS_PERC_KEY = "percentuale_somministrazione"
VAX_TOT_ADMINS_KEY = "totale"
VAX_FIRST_DOSE_KEY = "prima_dose"
VAX_SECOND_DOSE_KEY = "seconda_dose"
VAX_PROVIDER_KEY = "fornitore"
F_SEX_KEY = "sesso_femminile"
M_SEX_KEY = "sesso_maschile"
HEALTHCARE_PERS_KEY = "categoria_operatori_sanitari_sociosanitari"
NONHEALTHCARE_PERS_KEY = "categoria_personale_non_sanitario"
HFE_GUESTS_KEY = "categoria_ospiti_rsa"
OVER_80_KEY = "categoria_over80"
OTHER_KEY = "categoria_altro"
ARMED_FORCES_KEY = "categoria_forze_armate"
SCHOOL_PERS_KEY = "categoria_personale_scolastico"
RUBBISH_NOTE_REGEX = r"[a-z][a-z]-[A-Z]\w+-[0-9][0-9][0-9][0-9]"
TRANSLATION_DIRNAME = "translations"
TREND_SYMBOL_LOGIC = {
    "stable": {
        "colour": "text-info",
        "icon": "bi bi-dash",
        "tooltip": gettext("Stable with respect to yesterday")
    },
    "increase": {
        "colour": "text-danger",
        "icon": "bi bi-arrow-up-right",
        "tooltip": gettext("Increased with respect to yesterday")
    },
    "increase_inverted": {
        "colour": "text-success",
        "icon": "bi bi-arrow-up-right",
        "tooltip": gettext("Increased with respect to yesterday")
    },
    "decrease": {
        "colour": "text-success",
        "icon": "bi bi-arrow-down-left",
        "tooltip": gettext("Decreased with respect to yesterday")
    },
    "decrease_inverted": {
        "colour": "text-danger",
        "icon": "bi bi-arrow-down-left",
        "tooltip": gettext("Decreased with respect to yesterday")
    }
}
VARS = OrderedDict()

# Daily variables
VARS[NEW_POSITIVE_KEY] = {
    "title": gettext("New Positive"),
    "desc": gettext("Daily count of new positive cases"),
    "longdesc": gettext("Daily count of new positive cases"),
    "icon": "fas fa-head-side-cough",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily"
}
VARS[DAILY_ICU_KEY] = {
    "title": gettext("Daily ICU"),
    "desc": gettext("# of people daily admitted in ICU"),
    "longdesc": gettext("Daily count of people in ICU"),
    "icon": "fas fa-procedures",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily"
}
VARS[DAILY_DEATHS_KEY] = {
    "title": gettext("Daily Deaths"),
    "desc": gettext("Daily deaths count"),
    "longdesc": gettext(
        "Daily deaths count"
    ),
    "icon": "fas fa-cross",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily"
}
VARS[DAILY_SWABS_KEY] = {
    "title": gettext("Daily Swabs"),
    "desc": gettext("# of swabs performed daily"),
    "longdesc": gettext(
        "Daily number of swabs performed"
    ),
    "icon": "fas fa-vial",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily"
}
VARS[DAILY_HOSPITALIZED_KEY] = {
    "title": gettext("Daily Hospitalized"),
    "desc": gettext("# of people daily hospitalized"),
    "longdesc": gettext(
        "Daily count of people currently hospitalized. "
        "It takes into account ICU"),
    "icon": "fas fa-hospital-symbol",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily"
}
VARS[NEW_POSITIVE_MA_KEY] = {
    "title": gettext("New Positive (7-day MA)"),
    "desc": gettext("Daily count of new positve cases"),
    "longdesc": gettext("Daily count of new positve cases"),
    "icon": "fas fa-head-side-cough",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily"
}
VARS[DAILY_DEATHS_MA_KEY] = {
    "title": gettext("Daily Deaths (7-day MA)"),
    "desc": gettext("Daily deaths count"),
    "longdesc": gettext(
        "Daily deaths count"
    ),
    "icon": "fas fa-cross",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily"
}
VARS[DAILY_ICU_MA_KEY] = {
    "title": gettext("Daily ICU (7-day MA)"),
    "desc": gettext("# of people daily admitted in ICU"),
    "longdesc": gettext("Daily count of people in ICU"),
    "icon": "fas fa-procedures",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily"
}
VARS[DAILY_SWABS_MA_KEY] = {
    "title": gettext("Daily Swabs (7-day MA)"),
    "desc": gettext("# of swabs performed daily"),
    "longdesc": gettext(
        "Daily number of swabs performed"
    ),
    "icon": "fas fa-vial",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily"
}
VARS[DAILY_HOSPITALIZED_MA_KEY] = {
    "title": gettext("Daily Hospitalized (7-day MA)"),
    "desc": gettext("# of people daily hospitalized"),
    "longdesc": gettext(
        "Daily count of people currently hospitalized. "
        "It takes into account ICU"),
    "icon": "fas fa-hospital-symbol",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily"
}

# Current-state variables
VARS[TOTAL_POSITIVE_KEY] = {
    "title": gettext("Total Positive"),
    "desc": gettext(
        "# of people currently "
        "hospitalized with symptoms + ICU + self isolation"
    ),
    "longdesc": gettext(
        "People currently positive. "
        "Unlike 'Total Cases' it does not take into account "
        "'healed' and 'deaths'. By the end of the outbreak "
        "this should tend to zero. In particular, it is: "
        "total positive = total cases - total healed - total deaths"
    ),
    "icon": "fas fa-viruses",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "current"
}
VARS[ICU_KEY] = {
    "title": gettext("Intensive Care Unit"),
    "desc": gettext("# of people currently in ICU"),
    "longdesc": gettext(
        "Total count of people currently in ICU and positive to COVID-19"
    ),
    "icon": "fas fa-procedures",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "current"
}
VARS[HOSPITALIZED_WITH_SYMPTOMS_KEY] = {
    "title": gettext("Hospitalized With Symptoms"),
    "desc": gettext(
        "# of people currently hospitalized with symptoms"
    ),
    "longdesc": gettext(
        "Total count of people currently in hospital "
        "due to coronavirus with symptoms"
    ),
    "icon": "fas fa-hospital-symbol",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "current"
}

VARS[TOTAL_HOSPITALIZED_KEY] = {
    "title": gettext("Total Hospitalized"),
    "desc": gettext("# of people currently hospitalized"),
    "longdesc": gettext(
        "Total count of people currently hospitalized. "
        "It takes into account ICU"),
    "icon": "fas fa-hospital-symbol",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "current"
}
VARS[SELF_ISOLATION_KEY] = {
    "title": gettext("Self Isolation"),
    "desc": gettext("# of people currently in self isolation"),
    "longdesc": gettext(
        "People currently positive but who do not need hospitalization"
    ),
    "icon": "fas fa-house-user",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "current"
}

# Cumulative variables
VARS[TOTAL_CASES_KEY] = {
    "title": gettext("Total Cases"),
    "desc": gettext(
        "Total count of the positive tests since the"
        " beginning of the outbreak"
    ),
    "longdesc": gettext(
        "Total count of the positive tests since the"
        " beginning of the outbreak"
    ),
    "icon": "fas fa-viruses",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "cum"
}
VARS[TOTAL_DEATHS_KEY] = {
    "title": gettext("Total Deaths"),
    "desc": gettext("Total deaths count"),
    "longdesc": gettext(
        "Total deaths count since the beginning of the outbreak"
    ),
    "icon": "fas fa-cross",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "cum"
}

VARS[TOTAL_SWABS_KEY] = {
    "title": gettext("Total Swabs"),
    "desc": gettext("# of swabs performed"),
    "longdesc": gettext(
        "Total number of swabs performed since the beginning of the outbreak"
    ),
    "icon": "fas fa-vial",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "cum"
}
VARS[TOTAL_HEALED_KEY] = {
    "title": gettext("Total Healed"),
    "desc": gettext("Cumulative # of people healed"),
    "longdesc": gettext(
        "Total number of people healed since the beginning of the outbreak"
    ),
    "icon": "fas fa-smile",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "cum"
}

# Vax variables
VARS[HEALTHCARE_PERS_KEY] = {
    "title": gettext("Healthcare Personnel"),
    "type": "vax"
}
VARS[NONHEALTHCARE_PERS_KEY] = {
    "title": gettext("Non-healthcare Personnel"),
    "type": "vax"
}
VARS[HFE_GUESTS_KEY] = {
    "title": gettext("HFE Guests"),
    "type": "vax"
}
VARS[OVER_80_KEY] = {
    "title": gettext("Over 80"),
    "type": "vax"
}
VARS[OTHER_KEY] = {
    "title": gettext("Other"),
    "type": "vax"
}
VARS[ARMED_FORCES_KEY] = {
    "title": gettext("Armed Forces"),
    "type": "vax"
}
VARS[SCHOOL_PERS_KEY] = {
    "title": gettext("School personnel"),
    "type": "vax"
}
VARS[VAX_FIRST_DOSE_KEY] = {
    "title": gettext("Daily First administrations"),
    "icon": "fas fa-check",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "vax"
}
VARS[VAX_SECOND_DOSE_KEY] = {
    "title": gettext("Daily Second administrations"),
    "icon": "fas fa-check-double",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "vax"
}

# Data URLs: Pandemic
BASE_URL_DATA = (
    "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/"
)
NATIONAL_DATA_FILE = (
    "dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
REGIONAL_DATA_FILE = "dati-regioni/dpc-covid19-ita-regioni.csv"
PROVINCIAL_DATE_FILE = "dati-province/dpc-covid19-ita-province.csv"

URL_NATIONAL = os.path.join(BASE_URL_DATA, NATIONAL_DATA_FILE)
URL_REGIONAL = os.path.join(BASE_URL_DATA, REGIONAL_DATA_FILE)
URL_PROVINCIAL = os.path.join(BASE_URL_DATA, PROVINCIAL_DATE_FILE)

# Data URLs: Vaccines
BASE_URL_VAX_DATA = (
    "https://raw.githubusercontent.com/"
    "italia/covid19-opendata-vaccini/master/dati/"
)
VAX_FILE = "somministrazioni-vaccini-latest.csv"
VAX_ADMINS_SUMMARY_FILE = "somministrazioni-vaccini-summary-latest.csv"
VAX_SUMMARY_FILE = "vaccini-summary-latest.csv"
VAX_LATEST_UPDATE_JSON = "last-update-dataset.json"
URL_VAX_DATA = os.path.join(BASE_URL_VAX_DATA, VAX_FILE)
URL_VAX_LATEST_UPDATE = os.path.join(BASE_URL_VAX_DATA, VAX_LATEST_UPDATE_JSON)
URL_VAX_SUMMARY_DATA = os.path.join(BASE_URL_VAX_DATA, VAX_SUMMARY_FILE)
URL_VAX_ADMINS_SUMMARY_DATA = os.path.join(
    BASE_URL_VAX_DATA, VAX_ADMINS_SUMMARY_FILE)
# Key Dates
LOCKDOWN_DAY = dt.datetime(2020, 3, 22)
PHASE2_DAY = dt.datetime(2020, 5, 4)
PHASE3_DAY = dt.datetime(2020, 6, 15)
CRITICAL_AREAS_DAY = dt.datetime(2020, 11, 6)
VACCINE_DAY = dt.datetime(2020, 12, 27)

# Key Periods
KEY_PERIODS = OrderedDict()
KEY_PERIODS["lockdown"] = {
    "title": gettext("Lockdown"),
    "text": gettext('Days in Lockdown'),
    "color": "red",
    "from": LOCKDOWN_DAY,
    "to": PHASE2_DAY,
    "n_days": (PHASE2_DAY - LOCKDOWN_DAY).days
}
KEY_PERIODS["phase2"] = {
    "title": gettext("Phase 2"),
    "text": gettext('Days in "Phase 2"'),
    "color": "orange",
    "from": PHASE2_DAY,
    "to": PHASE3_DAY,
    "n_days": (PHASE3_DAY - PHASE2_DAY).days,
}
KEY_PERIODS["phase3"] = {
    "title": gettext("Phase 3"),
    "text": gettext('Days in "Phase 3"'),
    "color": "green",
    "from": PHASE3_DAY,
    "to": CRITICAL_AREAS_DAY,
    "n_days": (CRITICAL_AREAS_DAY - PHASE3_DAY).days,
}
KEY_PERIODS["critical_areas"] = {
    "title": gettext("Critical Areas"),
    "text": gettext('Days since "Critical areas"'),
    "color": "red",
    "from": CRITICAL_AREAS_DAY,
    "to": dt.datetime.today(),
    "n_days": (dt.datetime.today() - CRITICAL_AREAS_DAY).days
}
KEY_PERIODS["vaccine_day"] = {
    "title": gettext("Vaccine day"),
    "text": gettext('Days since "Vaccine day"'),
    "color": "blue",
    "from": VACCINE_DAY,
    "to": dt.datetime.today(),
    "n_days": (dt.datetime.today() - VACCINE_DAY).days
}

LANGUAGES = {
    "en": "English",
    "it_IT": "Italiano"
}

ITALY_MAP = {
    'Abruzzo': ['Chieti', "L'Aquila", 'Pescara', 'Teramo'],
    'Basilicata': ['Matera', 'Potenza'],
    'Calabria': ['Catanzaro',
                 'Cosenza',
                 'Crotone',
                 'Reggio di Calabria',
                 'Vibo Valentia'],
    'Campania': ['Avellino', 'Benevento', 'Caserta', 'Napoli', 'Salerno'],
    'Emilia-Romagna': ['Bologna',
                       'Ferrara',
                       'Forlì-Cesena',
                       'Modena',
                       'Parma',
                       'Piacenza',
                       'Ravenna',
                       "Reggio nell'Emilia",
                       'Rimini'],
    'Friuli Venezia Giulia': ['Gorizia', 'Pordenone', 'Trieste', 'Udine'],
    'Lazio': ['Frosinone', 'Latina', 'Rieti', 'Roma', 'Viterbo'],
    'Liguria': ['Genova', 'Imperia', 'La Spezia', 'Savona'],
    'Lombardia': ['Bergamo',
                  'Brescia',
                  'Como',
                  'Cremona',
                  'Lecco',
                  'Lodi',
                  'Mantova',
                  'Milano',
                  'Monza e della Brianza',
                  'Pavia',
                  'Sondrio',
                  'Varese'],
    'Marche': ['Ancona', 'Ascoli Piceno', 'Fermo', 'Macerata',
               'Pesaro e Urbino'],
    'Molise': ['Campobasso', 'Isernia'],
    'Piemonte': ['Alessandria',
                 'Asti',
                 'Biella',
                 'Cuneo',
                 'Novara',
                 'Torino',
                 'Verbano-Cusio-Ossola',
                 'Vercelli'],
    'Puglia': ['Bari',
               'Barletta-Andria-Trani',
               'Brindisi',
               'Lecce',
               'Foggia',
               'Taranto'],
    'Sardegna': ['Cagliari',
                 'Nuoro',
                 'Sassari',
                 'Sud Sardegna'],
    'Sicilia': ['Agrigento',
                'Caltanissetta',
                'Catania',
                'Enna',
                'Messina',
                'Palermo',
                'Ragusa',
                'Siracusa',
                'Trapani'],
    'Toscana': ['Arezzo',
                'Firenze',
                'Grosseto',
                'Livorno',
                'Lucca',
                'Massa Carrara',
                'Pisa',
                'Pistoia',
                'Prato',
                'Siena'],
    'P.A. Bolzano': [],
    'P.A. Trento': [],
    'Umbria': ['Perugia', 'Terni'],
    "Valle d'Aosta": ['Aosta'],
    'Veneto': ['Belluno',
               'Padova',
               'Rovigo',
               'Treviso',
               'Venezia',
               'Verona',
               'Vicenza']
}
REGIONS = [key for key in ITALY_MAP]
PROVINCES = [p for pp in ITALY_MAP.values() for p in pp]
ITALY_POPULATION = {
    'Piemonte': 4311217,
    "Valle d'Aosta": 125034,
    'Lombardia': 10027602,
    'P.A. Bolzano': 532250,
    'P.A. Trento': 542214,
    'Veneto': 4879133,
    'Friuli Venezia Giulia': 1206216,
    'Liguria': 1524826,
    'Emilia-Romagna': 4464119,
    'Toscana': 3692555,
    'Umbria': 870165,
    'Marche': 1512672,
    'Lazio': 5755700,
    'Abruzzo': 1293941,
    'Molise': 300516,
    'Campania': 5712143,
    'Puglia': 3953305,
    'Basilicata': 553254,
    'Calabria': 1894110,
    'Sicilia': 4875290,
    'Sardegna': 1611621,
    'Italia': 59641488
}
PC_TO_OD_MAP = {
    'Italia': 'ITA',
    'Abruzzo': 'ABR',
    'Basilicata': 'BAS',
    'Calabria': 'CAL',
    'Campania': 'CAM',
    'Emilia-Romagna': 'EMR',
    'Friuli Venezia Giulia': 'FVG',
    'Lazio': 'LAZ',
    'Liguria': 'LIG',
    'Lombardia': 'LOM',
    'Marche': 'MAR',
    'Molise': 'MOL',
    'P.A. Bolzano': 'PAB',
    'P.A. Trento': 'PAT',
    'Piemonte': 'PIE',
    'Puglia': 'PUG',
    'Sardegna': 'SAR',
    'Sicilia': 'SIC',
    'Toscana': 'TOS',
    'Umbria': 'UMB',
    "Valle d'Aosta": 'VDA',
    'Veneto': 'VEN',
}
OD_TO_PC_MAP = {
    'ITA': 'Italia',
    'ABR': 'Abruzzo',
    'BAS': 'Basilicata',
    'CAL': 'Calabria',
    'CAM': 'Campania',
    'EMR': 'Emilia-Romagna',
    'FVG': 'Friuli Venezia Giulia',
    'LAZ': 'Lazio',
    'LIG': 'Liguria',
    'LOM': 'Lombardia',
    'MAR': 'Marche',
    'MOL': 'Molise',
    'PAB': 'P.A. Bolzano',
    'PAT': 'P.A. Trento',
    'PIE': 'Piemonte',
    'PUG': 'Puglia',
    'SAR': 'Sardegna',
    'SIC': 'Sicilia',
    'TOS': 'Toscana',
    'UMB': 'Umbria',
    'VDA': "Valle d'Aosta",
    'VEN': 'Veneto'
}
