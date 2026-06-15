"""
Variables settings
"""
from collections import OrderedDict

ICU_KEY = "terapia_intensiva"
DAILY_ICU_KEY = "ingressi_terapia_intensiva"
DAILY_ICU_MA_KEY = "ingressi_terapia_intensiva_ma"
TOTAL_HOSPITALIZED_KEY = "totale_ospedalizzati"
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
POSITIVITY_INDEX = "indice_positivita"
REGION_KEY = "denominazione_regione"
PROVINCE_KEY = "denominazione_provincia"
REGION_CODE = "codice_regione"
OD_REGION_CODE = "ISTAT"
PROVINCE_CODE = "codice_provincia"
NUTS_KEY = "codice_nuts_2"
OD_NUTS1_KEY = "N1"
OD_NUTS2_KEY = "N2"
VAX_LATEST_UPDATE_KEY = "ultimo_aggiornamento"
CP_DATE_FMT = "%Y-%m-%dT%H:%M:%S"
VAX_DATE_FMT = "%Y-%m-%dT%H:%M:%S.%f%z"
CHART_DATE_FMT = "%d %b '%y"
UPDATE_FMT = "%d/%m/%Y"
VAX_UPDATE_FMT = "%d/%m/%Y %H:%M"
DATE_KEY = "data"
NOTE_KEY = "note"
STATE_KEY = "stato"
VAX_DATE_KEY = "data"
VAX_AREA_KEY = "area"
OD_AREA_KEY = "reg"
VAX_AGE_KEY = "eta"
POP_KEY = "popolazione"
OD_POP_KEY = "totale_popolazione"
ADMINS_DOSES_KEY = "dosi_somministrate"
DELIVERED_DOSES_KEY = "dosi_consegnate"
VAX_ADMINS_PERC_KEY = "percentuale_somministrazione"
VAX_TOT_ADMINS_KEY = "totale"
VAX_FIRST_DOSE_KEY = "d1"
VAX_SECOND_DOSE_KEY = "d2"
VAX_BOOSTER1_DOSE_KEY = "db1"
VAX_BOOSTER2_DOSE_KEY = "db2"
VAX_BOOSTER3_DOSE_KEY = "db3"
VAX_PROVIDER_KEY = "forn"
F_SEX_KEY = "f"
M_SEX_KEY = "m"
RUBBISH_NOTE_REGEX = r"[a-z][a-z]-[A-Z]\w+-[0-9][0-9][0-9][0-9]"
TREND_SYMBOL_LOGIC = {
    "stable": {
        "colour": "text-info",
        "icon": "bi bi-dash",
        "tooltip": "Stable with respect to yesterday",
    },
    "increase": {
        "colour": "text-danger",
        "icon": "bi bi-arrow-up-right",
        "tooltip": "Increased with respect to yesterday",
    },
    "increase_inverted": {
        "colour": "text-success",
        "icon": "bi bi-arrow-up-right",
        "tooltip": "Increased with respect to yesterday",
    },
    "decrease": {
        "colour": "text-success",
        "icon": "bi bi-arrow-down-left",
        "tooltip": "Decreased with respect to yesterday",
    },
    "decrease_inverted": {
        "colour": "text-danger",
        "icon": "bi bi-arrow-down-left",
        "tooltip": "Decreased with respect to yesterday",
    },
}
VARS = OrderedDict()
# Daily variables
VARS[NEW_POSITIVE_KEY] = {
    "title": ("New Positive"),
    "desc": ("Daily count of new positive cases"),
    "longdesc": ("Daily count of new positive cases"),
    "icon": "fas fa-head-side-cough",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily",
}
VARS[DAILY_ICU_KEY] = {
    "title": ("Daily ICU"),
    "desc": ("# of people daily admitted in ICU"),
    "longdesc": ("Daily count of people in ICU"),
    "icon": "fas fa-procedures",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily",
}
VARS[DAILY_DEATHS_KEY] = {
    "title": ("Daily Deaths"),
    "desc": ("Daily deaths count"),
    "longdesc": ("Daily deaths count"),
    "icon": "fas fa-cross",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily",
}
VARS[DAILY_SWABS_KEY] = {
    "title": ("Daily Swabs"),
    "desc": ("# of swabs performed daily"),
    "longdesc": ("Daily number of swabs performed"),
    "icon": "fas fa-vial",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily",
}
VARS[NEW_POSITIVE_MA_KEY] = {
    "title": ("New Positive (7-day MA)"),
    "desc": ("Daily count of new positve cases"),
    "longdesc": ("Daily count of new positve cases"),
    "icon": "fas fa-head-side-cough",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily",
}
VARS[DAILY_DEATHS_MA_KEY] = {
    "title": ("Daily Deaths (7-day MA)"),
    "desc": ("Daily deaths count"),
    "longdesc": ("Daily deaths count"),
    "icon": "fas fa-cross",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily",
}
VARS[DAILY_ICU_MA_KEY] = {
    "title": ("Daily ICU (7-day MA)"),
    "desc": ("# of people daily admitted in ICU"),
    "longdesc": ("Daily count of people in ICU"),
    "icon": "fas fa-procedures",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily",
}
VARS[DAILY_SWABS_MA_KEY] = {
    "title": ("Daily Swabs (7-day MA)"),
    "desc": ("# of swabs performed daily"),
    "longdesc": ("Daily number of swabs performed"),
    "icon": "fas fa-vial",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "daily",
}

# Current-state variables
VARS[TOTAL_POSITIVE_KEY] = {
    "title": ("Tot Positive"),
    "desc": (
        "# of people currently " "hospitalized with symptoms + ICU + self isolation"
    ),
    "longdesc": (
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
    "type": "current",
}
VARS[ICU_KEY] = {
    "title": ("ICU"),
    "desc": ("# of people currently in ICU"),
    "longdesc": ("Total count of people currently in ICU and positive to COVID-19"),
    "icon": "fas fa-procedures",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "current",
}

VARS[TOTAL_HOSPITALIZED_KEY] = {
    "title": ("Tot Hospitalized"),
    "desc": ("# of people currently hospitalized"),
    "longdesc": (
        "Total count of people currently hospitalized. " "It takes into account ICU"
    ),
    "icon": "fas fa-hospital-symbol",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "current",
}
VARS[SELF_ISOLATION_KEY] = {
    "title": ("Self Isolation"),
    "desc": ("# of people currently in self isolation"),
    "longdesc": ("People currently positive but who do not need hospitalization"),
    "icon": "fas fa-house-user",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "current",
}

# Cumulative variables
VARS[TOTAL_CASES_KEY] = {
    "title": ("Total Cases"),
    "desc": (
        "Total count of the positive tests since the" " beginning of the outbreak"
    ),
    "longdesc": (
        "Total count of the positive tests since the" " beginning of the outbreak"
    ),
    "icon": "fas fa-viruses",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "cum",
}
VARS[TOTAL_DEATHS_KEY] = {
    "title": ("Total Deaths"),
    "desc": ("Total deaths count"),
    "longdesc": ("Total deaths count since the beginning of the outbreak"),
    "icon": "fas fa-cross",
    "increase": TREND_SYMBOL_LOGIC["increase"],
    "decrease": TREND_SYMBOL_LOGIC["decrease"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "cum",
}

VARS[TOTAL_SWABS_KEY] = {
    "title": ("Total Swabs"),
    "desc": ("# of swabs performed"),
    "longdesc": ("Total number of swabs performed since the beginning of the outbreak"),
    "icon": "fas fa-vial",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "cum",
}
VARS[TOTAL_HEALED_KEY] = {
    "title": ("Total Healed"),
    "desc": ("Cumulative # of people healed"),
    "longdesc": ("Total number of people healed since the beginning of the outbreak"),
    "icon": "fas fa-smile",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "cum",
}

# Vax variables
VARS[VAX_FIRST_DOSE_KEY] = {
    "title": ("First Dose"),
    "icon": "fas fa-battery-half",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "vax",
}
VARS[VAX_SECOND_DOSE_KEY] = {
    "title": ("Second Dose"),
    "icon": "fas fa-battery-full",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "vax",
}
VARS[VAX_BOOSTER1_DOSE_KEY] = {
    "title": ("Booster dose"),
    "icon": "fas fa-plug",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "vax",
}
CUM_QUANTITIES = [q for q in VARS if VARS[q]["type"] == "cum"]
NON_CUM_QUANTITIES = [q for q in VARS if VARS[q]["type"] == "current"]
DAILY_QUANTITIES = [
    quantity
    for quantity in VARS
    if VARS[quantity]["type"] == "daily" and quantity.endswith("_ma")
]
TREND_CARDS = [
    quantity
    for quantity in VARS
    if not quantity.endswith("_ma") and VARS[quantity]["type"] != "vax"
]
PROV_TREND_CARDS = [TOTAL_CASES_KEY, NEW_POSITIVE_KEY]
