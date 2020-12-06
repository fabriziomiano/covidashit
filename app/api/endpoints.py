"""
API endpoints
"""
from flask import jsonify, request, Response, current_app as app
from flask_github_signature import verify_signature

from app.api import api
from app.db.recovery import (
    create_national_collection, create_national_series_collection,
    create_national_trends_collection, create_regional_collection,
    create_regional_breakdown_collection, create_regional_series_collection,
    create_regional_trends_collection, create_provincial_collections,
    create_provincial_breakdown_collection,
    create_provincial_series_collection, create_provincial_trends_collection
)
from app.db.update import (
    update_national_collection, update_national_series_collection,
    update_national_trends_collection, update_regional_collection,
    update_regional_series_collection, update_regional_trends_collection,
    update_regional_breakdown_collection, update_provincial_collection,
    update_provincial_breakdown_collection,
    update_provincial_series_or_trends_collection
)
from app.plotter import Plotter, validate_plot_request
from app.utils import apikey_required


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


@api.route("/recovery/national", methods=["PUT"])
@apikey_required
def trigger_national_collection_creation():
    """Trigger national collection drop and recreation"""
    app.logger.warning("Triggered national collections recovery")
    response, status = create_national_collection()
    return jsonify(**response), status


@api.route("/recovery/national/<coll_type>", methods=["PUT"])
@apikey_required
def trigger_national_type_collection_creation(coll_type):
    """Trigger national-type collection drop and recreation"""
    creation_menu = {
        "series": create_national_series_collection(),
        "trends": create_national_trends_collection()
    }
    if coll_type not in creation_menu:
        return jsonify({"errors": "Invalid collection type"}), 400
    app.logger.warning(f"Triggered national {coll_type} collections recovery")
    response, status = create_national_series_collection()
    return jsonify(**response), status


@api.route("/recovery/regional", methods=["PUT"])
@apikey_required
def trigger_regional_collection_creation():
    """Trigger regional collection drop and recreation"""
    app.logger.warning("Triggered regional collections recovery")
    response, status = create_regional_collection()
    return jsonify(**response), status


@api.route("/recovery/regional/<coll_type>", methods=["PUT"])
@apikey_required
def trigger_regional_type_collection_creation(coll_type):
    """Trigger regional-type collection drop and creation"""
    creation_menu = {
        "breakdown": create_regional_breakdown_collection(),
        "series": create_regional_series_collection(),
        "trends": create_regional_trends_collection()
    }
    if coll_type not in creation_menu:
        return jsonify({"errors": "Invalid collection type"}), 400
    app.logger.warning(f"Triggered regional {coll_type} collections recovery")
    response, status = creation_menu[coll_type]
    return jsonify(**response), status


@api.route("/recovery/provincial", methods=["PUT"])
@apikey_required
def trigger_provincial_collection_creation():
    """Trigger provincial collection drop and recreation"""
    app.logger.warning("Triggered provincial collections recovery")
    response, status = create_provincial_collections()
    return jsonify(**response), status


@api.route("/recovery/provincial/<coll_type>", methods=["PUT"])
@apikey_required
def trigger_provincial_type_collection_creation(coll_type):
    """Trigger provincial-type collection drop and creation"""
    creation_menu = {
        "breakdown": create_provincial_breakdown_collection(),
        "series": create_provincial_series_collection(),
        "trends": create_provincial_trends_collection()
    }
    if coll_type not in creation_menu:
        return jsonify({"errors": "Invalid collection type"}), 400
    msg = f"Triggered provincial {coll_type} collections recovery"
    app.logger.warning(msg)
    response, status = creation_menu[coll_type]
    return jsonify(**response), status


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
