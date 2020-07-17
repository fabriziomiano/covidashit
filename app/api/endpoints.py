from flask import jsonify

from app.api import api
from config import COLLECTION_NAME, BARCHART_RACE_QUERY, UPDATE_FMT


@api.route("/bcr")
def get_bcr():
    """
    Bar-chart race API. Return a JSON with fields "html" and "ts".
    The former contains the HTML code of the bar-chart race video,
    the latter the timestamp at which the bar-chart race was created on the DB
    :return: flask.jsonify()
    """
    from app import mongo
    bcr_data = next(
        mongo.db[COLLECTION_NAME].find(BARCHART_RACE_QUERY)
    )
    bcr_html = bcr_data["html_str"]
    bcr_ts = bcr_data["ts"].strftime(UPDATE_FMT)
    return jsonify(html=bcr_html, ts=bcr_ts)
