"""
API endpoints
"""
from flask import Response
from flask import current_app as app
from flask import jsonify, request

from covidashit import limiter
from covidashit.api import api
from covidashit.data_tools import (
    get_admins_per_provider_chart_data,
    get_admins_per_region,
    get_admins_timeseries_chart_data,
    get_age_chart_data,
)
from covidashit.plotter import Plotter, validate_plot_request
from settings import REGIONS


@api.get("/plot")
@limiter.limit("20 per second")
def plot_trend():
    """
    API to make plot for a given data_type, varname, and area
    'varname' must always be specified, together with 'data_type'.
    If 'data_type' is 'national' no 'area' is needed.
    As opposite, if 'data_type' is 'regional' or 'provincial' an 'area'
    must be specified.

    The specified 'varname' must be one of the VARS keys for 'national' and
    'regional' data types, and can only be 'totale_casi' or
    'nuovi_positivi' for the 'provincial' data type

    Example 1:
    GET /plot/varname=nuovi_positivi&data_type=provincial&area=Catania

    Example 2:
    GET /plot/varname=tamponi&data_type=regional&area=Sicilia

    :return:
        if 'download' in query string flask.Response object
        else JSON str, e.g.
        {
            'status': 'ok',
            'errors': [],
            'img': 'some_b64'
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


@api.get("vax_charts/<chart_id>")
@limiter.limit("10 per second")
def get_chart(chart_id):
    """
    Return JSON-formatted data for a chart
    :param chart_id: str: must be one of
        ['trend', 'region', 'age', 'category', 'provider'].
        Additionally, an 'area' argument can be passed via query string for
        the types ['age', 'category', 'provider']
    :return: json-formatted string
    """
    args = request.args
    area = args.get("area")
    data_menu = {
        "trend": get_admins_timeseries_chart_data,
        "region": get_admins_per_region,
        "age": get_age_chart_data,
        "provider": get_admins_per_provider_chart_data,
    }
    data = {}
    try:
        get_data = data_menu[chart_id]
        if area in REGIONS:
            data = get_data(area=area)
        else:
            data = get_data()
    except Exception as e:
        app.logger.error(f"While calling charts API: {e}")
    return data
