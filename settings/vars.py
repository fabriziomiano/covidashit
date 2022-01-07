"""
Variables settings
"""
from collections import OrderedDict

from flask_babel import gettext

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
OD_REGION_CODE = "codice_regione_ISTAT"
PROVINCE_CODE = "codice_provincia"
NUTS_KEY = 'codice_nuts_2'
OD_NUTS1_KEY = 'codice_NUTS1'
OD_NUTS2_KEY = 'codice_NUTS2'
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
OD_AREA_KEY = "nome_area"
VAX_TYPE_KEY = "fornitore"
VAX_AGE_KEY = "fascia_anagrafica"
POP_KEY = "popolazione"
OD_POP_KEY = "totale_popolazione"
ADMINS_DOSES_KEY = "dosi_somministrate"
DELIVERED_DOSES_KEY = "dosi_consegnate"
VAX_ADMINS_PERC_KEY = "percentuale_somministrazione"
VAX_TOT_ADMINS_KEY = "totale"
VAX_FIRST_DOSE_KEY = "prima_dose"
VAX_SECOND_DOSE_KEY = "seconda_dose"
VAX_BOOSTER_DOSE_KEY = "dose_addizionale_booster"
VAX_PROVIDER_KEY = "fornitore"
F_SEX_KEY = "sesso_femminile"
M_SEX_KEY = "sesso_maschile"
RUBBISH_NOTE_REGEX = r"[a-z][a-z]-[A-Z]\w+-[0-9][0-9][0-9][0-9]"
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

# Current-state variables
VARS[TOTAL_POSITIVE_KEY] = {
    "title": gettext("Tot Positive"),
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
    "title": gettext("ICU"),
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

VARS[TOTAL_HOSPITALIZED_KEY] = {
    "title": gettext("Tot Hospitalized"),
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
VARS[VAX_FIRST_DOSE_KEY] = {
    "title": gettext("First Dose"),
    "icon": "fas fa-battery-half",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "vax"
}
VARS[VAX_SECOND_DOSE_KEY] = {
    "title": gettext("Second Dose"),
    "icon": "fas fa-battery-full",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "vax"
}
VARS[VAX_BOOSTER_DOSE_KEY] = {
    "title": gettext("Booster dose"),
    "icon": "fas fa-plug",
    "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
    "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
    "stable": TREND_SYMBOL_LOGIC["stable"],
    "type": "vax"
}
