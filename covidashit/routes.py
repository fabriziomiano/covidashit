import json
import requests
from flask import render_template, Response
from covidashit import app, dataset
from config import (
    WEBSITE_TITLE, URL_REGIONAL_DATA, URL_NATIONAL_DATA, URL_PROVINCIAL_DATA,
    PCM_DATE_KEY, NATIONAL_DATA_FILE, REGIONAL_DATA_FILE, PROVINCIAL_DATE_FILE
)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", pagetitle=WEBSITE_TITLE), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html", pagetitle=WEBSITE_TITLE), 500


@app.route("/api/national")
def get_national_data():
    data = {}
    try:
        response = requests.get(URL_NATIONAL_DATA)
        status = response.status_code
        if status == 200:
            national_data = response.json()
            data["national"] = sorted(national_data, key=lambda x: x[PCM_DATE_KEY])
            dataset.cache_data(data["national"], NATIONAL_DATA_FILE)
        else:
            app.logger.error("Could not get data: ERROR {}".format(status))
            data["national"] = dataset.read_cached_data(NATIONAL_DATA_FILE)
            status = 200
    except Exception as e:
        app.logger.error("Request Error {}".format(e))
        data["national"] = dataset.read_cached_data(NATIONAL_DATA_FILE)
        status = 200
    return Response(
        json.dumps(data), mimetype='application/json', status=status
    )


@app.route("/api/regional")
def get_regional_data():
    data = {}
    try:
        response = requests.get(URL_REGIONAL_DATA)
        status = response.status_code
        if status == 200:
            regional_data = response.json()
            data["regional"] = sorted(regional_data, key=lambda x: x[PCM_DATE_KEY])
            dataset.cache_data(data["regional"], REGIONAL_DATA_FILE)
        else:
            app.logger.error("Could not get data: ERROR {}".format(status))
            data["regional"] = dataset.read_cached_data(REGIONAL_DATA_FILE)
            status = 200
    except Exception as e:
        app.logger.error("Request Error {}".format(e))
        data["regional"] = dataset.read_cached_data(REGIONAL_DATA_FILE)
        status = 200
    return Response(
        json.dumps(data), mimetype='application/json', status=status
    )


@app.route("/api/provincial")
def get_provincial_data():
    data = {}
    try:
        response = requests.get(URL_PROVINCIAL_DATA)
        status = response.status_code
        if status == 200:
            prov_data = response.json()
            data["provincial"] = sorted(prov_data, key=lambda x: x[PCM_DATE_KEY])
            dataset.cache_data(data["provincial"], PROVINCIAL_DATE_FILE)
        else:
            app.logger.error("Could not get data: ERROR {}".format(status))
            data["provincial"] = dataset.read_cached_data(PROVINCIAL_DATE_FILE)
            status = 200
    except Exception as e:
        app.logger.error("Request Error {}".format(e))
        data["provincial"] = dataset.read_cached_data(PROVINCIAL_DATE_FILE)
        status = 200
    return Response(
        json.dumps(data), mimetype='application/json', status=status
    )
