"""
URLs settings
"""
import os

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
