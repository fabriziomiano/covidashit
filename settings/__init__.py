"""
Settings Module
"""
import datetime as dt
from collections import OrderedDict

from flask_babel import gettext

VERSION = "5.8"
PAGE_BASE_TITLE = gettext("COVID-19 Italy")
LOCKDOWN_DAY = dt.datetime(2020, 3, 22)
PHASE2_DAY = dt.datetime(2020, 5, 4)
PHASE3_DAY = dt.datetime(2020, 6, 15)
CRITICAL_AREAS_DAY = dt.datetime(2020, 11, 6)
VACCINE_DAY = dt.datetime(2020, 12, 27)
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
TRANSLATION_DIRNAME = "translations"
