import time
from flask import render_template
from covidashit import app, get_data
PAGE_TITLE = "COVID-19 Italian trend"


@app.route('/')
@app.route('/national')
@app.route('/<string:region>')
def index(region=None, chart_id='chart_ID', chart_type='column'):
    app.logger.debug("Region {}".format(region))
    if region is None:
        dates, series, trend, regions = get_data()
        title = {"text": 'COVID-19 Italian trend', "align": "left"}
    else:
        title = {"text": region, "align": "left"}
        dates, series, trend, regions = get_data(region)
    app.logger.debug(regions)
    chart = {"renderTo": chart_id, "type": chart_type}
    x_axis = {"categories": dates}
    y_axis = {"title": {"text": '# of people'}, "type": "logarithmic"}
    return render_template(
        'index.html',
        regions=regions,
        trend=trend,
        pagetitle=PAGE_TITLE,
        chartID=chart_id,
        chart=chart,
        series=series,
        title=title,
        xAxis=x_axis,
        yAxis=y_axis,
        ts=str(time.time())
    )
