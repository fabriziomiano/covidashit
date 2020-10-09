import datetime as dt
import os

from flask_babel import gettext

DAILY_SWABS_KEY = "tamponi_giornalieri"
HOSPITALIZED_WITH_SYMPTOMS_KEY = "ricoverati_con_sintomi"
ICU_KEY = "terapia_intensiva"
TOTAL_HOSPITALIZED_KEY = "totale_ospedalizzati"
SELF_ISOLATION_KEY = "isolamento_domiciliare"
TOTAL_POSITIVE_KEY = "totale_positivi"
TOTAL_POSITIVE_VARIATION_KEY = "variazione_totale_positivi"
NEW_POSITIVE_KEY = "nuovi_positivi"
TOTAL_HEALED_KEY = "dimessi_guariti"
TOTAL_DEATHS_KEY = "deceduti"
TOTAL_CASES_KEY = "totale_casi"
TOTAL_SWABS_KEY = "tamponi"
DAILY_DEATHS_KEY = "deceduti_giornalieri"
POSITIVE_SUSPECTED_KEY = "casi_da_sospetto_diagnostico"
POSITIVE_FROM_SCREENING_KEY = "casi_da_screening"
TOTAL_TESTED = "casi_testati"
REGION_KEY = "denominazione_regione"
PROVINCE_KEY = "denominazione_provincia"
PCM_DATE_FMT = "%Y-%m-%dT%H:%M:%S"
CHART_DATE_FMT = "%d %b"
UPDATE_FMT = "%d/%m/%Y %H:%M"
PCM_DATE_KEY = "data"
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
        "stable": TREND_SYMBOL_LOGIC["stable"]
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
        "stable": TREND_SYMBOL_LOGIC["stable"]
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
        "stable": TREND_SYMBOL_LOGIC["stable"]
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
        "stable": TREND_SYMBOL_LOGIC["stable"]
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
        "stable": TREND_SYMBOL_LOGIC["stable"]
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
        "stable": TREND_SYMBOL_LOGIC["stable"]
    },
    NEW_POSITIVE_KEY: {
        "title": gettext("New Positive"),
        "desc": gettext("Daily count of new positve cases"),
        "longdesc": gettext("Daily count of new positve cases"),
        "icon": "fas fa-user-plus",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"]
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
        "stable": TREND_SYMBOL_LOGIC["stable"]
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
        "stable": TREND_SYMBOL_LOGIC["stable"]
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
        "stable": TREND_SYMBOL_LOGIC["stable"]
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
        "stable": TREND_SYMBOL_LOGIC["stable"]
    },
    DAILY_SWABS_KEY: {
        "title": gettext("Daily Swabs"),
        "desc": gettext("# of swabs performed today"),
        "longdesc": gettext(
            "Number of swabs performed today"
        ),
        "icon": "fas fa-vial",
        "increase": TREND_SYMBOL_LOGIC["increase_inverted"],
        "decrease": TREND_SYMBOL_LOGIC["decrease_inverted"],
        "stable": TREND_SYMBOL_LOGIC["stable"]
    },
    DAILY_DEATHS_KEY: {
        "title": gettext("Daily deaths"),
        "desc": gettext("Daily deaths count"),
        "longdesc": gettext("Daily deaths count"),
        "icon": "fas fa-cross",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"]
    },
    POSITIVE_SUSPECTED_KEY: {
        "title": gettext("Positive suspected case"),
        "desc": gettext("Positive cases emerged from clinical activity"),
        "longdesc": gettext("Positive cases emerged from clinical activity"),
        "icon": "fas fa-diagnoses",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"]
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
        "stable": TREND_SYMBOL_LOGIC["stable"]
    },
    TOTAL_TESTED: {
        "title": gettext("Total tested"),
        "desc": gettext("Total number of people tested"),
        "longdesc": gettext("Total number of people tested"),
        "icon": "fas fa-stethoscope",
        "increase": TREND_SYMBOL_LOGIC["increase"],
        "decrease": TREND_SYMBOL_LOGIC["decrease"],
        "stable": TREND_SYMBOL_LOGIC["stable"]
    },
}

NATIONAL_DATA_FILE = "dpc-covid19-ita-andamento-nazionale.json"
LATEST_NATIONAL_DATA_FILE = "dpc-covid19-ita-andamento-nazionale-latest.json"
REGIONAL_DATA_FILE = "dpc-covid19-ita-regioni.json"
LATEST_REGIONAL_DATA_FILE = "dpc-covid19-ita-regioni-latest.json"
PROVINCIAL_DATE_FILE = "dpc-covid19-ita-province.json"
LATEST_PROVINCIAL_DATE_FILE = "dpc-covid19-ita-province-latest.json"
BASE_URL_DATA = (
    "https://raw.githubusercontent.com"
    "/pcm-dpc/COVID-19/master/dati-json/"
)
URL_NATIONAL_DATA = os.path.join(BASE_URL_DATA, NATIONAL_DATA_FILE)
URL_LATEST_NATIONAL_DATA = os.path.join(
    BASE_URL_DATA, LATEST_NATIONAL_DATA_FILE
)
URL_REGIONAL_DATA = os.path.join(BASE_URL_DATA, REGIONAL_DATA_FILE)
URL_LATEST_REGIONAL_DATA = os.path.join(
    BASE_URL_DATA, LATEST_REGIONAL_DATA_FILE
)
URL_PROVINCIAL_DATA = os.path.join(BASE_URL_DATA, PROVINCIAL_DATE_FILE)
URL_LATEST_PROVINCIAL_DATA = os.path.join(
    BASE_URL_DATA, LATEST_PROVINCIAL_DATE_FILE
)
#  The order here matters as it will be reflected in the webpage
CARD_TYPES = [
    NEW_POSITIVE_KEY,
    HOSPITALIZED_WITH_SYMPTOMS_KEY,
    ICU_KEY,
    DAILY_SWABS_KEY,
    DAILY_DEATHS_KEY,
    SELF_ISOLATION_KEY,
    POSITIVE_SUSPECTED_KEY,
    POSITIVE_FROM_SCREENING_KEY,
    TOTAL_TESTED,
    TOTAL_POSITIVE_VARIATION_KEY,
    TOTAL_POSITIVE_KEY,
    TOTAL_HOSPITALIZED_KEY,
    TOTAL_HEALED_KEY,
    TOTAL_DEATHS_KEY,
    TOTAL_SWABS_KEY,
    TOTAL_CASES_KEY
]
CUSTOM_CARDS = [DAILY_DEATHS_KEY, DAILY_SWABS_KEY]
CUMULATIVE_DATA_TYPES = [
    TOTAL_TESTED,
    TOTAL_POSITIVE_VARIATION_KEY,
    TOTAL_HEALED_KEY,
    TOTAL_SWABS_KEY,
    TOTAL_CASES_KEY
]
CARD_MAP = {
    DAILY_DEATHS_KEY: TOTAL_DEATHS_KEY,
    DAILY_SWABS_KEY: TOTAL_SWABS_KEY
}
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
COLLECTION_NAME = os.environ["COLLECTION_NAME"]
BARCHART_RACE_QUERY = {"name": ""}
DATA_SERIES = [
    VARS_CONFIG[key]["title"]
    for key in VARS_CONFIG
    if key not in CUSTOM_CARDS
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
DATA_TYPE = {
    "national": {
        "url": URL_NATIONAL_DATA,
        "cache_file": NATIONAL_DATA_FILE
    },
    "provincial": {
        "url": URL_PROVINCIAL_DATA,
        "cache_file": PROVINCIAL_DATE_FILE
    },
    "regional": {
        "url": URL_REGIONAL_DATA,
        "cache_file": REGIONAL_DATA_FILE
    },
    "latest_national": {
        "url": URL_LATEST_NATIONAL_DATA,
        "cache_file": LATEST_NATIONAL_DATA_FILE
    },
    "latest_regional": {
        "url": URL_LATEST_REGIONAL_DATA,
        "cache_file": LATEST_REGIONAL_DATA_FILE
    },
    "latest_provincial": {
        "url": URL_LATEST_PROVINCIAL_DATA,
        "cache_file": LATEST_PROVINCIAL_DATE_FILE
    }
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
