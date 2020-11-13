import datetime as dt
import os

from flask_babel import gettext

HOSPITALIZED_WITH_SYMPTOMS_KEY = "ricoverati_con_sintomi"
HOSPITALIZED_WITH_SYMPTOMS_D_KEY = "ricoverati_con_sintomi_g"
ICU_KEY = "terapia_intensiva"
ICU_D_KEY = "terapia_intensiva_g"
TOTAL_HOSPITALIZED_KEY = "totale_ospedalizzati"
TOTAL_HOSPITALIZED_D_KEY = "totale_ospedalizzati_g"
SELF_ISOLATION_KEY = "isolamento_domiciliare"
SELF_ISOLATION_D_KEY = "isolamento_domiciliare_g"
TOTAL_POSITIVE_KEY = "totale_positivi"
TOTAL_POSITIVE_D_KEY = "totale_positivi_g"
TOTAL_POSITIVE_VARIATION_KEY = "variazione_totale_positivi"
TOTAL_POSITIVE_VARIATION_D_KEY = "variazione_totale_positivi_g"
NEW_POSITIVE_KEY = "nuovi_positivi"
NEW_POSITIVE_D_KEY = "nuovi_positivi_g"
TOTAL_HEALED_KEY = "dimessi_guariti"
TOTAL_HEALED_D_KEY = "dimessi_guariti_g"
TOTAL_DEATHS_KEY = "deceduti"
TOTAL_DEATHS_D_KEY = "deceduti_g"
TOTAL_CASES_KEY = "totale_casi"
TOTAL_CASES_D_KEY = "totale_casi_g"
TOTAL_SWABS_KEY = "tamponi"
TOTAL_SWABS_D_KEY = "tamponi_g"
POSITIVE_SUSPECTED_KEY = "casi_da_sospetto_diagnostico"
POSITIVE_SUSPECTED_D_KEY = "casi_da_sospetto_diagnostico_g"
POSITIVE_FROM_SCREENING_KEY = "casi_da_screening"
POSITIVE_FROM_SCREENING_D_KEY = "casi_da_screening_g"
TOTAL_TESTED_KEY = "casi_testati"
TOTAL_TESTED_D_KEY = "casi_testati_g"
REGION_KEY = "denominazione_regione"
PROVINCE_KEY = "denominazione_provincia"
REGION_CODE = "codice_regione"
PROVINCE_CODE = "codice_provincia"
CP_DATE_FMT = "%Y-%m-%dT%H:%M:%S"
CHART_DATE_FMT = "%d %b"
UPDATE_FMT = "%d/%m/%Y %H:%M"
DATE_KEY = "data"
DATA_TO_MONITOR = "json"
NOTE_KEY = "note"
RUBBISH_NOTE_REGEX = r"[a-z][a-z]-[A-Z]\w+-[0-9][0-9][0-9][0-9]"
TRANSLATION_DIRNAME = "translations"
TREND_SYMBOL_LOGIC = {
    "stable": {
        "colour": "text-info",
        "icon": "fas fa-minus",
        "tooltip": gettext("Stable with respect to yesterday")
    },
    "increase": {
        "colour": "text-danger",
        "icon": "fas fa-long-arrow-alt-up",
        "tooltip": gettext("Increased with respect to yesterday")
    },
    "increase_inverted": {
        "colour": "text-success",
        "icon": "fas fa-long-arrow-alt-up",
        "tooltip": gettext("Increased with respect to yesterday")
    },
    "decrease": {
        "colour": "text-success",
        "icon": "fas fa-long-arrow-alt-down",
        "tooltip": gettext("Decreased with respect to yesterday")
    },
    "decrease_inverted": {
        "colour": "text-danger",
        "icon": "fas fa-long-arrow-alt-down",
        "tooltip": gettext("Decreased with respect to yesterday")
    }
}
VARS_CONFIG = {
    HOSPITALIZED_WITH_SYMPTOMS_KEY: {
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
    },
    HOSPITALIZED_WITH_SYMPTOMS_D_KEY: {
        "title": gettext("Daily Hospitalized With Symptoms"),
        "desc": gettext(
            "# of people with symptoms hospitalized every day"
        ),
        "longdesc": gettext(
            "Daily count of people admitted in hospital "
            "due to coronavirus with symptoms"
        ),
        "icon": "fas fa-hospital-symbol",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "daily"
    },
    ICU_KEY: {
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
    },
    ICU_D_KEY: {
        "title": gettext("Daily Intensive Care Unit"),
        "desc": gettext("# of people daily admitted in ICU"),
        "longdesc": gettext(
            "Daily count of people in ICU"
        ),
        "icon": "fas fa-procedures",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "daily"
    },
    TOTAL_HOSPITALIZED_KEY: {
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
    },
    TOTAL_HOSPITALIZED_D_KEY: {
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
    },
    SELF_ISOLATION_KEY: {
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
    },
    SELF_ISOLATION_D_KEY: {
        "title": gettext("Daily self Isolation"),
        "desc": gettext("Daily count of people in self isolation"),
        "longdesc": gettext("Daily count of positive people put in isolation"),
        "icon": "fas fa-house-user",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "daily"
    },
    TOTAL_POSITIVE_KEY: {
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
    },
    TOTAL_POSITIVE_D_KEY: {
        "title": gettext("Daily Positive"),
        "desc": gettext(
            "Daily number of people hospitalized with symptoms"
            " + ICU + self isolation"
        ),
        "longdesc": gettext(
            "Daily number of people positive. "
            "Unlike 'Total Cases' it does not take into account "
            "'healed' and 'deaths'. By the end of the outbreak "
            "this should tend to zero. In particular, it is: "
            "total positive = total cases - total healed - total deaths"
        ),
        "icon": "fas fa-viruses",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "daily"
    },
    TOTAL_POSITIVE_VARIATION_KEY: {
        "title": gettext("Total Positive Variation"),
        "desc": gettext(
            "Variation of # of people currently positive "
            "with respect to yesterday"
        ),
        "longdesc": gettext(
            "Variation of the number of people currently positive "
            "with respect to the previous day. It is negative when the number "
            "of daily healed and deaths is larger than 'New positive'"
        ),
        "icon": "fas fa-chart-area",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "current"
    },
    TOTAL_POSITIVE_VARIATION_D_KEY: {
        "title": gettext("Daily Positive Variation"),
        "desc": gettext(
            "Variation of daily # people currently positive "
            "with respect to yesterday"
        ),
        "longdesc": gettext(
            "Variation of the number of people currently positive "
            "with respect to the previous day. It is negative when the number "
            "of daily healed and deaths is larger than 'New positive'"
        ),
        "icon": "fas fa-chart-area",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "daily"
    },
    NEW_POSITIVE_KEY: {
        "title": gettext("New Positive"),
        "desc": gettext("Daily count of new positve cases"),
        "longdesc": gettext("Daily count of new positve cases"),
        "icon": "fas fa-user-plus",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "current"
    },
    NEW_POSITIVE_D_KEY: {
        "title": gettext("Daily New Positive"),
        "desc": gettext("Daily count of daily new positve cases"),
        "longdesc": gettext("Daily count of daily new positve cases"),
        "icon": "fas fa-user-plus",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "daily"
    },
    TOTAL_HEALED_KEY: {
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
    },
    TOTAL_HEALED_D_KEY: {
        "title": gettext("Daily Healed"),
        "desc": gettext("Daily # of people healed"),
        "longdesc": gettext(
            "Daily number of people healed"
        ),
        "icon": "fas fa-smile",
        "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
        "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "daily"
    },
    TOTAL_DEATHS_KEY: {
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
    },
    TOTAL_DEATHS_D_KEY: {
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
    },
    TOTAL_CASES_KEY: {
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
    },
    TOTAL_CASES_D_KEY: {
        "title": gettext("Daily total Cases"),
        "desc": gettext("Daily count of the positive tests"),
        "longdesc": gettext(
            "Total count of the positive tests since the"
            " beginning of the outbreak"
        ),
        "icon": "fas fa-viruses",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "daily"
    },
    TOTAL_SWABS_KEY: {
        "title": gettext("Total Swabs"),
        "desc": gettext("# of swabs performed"),
        "longdesc": gettext(
            "Total number of swabs performed since the beginning of "
            "the outbreak"
        ),
        "icon": "fas fa-vial",
        "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
        "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "cum"
    },
    TOTAL_SWABS_D_KEY: {
        "title": gettext("Daily Swabs"),
        "desc": gettext("# of swabs performed daily"),
        "longdesc": gettext(
            "Daily number of swabs performed since the beginning of "
            "the outbreak"
        ),
        "icon": "fas fa-vial",
        "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
        "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "daily"
    },
    POSITIVE_SUSPECTED_KEY: {
        "title": gettext("Positive suspected case"),
        "desc": gettext("Positive cases emerged from clinical activity"),
        "longdesc": gettext("Positive cases emerged from clinical activity"),
        "icon": "fas fa-diagnoses",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "cum"
    },
    POSITIVE_SUSPECTED_D_KEY: {
        "title": gettext("Daily positive suspected case"),
        "desc": gettext("Positive cases emerged from clinical activity"),
        "longdesc": gettext("Positive cases emerged from clinical activity"),
        "icon": "fas fa-diagnoses",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "daily"
    },
    POSITIVE_FROM_SCREENING_KEY: {
        "title": gettext("Positive from screening"),
        "desc": gettext(
            "Positive cases emerging from surveys and tests, "
            "planned at national or regional level"
        ),
        "longdesc": gettext(
            "Positive cases emerging from surveys and tests,"
            " planned at national or regional level"
        ),
        "icon": "fas fa-stethoscope",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "cum"
    },
    POSITIVE_FROM_SCREENING_D_KEY: {
        "title": gettext("Daily positive from screening"),
        "desc": gettext(
            "Daily positive cases emerging from surveys and tests, "
            "planned at national or regional level"
        ),
        "longdesc": gettext(
            "Daily positive cases emerging from surveys and tests,"
            " planned at national or regional level"
        ),
        "icon": "fas fa-stethoscope",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "daily"
    },
    TOTAL_TESTED_KEY: {
        "title": gettext("Total tested"),
        "desc": gettext("Total number of people tested"),
        "longdesc": gettext("Total number of people tested"),
        "icon": "fas fa-stethoscope",
        "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
        "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "cum"
    },
    TOTAL_TESTED_D_KEY: {
        "title": gettext("Daily tested"),
        "desc": gettext("Daily number of people tested"),
        "longdesc": gettext("Daily number of people tested"),
        "icon": "fas fa-stethoscope",
        "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
        "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
        "stable": TREND_SYMBOL_LOGIC["stable"],
        "type": "daily"
    }
}

NATIONAL_DATA_FILE = (
    "dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
REGIONAL_DATA_FILE = "dati-regioni/dpc-covid19-ita-regioni.csv"
PROVINCIAL_DATE_FILE = "dati-province/dpc-covid19-ita-province.csv"
BASE_URL_DATA = (
    "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/"
)
URL_NATIONAL_DATA = os.path.join(BASE_URL_DATA, NATIONAL_DATA_FILE)
URL_REGIONAL_DATA = os.path.join(BASE_URL_DATA, REGIONAL_DATA_FILE)
URL_PROVINCIAL_DATA = os.path.join(BASE_URL_DATA, PROVINCIAL_DATE_FILE)

LOCKDOWN_DAY = dt.datetime(2020, 3, 9)
PHASE2_DAY = dt.datetime(2020, 5, 4)
REOPENING_DAY = dt.datetime(2020, 5, 18)
LANGUAGES = {
    "en": "English",
    "it_IT": "Italiano"
}
REGIONS = [
    "Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna",
    "Friuli Venezia Giulia", "Lazio", "Liguria", "Lombardia",
    "Marche", "Molise", "P.A. Bolzano", "P.A. Trento", "Piemonte",
    "Puglia", "Sardegna", "Sicilia", "Toscana", "Umbria",
    "Valle d'Aosta", "Veneto"
]
PROVINCES = [
    "Agrigento", "Alessandria", "Ancona", "Aosta", "Arezzo",
    "Ascoli Piceno", "Asti", "Avellino", "Bari",
    "Barletta-Andria-Trani", "Belluno", "Benevento", "Bergamo",
    "Biella", "Bologna", "Bolzano", "Brescia", "Brindisi", "Cagliari",
    "Caltanissetta", "Campobasso", "Caserta", "Catania", "Catanzaro",
    "Chieti", "Como", "Cosenza", "Cremona", "Crotone", "Cuneo",
    "Enna", "Fermo", "Ferrara", "Firenze", "Foggia", "Forlì-Cesena",
    "Frosinone", "Genova", "Gorizia", "Grosseto", "Imperia",
    "Isernia", "L'Aquila", "La Spezia", "Latina", "Lecce", "Lecco",
    "Livorno", "Lodi", "Lucca", "Macerata", "Mantova",
    "Massa Carrara", "Matera", "Messina", "Milano", "Modena",
    "Monza e della Brianza", "Napoli", "Novara", "Nuoro", "Oristano",
    "Padova", "Palermo", "Parma", "Pavia", "Perugia",
    "Pesaro e Urbino", "Pescara", "Piacenza", "Pisa", "Pistoia",
    "Pordenone", "Potenza", "Prato", "Ragusa", "Ravenna",
    "Reggio di Calabria", "Reggio nell'Emilia", "Rieti", "Rimini",
    "Roma", "Rovigo", "Salerno", "Sassari", "Savona", "Siena",
    "Siracusa", "Sondrio", "Sud Sardegna", "Taranto", "Teramo",
    "Terni", "Torino", "Trapani", "Trento", "Treviso", "Trieste",
    "Udine", "Varese", "Venezia", "Verbano-Cusio-Ossola", "Vercelli",
    "Verona", "Vibo Valentia", "Vicenza", "Viterbo"
]
DASHBOARD_DATA = {
    "regions": REGIONS,
    "provinces": PROVINCES,
    "days_since_phase2": (dt.datetime.today() - PHASE2_DAY).days,
    "days_since_reopening": (dt.datetime.today() - REOPENING_DAY).days,
    "days_in_lockdown": (PHASE2_DAY - LOCKDOWN_DAY).days
}
MONGO_URI = os.environ["MONGO_URI"]
BAR_CHART_COLLECTION = os.environ["BAR_CHART_COLLECTION"]
NATIONAL_DATA_COLLECTION = os.environ["NATIONAL_DATA_COLLECTION"]
NATIONAL_TRENDS_COLLECTION = os.environ["NATIONAL_TRENDS_COLLECTION"]
NATIONAL_SERIES_COLLECTION = os.environ["NATIONAL_SERIES_COLLECTION"]
REGIONAL_DATA_COLLECTION = os.environ["REGIONAL_DATA_COLLECTION"]
REGIONAL_TRENDS_COLLECTION = os.environ["REGIONAL_TRENDS_COLLECTION"]
REGIONAL_SERIES_COLLECTION = os.environ["REGIONAL_SERIES_COLLECTION"]
REGIONAL_BREAKDOWN_COLLECTION = os.environ["REGIONAL_BREAKDOWN_COLLECTION"]
PROVINCIAL_DATA_COLLECTION = os.environ["PROVINCIAL_DATA_COLLECTION"]
PROVINCIAL_TRENDS_COLLECTION = os.environ["PROVINCIAL_TRENDS_COLLECTION"]
PROVINCIAL_SERIES_COLLECTION = os.environ["PROVINCIAL_SERIES_COLLECTION"]
PROVINCIAL_BREAKDOWN_COLLECTION = os.environ["PROVINCIAL_BREAKDOWN_COLLECTION"]

DATA_SERIES = [
    VARS_CONFIG[key]["title"]
    for key in VARS_CONFIG
]
#  The order here matters as it will be reflected in the webpage
BCR_TYPES = [
    HOSPITALIZED_WITH_SYMPTOMS_KEY,
    ICU_KEY,
    TOTAL_HOSPITALIZED_KEY,
    TOTAL_POSITIVE_KEY,
    TOTAL_HEALED_KEY,
    TOTAL_DEATHS_KEY,
    TOTAL_CASES_KEY,
    TOTAL_SWABS_KEY
]
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
    # 'Trentino-Alto Adige': ['Bolzano', 'Trento'],
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
