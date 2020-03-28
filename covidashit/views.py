import time
import json
from flask import render_template
from config import WEBSITE_TITLE
from covidashit.dataset import init_data, parse_data, init_chart
from covidashit import app
from covidashit.routes import (
    server_error, get_national_data, get_regional_data
)


@app.route('/')
@app.route('/national')
def national(chart_id='chart_ID', chart_type='column'):
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
    app.logger.debug("Data processed {}".format(data))
    init_data()
    dates, series, trend, regions = parse_data(data)
    title = {"text": "COVID-19 Trend | Italy", "align": "left"}
    chart, x_axis, y_axis = init_chart(chart_id, chart_type, dates)
    return render_template(
        'dashboard.html',
        trend=trend,
        regions=regions,
        pagetitle=WEBSITE_TITLE,
        chartID=chart_id,
        chart=chart,
        series=series,
        title=title,
        xAxis=x_axis,
        yAxis=y_axis,
        ts=str(time.time())
    )


@app.route('/regional/<string:region>')
def regional(region, chart_id='chart_ID', chart_type='column'):
    """
    Render /<region> route
    :param region:
    :param chart_id: str, optional
    :param chart_type: str, optional
    :return:
    """
    response = get_regional_data()
    status = response.status_code
    if status != 200:
        app.logger.error("Could not get PCM data: {}".format(status))
        return server_error
    data = json.loads(response.data)
    init_data()
    dates, series, trend, regions = parse_data(data, region)
    title = {"text": "COVID-19 Trend | " + region, "align": "left"}
    chart, x_axis, y_axis = init_chart(chart_id, chart_type, dates)
    return render_template(
        'dashboard.html',
        trend=trend,
        region=region,
        regions=regions,
        pagetitle=WEBSITE_TITLE,
        chartID=chart_id,
        chart=chart,
        series=series,
        title=title,
        xAxis=x_axis,
        yAxis=y_axis,
        ts=str(time.time())
    )
