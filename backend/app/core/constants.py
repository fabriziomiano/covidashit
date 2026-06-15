"""Shared product constants for the modern COVIDash application."""

from __future__ import annotations

from collections import OrderedDict
from typing import Any

VERSION = "8.0.1"
PAGE_BASE_TITLE = "COVIDash.it"
DATE_KEY = "data"
NOTE_KEY = "note"
REGION_KEY = "denominazione_regione"
PROVINCE_KEY = "denominazione_provincia"
POSITIVITY_INDEX = "indice_positivita"
VAX_AREA_KEY = "area"
VAX_AGE_KEY = "eta"
VAX_DATE_KEY = "data"
VAX_FIRST_DOSE_KEY = "d1"
VAX_SECOND_DOSE_KEY = "d2"
VAX_BOOSTER_DOSE_KEY = "db1"
VAX_PROVIDER_KEY = "forn"
VAX_TOT_ADMINS_KEY = "totale"
VAX_POP_KEY = "popolazione"
OD_POP_KEY = "totale_popolazione"
TOTAL_CASES_KEY = "totale_casi"
NEW_POSITIVE_KEY = "nuovi_positivi"

ITALY_MAP: dict[str, list[str]] = {
    "Abruzzo": ["Chieti", "L'Aquila", "Pescara", "Teramo"],
    "Basilicata": ["Matera", "Potenza"],
    "Calabria": ["Catanzaro", "Cosenza", "Crotone", "Reggio di Calabria", "Vibo Valentia"],
    "Campania": ["Avellino", "Benevento", "Caserta", "Napoli", "Salerno"],
    "Emilia-Romagna": ["Bologna", "Ferrara", "Forlì-Cesena", "Modena", "Parma", "Piacenza", "Ravenna", "Reggio nell'Emilia", "Rimini"],
    "Friuli Venezia Giulia": ["Gorizia", "Pordenone", "Trieste", "Udine"],
    "Lazio": ["Frosinone", "Latina", "Rieti", "Roma", "Viterbo"],
    "Liguria": ["Genova", "Imperia", "La Spezia", "Savona"],
    "Lombardia": ["Bergamo", "Brescia", "Como", "Cremona", "Lecco", "Lodi", "Mantova", "Milano", "Monza e della Brianza", "Pavia", "Sondrio", "Varese"],
    "Marche": ["Ancona", "Ascoli Piceno", "Fermo", "Macerata", "Pesaro e Urbino"],
    "Molise": ["Campobasso", "Isernia"],
    "Piemonte": ["Alessandria", "Asti", "Biella", "Cuneo", "Novara", "Torino", "Verbano-Cusio-Ossola", "Vercelli"],
    "Puglia": ["Bari", "Barletta-Andria-Trani", "Brindisi", "Lecce", "Foggia", "Taranto"],
    "Sardegna": ["Cagliari", "Nuoro", "Sassari", "Sud Sardegna"],
    "Sicilia": ["Agrigento", "Caltanissetta", "Catania", "Enna", "Messina", "Palermo", "Ragusa", "Siracusa", "Trapani"],
    "Toscana": ["Arezzo", "Firenze", "Grosseto", "Livorno", "Lucca", "Massa Carrara", "Pisa", "Pistoia", "Prato", "Siena"],
    "P.A. Bolzano": [],
    "P.A. Trento": [],
    "Umbria": ["Perugia", "Terni"],
    "Valle d'Aosta": ["Aosta"],
    "Veneto": ["Belluno", "Padova", "Rovigo", "Treviso", "Venezia", "Verona", "Vicenza"],
}
REGIONS = list(ITALY_MAP)
PROVINCES = [province for provinces in ITALY_MAP.values() for province in provinces]
PC_TO_OD_MAP = {
    "Italia": "ITA", "Abruzzo": "ABR", "Basilicata": "BAS", "Calabria": "CAL", "Campania": "CAM",
    "Emilia-Romagna": "EMR", "Friuli Venezia Giulia": "FVG", "Lazio": "LAZ", "Liguria": "LIG",
    "Lombardia": "LOM", "Marche": "MAR", "Molise": "MOL", "P.A. Bolzano": "PAB", "P.A. Trento": "PAT",
    "Piemonte": "PIE", "Puglia": "PUG", "Sardegna": "SAR", "Sicilia": "SIC", "Toscana": "TOS",
    "Umbria": "UMB", "Valle d'Aosta": "VDA", "Veneto": "VEN",
}
OD_TO_PC_MAP = {value: key for key, value in PC_TO_OD_MAP.items()}
TREND_SYMBOL_LOGIC = {
    "stable": {"colour": "text-info", "icon": "bi bi-dash", "tooltip": "Stable with respect to yesterday"},
    "increase": {"colour": "text-danger", "icon": "bi bi-arrow-up-right", "tooltip": "Increased with respect to yesterday"},
    "increase_inverted": {"colour": "text-success", "icon": "bi bi-arrow-up-right", "tooltip": "Increased with respect to yesterday"},
    "decrease": {"colour": "text-success", "icon": "bi bi-arrow-down-left", "tooltip": "Decreased with respect to yesterday"},
    "decrease_inverted": {"colour": "text-danger", "icon": "bi bi-arrow-down-left", "tooltip": "Decreased with respect to yesterday"},
}
VARS: "OrderedDict[str, dict[str, Any]]" = OrderedDict([
    ("nuovi_positivi", {"title": "New Positive", "desc": "Daily count of new positive cases", "icon": "fas fa-head-side-cough", "type": "daily"}),
    ("ingressi_terapia_intensiva", {"title": "Daily ICU", "desc": "# of people daily admitted in ICU", "icon": "fas fa-procedures", "type": "daily"}),
    ("deceduti_g", {"title": "Daily Deaths", "desc": "Daily deaths count", "icon": "fas fa-cross", "type": "daily"}),
    ("tamponi_g", {"title": "Daily Swabs", "desc": "# of swabs performed daily", "icon": "fas fa-vial", "type": "daily"}),
    ("nuovi_positivi_ma", {"title": "New Positive (7-day MA)", "desc": "Daily count of new positive cases", "icon": "fas fa-head-side-cough", "type": "daily"}),
    ("deceduti_g_ma", {"title": "Daily Deaths (7-day MA)", "desc": "Daily deaths count", "icon": "fas fa-cross", "type": "daily"}),
    ("ingressi_terapia_intensiva_ma", {"title": "Daily ICU (7-day MA)", "desc": "# of people daily admitted in ICU", "icon": "fas fa-procedures", "type": "daily"}),
    ("tamponi_g_ma", {"title": "Daily Swabs (7-day MA)", "desc": "# of swabs performed daily", "icon": "fas fa-vial", "type": "daily"}),
    ("totale_positivi", {"title": "Tot Positive", "desc": "# of people currently hospitalized with symptoms + ICU + self isolation", "icon": "fas fa-viruses", "type": "current"}),
    ("terapia_intensiva", {"title": "ICU", "desc": "# of people currently in ICU", "icon": "fas fa-procedures", "type": "current"}),
    ("totale_ospedalizzati", {"title": "Tot Hospitalized", "desc": "# of people currently hospitalized", "icon": "fas fa-hospital-symbol", "type": "current"}),
    ("isolamento_domiciliare", {"title": "Self Isolation", "desc": "# of people currently in self isolation", "icon": "fas fa-house-user", "type": "current"}),
    ("totale_casi", {"title": "Total Cases", "desc": "Total count of the positive tests since the beginning of the outbreak", "icon": "fas fa-viruses", "type": "cum"}),
    ("deceduti", {"title": "Total Deaths", "desc": "Total deaths count", "icon": "fas fa-cross", "type": "cum"}),
    ("tamponi", {"title": "Total Swabs", "desc": "# of swabs performed", "icon": "fas fa-vial", "type": "cum"}),
    ("dimessi_guariti", {"title": "Total Healed", "desc": "Cumulative # of people healed", "icon": "fas fa-smile", "type": "cum"}),
    ("d1", {"title": "First Dose", "icon": "fas fa-vial", "type": "vax"}),
    ("d2", {"title": "Second Dose", "icon": "fas fa-vials", "type": "vax"}),
    ("db1", {"title": "Booster dose", "icon": "fas fa-rocket", "type": "vax"}),
])
for key, item in VARS.items():
    if key in {"tamponi_g", "tamponi", "dimessi_guariti", "d1", "d2", "db1"}:
        item.update(increase=TREND_SYMBOL_LOGIC["increase_inverted"], decrease=TREND_SYMBOL_LOGIC["decrease_inverted"], stable=TREND_SYMBOL_LOGIC["stable"])
    else:
        item.update(increase=TREND_SYMBOL_LOGIC["increase"], decrease=TREND_SYMBOL_LOGIC["decrease"], stable=TREND_SYMBOL_LOGIC["stable"])
VAX_DOSES = [VAX_FIRST_DOSE_KEY, VAX_SECOND_DOSE_KEY, VAX_BOOSTER_DOSE_KEY]
