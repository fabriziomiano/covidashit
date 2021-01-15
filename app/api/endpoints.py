"""
API endpoints
"""
from flask import jsonify, request, Response, current_app as app
from flask_github_signature import verify_signature

from app.api import api
from app.db.update import (
    update_national_collection, update_national_series_collection,
    update_national_trends_collection, update_regional_collection,
    update_regional_series_collection, update_regional_trends_collection,
    update_regional_breakdown_collection, update_provincial_collection,
    update_provincial_breakdown_collection,
    update_provincial_series_or_trends_collection, update_vax_collection
)
from app.plotter import Plotter, validate_plot_request


@api.route("/plot")
def plot_trend():
    """
    API to make plot for a given data_type, varname, and area
    "varname" must always be specified, together with "data_type".
    If "data_type" is "national" no "area" is needed.
    As opposite, if "data_type" is "regional" or "provincial" an "area"
    must be specified.

    The specified "varname" must be one of the VARS keys for "national" and
    "regional" data types, and can only be "totale_casi" or
    "nuovi_positivi" for the "provincial" data type

    Example 1:
    GET /plot/varname=nuovi_positivi&data_type=provincial&area=Catania

    Example 2:
    GET /plot/varname=tamponi&data_type=regional&area=Sicilia

    :return:
        if 'download' in query string flask.Response object
        else JSON str, e.g.
        {
            "status": "ok",
            "errors": [],
            "img": "some_b64"
        }
    """
    response = {"status": "ko", "errors": []}
    status = 400
    varname = request.args.get("varname")
    data_type = request.args.get("data_type")
    area = request.args.get("area")
    download = request.args.get("download")
    is_valid, err = validate_plot_request(varname, data_type, area)
    if is_valid:
        try:
            p = Plotter(varname, data_type, area=area)
            if download:
                img_bytes = p.to_bytes()
                response = Response(img_bytes, mimetype="image/png")
            else:
                img = p.to_b64()
                response["img"] = img
                response["status"] = "ok"
                response = jsonify(**response)
            status = 200
        except Exception as e:
            app.logger.error(f"{e}")
            response["errors"].extend([f"{e}"])
            status = 400
    else:
        response["errors"].append(err)
    return response, status


@api.route("/update/national", methods=["POST"])
@verify_signature
def trigger_national_coll_update():
    """Trigger national collection update"""
    app.logger.warning("Triggered national data update")
    response = update_national_collection()
    return jsonify(**response)


@api.route("/update/national/series", methods=["POST"])
@verify_signature
def trigger_national_series_collection_update():
    """Trigger national series collection update"""
    app.logger.warning("Triggered national series update")
    response = update_national_series_collection()
    return jsonify(**response)


@api.route("/update/national/trends", methods=["POST"])
@verify_signature
def trigger_national_trends_collection_update():
    """Trigger national trends collection update"""
    app.logger.warning("Triggered national trends update")
    response = update_national_trends_collection()
    return jsonify(**response)


@api.route("/update/regional", methods=["POST"])
@verify_signature
def trigger_regional_collection_update():
    """Trigger regional-data collection update"""
    app.logger.warning("Triggered regional data update")
    response = update_regional_collection()
    return jsonify(**response)


@api.route("/update/regional/series", methods=["POST"])
@verify_signature
def trigger_regional_series_collection_update():
    """Trigger regional series collection update"""
    app.logger.warning("Triggered regional series update")
    response = update_regional_series_collection()
    return jsonify(**response)


@api.route("update/regional/trends", methods=["POST"])
def trigger_regional_trends_collection_update():
    """Trigger regional trends collection update"""
    app.logger.warning("Triggered regional trends update")
    response = update_regional_trends_collection()
    return jsonify(**response)


@api.route("update/regional/breakdown", methods=["POST"])
@verify_signature
def trigger_regional_breakdown_collection_update():
    """Trigger regional breakdown collection update"""
    app.logger.warning("Triggered regional breakdown update")
    response = update_regional_breakdown_collection()
    return jsonify(**response)


@api.route("update/provincial", methods=["POST"])
@verify_signature
def trigger_provincial_collection_update():
    """Trigger provincial data collection update"""
    app.logger.warning("Triggered provincial data update")
    response = update_provincial_collection()
    return jsonify(**response)


@api.route("/update/provincial/breakdown", methods=["POST"])
@verify_signature
def trigger_provincial_breakdown_collection_update():
    """Trigger provincial breakdown collection update"""
    app.logger.warning("Triggered provincial breakdown update")
    response = update_provincial_breakdown_collection()
    return jsonify(**response)


@api.route("/update/provincial/<coll_type>", methods=["POST"])
@verify_signature
def trigger_provincial_series_or_trends_collection_update(coll_type):
    """Trigger provincial series OR trends collections update"""
    app.logger.warning(f"Triggered provincial {coll_type} update")
    response = update_provincial_series_or_trends_collection(coll_type)
    return jsonify(**response)


@api.route("/update/vax", methods=["POST"])
@verify_signature
def trigger_vax_collection_update():
    """Trigger vax or vax summary collection update"""
    app.logger.warning(f"Triggered vax collection update")
    response = update_vax_collection()
    return jsonify(**response)


@api.route("/update/vax/summary", methods=["POST"])
@verify_signature
def trigger_vax_summary_collection_update():
    """Trigger vax or vax summary collection update"""
    app.logger.warning(f"Triggered vax collection update")
    response = update_vax_collection(summary=True)
    return jsonify(**response)
