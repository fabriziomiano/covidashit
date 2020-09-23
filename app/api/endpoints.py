from flask import jsonify

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
        data = next(
            mongo.db[COLLECTION_NAME].find(BARCHART_RACE_QUERY)
        )
        data["ts"] = data["ts"].strftime(UPDATE_FMT)
        data["status"] = "ok"
        data = json.loads(JSONEncoder().encode(data))
    except StopIteration:
        data["status"] = "ko"
        data["error"] = "No data"
    return jsonify(**data)
