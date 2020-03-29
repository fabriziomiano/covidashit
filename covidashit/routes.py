import json
import requests
from flask import render_template, Response
from covidashit import app
from config import (
    WEBSITE_TITLE, URL_REGIONAL_DATA, URL_NATIONAL_DATA, URL_PROVINCIAL_DATA,
    PCM_DATE_KEY
)


@app.errorhandler(404)
def page_not_found(e):
    app.logger.error("Error {}".format(e))
    return render_template("404.html", title=WEBSITE_TITLE), 404


@app.errorhandler(500)
def server_error(e):
    app.logger.error("Error {}".format(e))
    return render_template("500.html", title=WEBSITE_TITLE), 500


@app.route("/api/national")
def get_national_data():
    data = {}
    response = requests.get(URL_NATIONAL_DATA)
    status = response.status_code
    if status == 200:
        data["national"] = sorted(response.json(), key=lambda x: x[PCM_DATE_KEY])
    return Response(
        json.dumps(data), mimetype='application/json', status=status
    )


@app.route("/api/regional")
def get_regional_data():
    data = {}
    response = requests.get(URL_REGIONAL_DATA)
    status = response.status_code
    if status == 200:
        data["regional"] = sorted(response.json(), key=lambda x: x[PCM_DATE_KEY])
    return Response(
        json.dumps(data), mimetype='application/json', status=status
    )


@app.route("/api/provincial")
def get_provincial_data():
    data = {}
    response = requests.get(URL_PROVINCIAL_DATA)
    status = response.status_code
    if status == 200:
        data["provincial"] = sorted(response.json(), key=lambda x: x[PCM_DATE_KEY])
    return Response(
        json.dumps(data), mimetype='application/json', status=status
    )
