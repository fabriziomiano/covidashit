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
VAX_ADMINS_FILE = "somministrazioni-vaccini-latest.csv"
VAX_ADMINS_SUMMARY_FILE = "somministrazioni-vaccini-summary-latest.csv"
VAX_SUMMARY_FILE = "vaccini-summary-latest.csv"
VAX_LATEST_UPDATE = "last-update-dataset.json"
VAX_POP_FILE = "platea.csv"
URL_VAX_ADMINS_DATA = os.path.join(BASE_URL_VAX_DATA, VAX_ADMINS_FILE)
URL_VAX_LATEST_UPDATE = os.path.join(BASE_URL_VAX_DATA, VAX_LATEST_UPDATE)
URL_VAX_SUMMARY_DATA = os.path.join(BASE_URL_VAX_DATA, VAX_SUMMARY_FILE)
URL_VAX_ADMINS_SUMMARY_DATA = os.path.join(
    BASE_URL_VAX_DATA, VAX_ADMINS_SUMMARY_FILE)
URL_VAX_POP_DATA = os.path.join(BASE_URL_VAX_DATA, VAX_POP_FILE)
BASE_ISTAT_URL = "http://sdmx.istat.it/SDMXWS/rest/data"
URL_ISTAT_POP = os.path.join(
    BASE_ISTAT_URL,
    "22_289/"
    ".TOTAL."
    "ITC1+ITC2+ITC3+ITC4+"
    "ITD1+ITD2+ITD3+ITD4+ITD5+"
    "ITE1+ITE2+ITE3+ITE4+"
    "ITF1+ITF2+ITF3+ITF4+ITF5+ITF6+"
    "ITG1+ITG2"
    ".9.99../"
    "?startPeriod=2021&format=csv"
)
URL_ISTAT_AGE_POP = os.path.join(
    BASE_ISTAT_URL,
    "22_289/"
    "..ITC1+ITC2+ITC3+ITC4+ITD1+ITD2+ITD3+ITD4+ITD5+ITE1+ITE2+ITE3+ITE4+ITF1+"
    "ITF2+ITF3+ITF4+ITF5+ITF6+ITG1+ITG2."
    "9.99..?format=csv&startPeriod=2021&detail=dataonly"
)
