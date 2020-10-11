import json

from bson import ObjectId
from flask import jsonify, request, current_app as app

from app import mongo
from app.api import api
from app.utils.data import update_collections
from config import (
    BAR_CHART_COLLECTION, BARCHART_RACE_QUERY, UPDATE_FMT
)

BARCHART_COLLECTION = mongo.db[BAR_CHART_COLLECTION]


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@api.route("/bcr/<string:var_name>")
def get_bcr(var_name):
    """
    Bar-chart race API. Return a JSON with fields "html" and "ts".
    The former contains the HTML code of the bar-chart race video,
    the latter the timestamp at which the bar-chart race was created on the DB
    :param: var_name: str
    :return: flask.jsonify()
    """
    data = {}
    BARCHART_RACE_QUERY["name"] = var_name
    try:
        app.logger.info("Getting {} bcr from mongo".format(var_name))
        data = next(BARCHART_COLLECTION.find(BARCHART_RACE_QUERY))
        data["ts"] = data["ts"].strftime(UPDATE_FMT)
        data["status"] = "ok"
        data = json.loads(JSONEncoder().encode(data))
    except StopIteration:
        err_msg = "No {} bcr data in mongo".format(var_name)
        app.logger.error(err_msg)
        data["status"] = "ko"
        data["error"] = err_msg
    return jsonify(**data)


@api.route("/update_db", methods=["POST"])
def update_db():
    """
    Trigger db-collections update if any last commit contains any
    *latest*.json file
    :return: dict
    """
    response = {}
    do_update = False
    try:
        payload = request.json
        commits = payload["commits"]
        modified_files = [m for c in commits for m in c["modified"]]
        app.logger.info("Modified files: {}".format(modified_files))
        if any("latest.json" in _file for _file in modified_files):
            do_update = True
        if do_update:
            app.logger.warning("Start collections update")
            update_collections()
        response["status"] = "ok"
        response["message"] = "collections updated"
        app.logger.warning("Collections updated")
    except Exception as e:
        app.logger.error("{}".format(e))
        response["status"] = "ko"
        response["message"] = "Error: {}".format(e)
    return jsonify(**response)
