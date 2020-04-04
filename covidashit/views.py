import time
import json
import datetime as dt
from flask import render_template
from flask_babel import gettext
from config import WEBSITE_TITLE, LOCKDOWN_DAY
from covidashit import app
from covidashit.dataset import init_data, parse_data, init_chart
from covidashit.routes import (
    get_national_data, get_regional_data, get_provincial_data
)


@app.route('/')
@app.route('/regions/<string:region>')
@app.route('/provinces/<string:province>')
def provincial(region=None, province=None, chart_id='chart_ID', chart_type='line'):
    data = json.loads(get_provincial_data().data)
    data.update(json.loads(get_regional_data().data))
    data.update(json.loads(get_national_data().data))
    init_data()
    if province is not None:
        dates, series, trend, regions, provinces = parse_data(data, province=province)
        chart_title = {"text": province, "align": "left"}
    elif region is not None:
        dates, series, trend, regions, provinces = parse_data(data, region=region)
        chart_title = {"text": region, "align": "left"}
    else:
        dates, series, trend, regions, provinces = parse_data(data)
        chart_title = {"text": gettext("Italy"), "align": "left"}
    chart, x_axis, y_axis = init_chart(chart_id, chart_type, dates)
    latest_update = dates[-1]
    return render_template(
        'dashboard.html',
        trend=trend,
        regions=regions,
        region=region,
        provinces=provinces,
        province=province,
        pagetitle=gettext(WEBSITE_TITLE),
        chartID=chart_id,
        chart=chart,
        series=series,
        chart_title=chart_title,
        xAxis=x_axis,
        yAxis=y_axis,
        ts=str(time.time()),
        lockdown_days=(dt.datetime.today()-LOCKDOWN_DAY).days,
        latest_update=latest_update
    )
