import datetime as dt
import os

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
BARCHART_RACE_VAR = "totale_positivi"
#  The order here matters as it will be reflected in the webpage
CARD_TYPES = [
    "nuovi_positivi", "ricoverati_con_sintomi", "terapia_intensiva",
    "deceduti_giornalieri", "totale_positivi", "totale_ospedalizzati",
    "variazione_totale_positivi", "totale_casi", "isolamento_domiciliare",
    "dimessi_guariti", "deceduti", "tamponi"
]
CUSTOM_CARDS = ["deceduti_giornalieri"]
CARD_MAP = {
    "deceduti_giornalieri": "deceduti"
}
REGION_KEY = "denominazione_regione"
PROVINCE_KEY = "denominazione_provincia"
PCM_DATE_FMT = "%Y-%m-%dT%H:%M:%S"
CHART_DATE_FMT = "%d %b"
UPDATE_FMT = "%d/%m/%Y %H:%M"
PCM_DATE_KEY = "data"
LOCKDOWN_DAY = dt.datetime(2020, 3, 9)
PHASE2_DAY = dt.datetime(2020, 5, 4)
REOPENING_DAY = dt.datetime(2020, 5, 18)
LANGUAGES = {
    "en": "English",
    "it_IT": "Italiano"
}
REGIONS = [
    'Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romagna',
    'Friuli Venezia Giulia', 'Lazio', 'Liguria', 'Lombardia',
    'Marche', 'Molise', 'P.A. Bolzano', 'P.A. Trento', 'Piemonte',
    'Puglia', 'Sardegna', 'Sicilia', 'Toscana', 'Umbria',
    "Valle d'Aosta", 'Veneto'
]
PROVINCES = [
    'Agrigento', 'Alessandria', 'Ancona', 'Aosta', 'Arezzo',
    'Ascoli Piceno', 'Asti', 'Avellino', 'Bari',
    'Barletta-Andria-Trani', 'Belluno', 'Benevento', 'Bergamo',
    'Biella', 'Bologna', 'Bolzano', 'Brescia', 'Brindisi', 'Cagliari',
    'Caltanissetta', 'Campobasso', 'Caserta', 'Catania', 'Catanzaro',
    'Chieti', 'Como', 'Cosenza', 'Cremona', 'Crotone', 'Cuneo',
    'Enna', 'Fermo', 'Ferrara', 'Firenze', 'Foggia', 'Forlì-Cesena',
    'Frosinone', 'Genova', 'Gorizia', 'Grosseto', 'Imperia',
    'Isernia', "L'Aquila", 'La Spezia', 'Latina', 'Lecce', 'Lecco',
    'Livorno', 'Lodi', 'Lucca', 'Macerata', 'Mantova',
    'Massa Carrara', 'Matera', 'Messina', 'Milano', 'Modena',
    'Monza e della Brianza', 'Napoli', 'Novara', 'Nuoro', 'Oristano',
    'Padova', 'Palermo', 'Parma', 'Pavia', 'Perugia',
    'Pesaro e Urbino', 'Pescara', 'Piacenza', 'Pisa', 'Pistoia',
    'Pordenone', 'Potenza', 'Prato', 'Ragusa', 'Ravenna',
    'Reggio di Calabria', "Reggio nell'Emilia", 'Rieti', 'Rimini',
    'Roma', 'Rovigo', 'Salerno', 'Sassari', 'Savona', 'Siena',
    'Siracusa', 'Sondrio', 'Sud Sardegna', 'Taranto', 'Teramo',
    'Terni', 'Torino', 'Trapani', 'Trento', 'Treviso', 'Trieste',
    'Udine', 'Varese', 'Venezia', 'Verbano-Cusio-Ossola', 'Vercelli',
    'Verona', 'Vibo Valentia', 'Vicenza', 'Viterbo'
]
DATA_TO_FRONTEND = {
    "regions": REGIONS,
    "provinces": PROVINCES,
    "days_since_phase2": (dt.datetime.today() - PHASE2_DAY).days,
    "days_since_reopening": (dt.datetime.today() - REOPENING_DAY).days,
    "days_in_lockdown": (PHASE2_DAY - LOCKDOWN_DAY).days
}
TRANSLATION_DIRNAME = "translations"
MONGO_URI = os.environ["MONGO_URI"]
DB_NAME = os.environ["DB_NAME"]
COLLECTION_NAME = os.environ["COLLECTION_NAME"]
BARCHART_RACE_QUERY = {"name": "barchart_race"}
