import json

from bson import ObjectId
from flask import jsonify, current_app as app

from app import mongo
from app.api import api
from config import BAR_CHART_COLLECTION, BARCHART_RACE_QUERY, UPDATE_FMT


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
        data = next(
            mongo.db[BAR_CHART_COLLECTION].find(BARCHART_RACE_QUERY)
        )
        data["ts"] = data["ts"].strftime(UPDATE_FMT)
        data["status"] = "ok"
        data = json.loads(JSONEncoder().encode(data))
    except StopIteration:
        err_msg = "No {} bcr data in mongo".format(var_name)
        app.logger.error(err_msg)
        data["status"] = "ko"
        data["error"] = err_msg
    return jsonify(**data)
