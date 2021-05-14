"""
API endpoints
"""
from flask import jsonify, request, Response, current_app as app
from flask_github_signature import verify_signature

from app import limiter
from app.api import api
from app.data import (
    get_admins_timeseries_chart_data, get_region_chart_data,
    get_age_chart_data, get_category_chart_data,
    get_admins_per_provider_chart_data
)
from app.db_utils.tasks import (
    update_national_collection, update_national_series_collection,
    update_national_trends_collection, update_regional_collection,
    update_regional_series_collection, update_regional_trends_collection,
    update_regional_breakdown_collection, update_provincial_collection,
    update_provincial_breakdown_collection,
    update_provincial_series_or_trends_collection, update_vax_collections
)
from app.plotter import Plotter, validate_plot_request
from settings import REGIONS


@api.route('/plot')
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
    response = {'status': 'ko', 'errors': []}
    status = 400
    varname = request.args.get('varname')
    data_type = request.args.get('data_type')
    area = request.args.get('area')
    download = request.args.get('download')
    is_valid, err = validate_plot_request(varname, data_type, area)
    if is_valid:
        try:
            p = Plotter(varname, data_type, area=area)
            if download:
                img_bytes = p.to_bytes()
                response = Response(img_bytes, mimetype='image/png')
            else:
                img = p.to_b64()
                response['img'] = img
                response['status'] = 'ok'
                response = jsonify(**response)
            status = 200
        except Exception as e:
            app.logger.error(f'{e}')
            response['errors'].extend([f'{e}'])
            status = 400
    else:
        response['errors'].append(err)
    return response, status


update_menu = {
    'national': {
        'root': {
            'task': update_national_collection,
            'args': None
        },
        'series': {
            'task': update_national_series_collection,
            'args': None
        },
        'trends': {
            'task': update_national_trends_collection,
            'args': None
        }
    },
    'regional': {
        'root': {
            'task': update_regional_collection,
            'args': None
        },
        'breakdown': {
            'task': update_regional_breakdown_collection,
            'args': None
        },
        'series': {
            'task': update_regional_series_collection,
            'args': None
        },
        'trends': {
            'task': update_regional_trends_collection,
            'args': None
        }
    },
    'provincial': {
        'root': {
            'task': update_provincial_collection,
            'args': None
        },
        'breakdown': {
            'task': update_provincial_breakdown_collection,
            'args': None
        },
        'series': {
            'task': update_provincial_series_or_trends_collection,
            'args': 'series'
        },
        'trends': {
            'task': update_provincial_series_or_trends_collection,
            'args': 'trends'
        }
    },
    'vax': {
        'root': {
            'task': update_vax_collections,
            'args': None
        },
        'summary': {
            'task': update_vax_collections,
            'args': True
        }
    }
}


@api.route('/update/<data_type>', methods=['POST'])
@api.route('/update/<data_type>/<coll_type>', methods=['POST'])
@verify_signature
def update_collection(data_type, coll_type='root'):
    """Trigger collection update task"""
    app.logger.warning(f'Triggered {data_type} {coll_type} data update')
    status = 'ko'
    try:
        task_to_exec = update_menu[data_type][coll_type]['task']
        args = update_menu[data_type][coll_type]['args']
        if args:
            task = task_to_exec.apply_async(args=[args])
        else:
            task = task_to_exec.delay()
        msg = f'Task {task.id} submitted. Status {task.state}'
        app.logger.warning(msg)
        status = 'ok'
    except Exception as e:
        msg = f'While submitting {data_type} {coll_type} update task: {e}'
        app.logger.error(msg)
    return {'status': status, 'msg': msg}


@api.route('vax_charts/<chart_id>')
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
    area = args.get('area')
    data_menu = {
        'trend': get_admins_timeseries_chart_data,
        'region': get_region_chart_data,
        'age': get_age_chart_data,
        'category': get_category_chart_data,
        'provider': get_admins_per_provider_chart_data
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
