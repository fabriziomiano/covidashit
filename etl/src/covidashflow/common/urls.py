"""Remote CSV and JSON source URLs consumed by the ETL pipelines."""

from urllib.parse import urljoin

BASE_URL_DATA = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/"
NATIONAL_DATA_FILE = "dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
REGIONAL_DATA_FILE = "dati-regioni/dpc-covid19-ita-regioni.csv"
PROVINCIAL_DATE_FILE = "dati-province/dpc-covid19-ita-province.csv"

URL_NATIONAL = urljoin(BASE_URL_DATA, NATIONAL_DATA_FILE)
URL_REGIONAL = urljoin(BASE_URL_DATA, REGIONAL_DATA_FILE)
URL_PROVINCIAL = urljoin(BASE_URL_DATA, PROVINCIAL_DATE_FILE)

BASE_URL_VAX_DATA = (
    "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/"
)
VAX_ADMINS_FILE = "somministrazioni-vaccini-latest.csv"
VAX_ADMINS_SUMMARY_FILE = "somministrazioni-vaccini-summary-latest.csv"
VAX_SUMMARY_FILE = "vaccini-summary-latest.csv"
VAX_LATEST_UPDATE = "last-update-dataset.json"
VAX_POP_FILE = "platea.csv"

URL_VAX_ADMINS_DATA = urljoin(BASE_URL_VAX_DATA, VAX_ADMINS_FILE)
URL_VAX_LATEST_UPDATE = urljoin(BASE_URL_VAX_DATA, VAX_LATEST_UPDATE)
URL_VAX_SUMMARY_DATA = urljoin(BASE_URL_VAX_DATA, VAX_SUMMARY_FILE)
URL_VAX_ADMINS_SUMMARY_DATA = urljoin(BASE_URL_VAX_DATA, VAX_ADMINS_SUMMARY_FILE)
URL_VAX_POP_DATA = urljoin(BASE_URL_VAX_DATA, VAX_POP_FILE)
