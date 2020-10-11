import datetime as dt

from flask import jsonify, request, current_app as app

from app import mongo
from app.api import api
from app.utils.data import update_collections
from config import (
    BAR_CHART_COLLECTION, BARCHART_DB_KEY, UPDATE_FMT, CP_DATAFILE_MONITOR
)

BARCHART_COLLECTION = mongo.db[BAR_CHART_COLLECTION]


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
    try:
        app.logger.info("Getting {} bcr from mongo".format(var_name))
        data = next(BARCHART_COLLECTION.find({BARCHART_DB_KEY: var_name}))
        data["ts"] = data["ts"].strftime(UPDATE_FMT)
        data["status"] = "ok"
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
    app.logger.warning("Received db update request")
    response = {"ts": dt.datetime.utcnow()}
    message = "nothing to update"
    do_update = False
    try:
        payload = request.json
        commits = payload.get("commits")
        if commits is not None:
            modified_files = []
            for c in commits:
                commit_modified_files = c.get("modified")
                if commit_modified_files is not None:
                    modified_files.extend(commit_modified_files)
            response["modified_files"] = modified_files
            app.logger.debug("Modified files: {}".format(modified_files))
            if any(CP_DATAFILE_MONITOR in _file for _file in modified_files):
                do_update = True
            if do_update:
                app.logger.warning("Start collections update")
                update_collections()
                message = "collections updated"
                app.logger.warning("Collections updated")
        response["status"] = "ok"
        response["message"] = message
    except Exception as e:
        app.logger.error("{}".format(e))
        response["status"] = "ko"
        response["message"] = "Error: {}".format(e)
    return jsonify(**response)
