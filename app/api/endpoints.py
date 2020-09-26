from flask import jsonify, current_app

from app.api import api
from config import COLLECTION_NAME, BARCHART_RACE_QUERY, UPDATE_FMT

import json
from bson import ObjectId


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
    from app import mongo
    data = {}
    BARCHART_RACE_QUERY["name"] = var_name
    try:
        current_app.logger.info("Getting {} bcr from mongo".format(var_name))
        data = next(
            mongo.db[COLLECTION_NAME].find(BARCHART_RACE_QUERY)
        )
        data["ts"] = data["ts"].strftime(UPDATE_FMT)
        data["status"] = "ok"
        data = json.loads(JSONEncoder().encode(data))
    except StopIteration:
        err_msg = "No {} bcr data in mongo".format(var_name)
        current_app.logger.error(err_msg)
        data["status"] = "ko"
        data["error"] = err_msg
    return jsonify(**data)
