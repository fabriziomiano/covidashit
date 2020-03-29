import time
import json
import datetime as dt
from flask import render_template
from config import WEBSITE_TITLE, LOCKDOWN_DAY
from covidashit import app
from covidashit.dataset import init_data, parse_data, init_chart
from covidashit.routes import (
    server_error, get_national_data, get_regional_data,
    get_provincial_data
)


@app.route('/')
@app.route('/national')
def index(chart_id='chart_ID', chart_type='line'):
    response = get_regional_data()
    status = response.status_code
    if status != 200:
        app.logger.error("Could not get PCM data: {}".format(status))
        return server_error
    data = json.loads(response.data)
    response = get_national_data()
    status = response.status_code
    if status != 200:
        app.logger.error("Could not get PCM data: {}".format(status))
        return server_error
    data.update(json.loads(response.data))
    response = get_provincial_data()
    status = response.status_code
    if status != 200:
        app.logger.error("Could not get PCM data: {}".format(status))
        return server_error
    data.update(json.loads(response.data))
    app.logger.debug("Data processed {}".format(data))
    init_data()
    dates, series, trend, regions, provinces = parse_data(data)
    title = {"text": "Italy", "align": "left"}
    chart, x_axis, y_axis = init_chart(chart_id, chart_type, dates)
    return render_template(
        'dashboard.html',
        trend=trend,
        regions=regions,
        provinces=provinces,
        pagetitle=WEBSITE_TITLE,
        chartID=chart_id,
        chart=chart,
        series=series,
        title=title,
        xAxis=x_axis,
        yAxis=y_axis,
        ts=str(time.time()),
        lockdown_days=(dt.datetime.today()-LOCKDOWN_DAY).days
    )


@app.route('/regions/<string:region>')
def regional(region, chart_id='chart_ID', chart_type='line'):
    response = get_regional_data()
    status = response.status_code
    if status != 200:
        app.logger.error("Could not get PCM data: {}".format(status))
        return server_error
    data = json.loads(response.data)
    response = get_national_data()
    status = response.status_code
    if status != 200:
        app.logger.error("Could not get PCM data: {}".format(status))
        return server_error
    data.update(json.loads(response.data))
    response = get_provincial_data()
    status = response.status_code
    if status != 200:
        app.logger.error("Could not get PCM data: {}".format(status))
        return server_error
    data.update(json.loads(response.data))
    app.logger.debug("Data processed {}".format(data))
    init_data()
    dates, series, trend, regions, provinces = parse_data(data, region)
    title = {"text": region, "align": "left"}
    chart, x_axis, y_axis = init_chart(chart_id, chart_type, dates)
    return render_template(
        'dashboard.html',
        trend=trend,
        region=region,
        regions=regions,
        provinces=provinces,
        pagetitle=WEBSITE_TITLE,
        chartID=chart_id,
        chart=chart,
        series=series,
        title=title,
        xAxis=x_axis,
        yAxis=y_axis,
        ts=str(time.time()),
        lockdown_days=(dt.datetime.today()-LOCKDOWN_DAY).days
    )


@app.route('/provinces/<string:province>')
def provincial(province, chart_id='chart_ID', chart_type='line'):
    response = get_regional_data()
    status = response.status_code
    if status != 200:
        app.logger.error("Could not get PCM data: {}".format(status))
        return server_error
    data = json.loads(response.data)
    response = get_national_data()
    status = response.status_code
    if status != 200:
        app.logger.error("Could not get PCM data: {}".format(status))
        return server_error
    data.update(json.loads(response.data))
    response = get_provincial_data()
    status = response.status_code
    if status != 200:
        app.logger.error("Could not get PCM data: {}".format(status))
        return server_error
    data.update(json.loads(response.data))
    app.logger.debug("Data processed {}".format(data))
    init_data()
    dates, series, trend, regions, provinces = parse_data(data, province=province)
    title = {"text": province, "align": "left"}
    chart, x_axis, y_axis = init_chart(chart_id, chart_type, dates)
    return render_template(
        'dashboard.html',
        trend=trend,
        regions=regions,
        provinces=provinces,
        province=province,
        pagetitle=WEBSITE_TITLE,
        chartID=chart_id,
        chart=chart,
        series=series,
        title=title,
        xAxis=x_axis,
        yAxis=y_axis,
        ts=str(time.time()),
        lockdown_days=(dt.datetime.today()-LOCKDOWN_DAY).days
    )
