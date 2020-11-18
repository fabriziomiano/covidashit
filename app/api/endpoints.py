from flask import jsonify, request, Response, current_app as app

from app.api import api
from app.db.update import (
    update_national_collections, update_regional_collections,
    update_provincial_collections
)
from app.plotter import Plotter, validate_plot_request


@api.route("/update/<coll>", methods=["POST"])
def update_db(coll):
    """
    Trigger db-collection updates
    :param coll: str
    :return: json str
    """
    response = {"status": "ok", "collections_updated": [], "errors": []}
    if coll == "national":
        response = update_national_collections(response)
    if coll == "regional":
        response = update_regional_collections(response)
    if coll == "provincial":
        response = update_provincial_collections(response)
    return jsonify(**response)


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
    app.logger.debug(f"QS Args: {request.args}")
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
