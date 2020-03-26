import time
from flask import render_template, abort
from config import REGIONS, WEBSITE_TITLE
from covidashit import app, get_data


@app.errorhandler(404)
def page_not_found(e):
    app.logger.error("Error {}".format(e))
    return render_template("404.html", title=WEBSITE_TITLE), 404


@app.errorhandler(500)
def page_not_found(e):
    app.logger.error("Error {}".format(e))
    return render_template("500.html", title=WEBSITE_TITLE), 500


@app.route('/')
@app.route('/national')
@app.route('/<string:region>')
def index(region=None, chart_id='chart_ID', chart_type='column'):
    app.logger.debug("Region {}".format(region))
    if region is None:
        dates, series, trend = get_data()
        title = {"text": "COVID-19 Trend | Italy", "align": "left"}
    else:
        if region not in REGIONS:
            abort(404)
        title = {"text": "COVID-19 Trend | " + region, "align": "left"}
        dates, series, trend = get_data(region)
    chart = {"renderTo": chart_id, "type": chart_type}
    x_axis = {"categories": dates}
    y_axis = {"title": {"text": '# of people'}}
    return render_template(
        'index.html',
        region=region,
        regions=REGIONS,
        trend=trend,
        pagetitle=WEBSITE_TITLE,
        chartID=chart_id,
        chart=chart,
        series=series,
        title=title,
        xAxis=x_axis,
        yAxis=y_axis,
        ts=str(time.time())
    )
