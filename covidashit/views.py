import datetime as dt
import json
import time

from flask import render_template
from flask_babel import gettext

from config import (
    WEBSITE_TITLE, LOCKDOWN_DAY, CHART_TYPE, CHART_ID, REGIONS, PROVINCES
)
from covidashit import app
from covidashit.dataset import init_data, parse_data, init_chart, latest_update
from covidashit.routes import (
    get_national_data, get_regional_data, get_provincial_data
)


@app.route("/")
def national():
    data = json.loads(get_national_data().data)
    init_data()
    dates, series, trend = parse_data(data)
    chart_title = {"text": gettext("Italy"), "align": "left"}
    updated_at = latest_update(data["national"])
    chart, x_axis, y_axis = init_chart(CHART_ID, CHART_TYPE, dates)
    return render_template(
        "dashboard.html",
        trend=trend,
        regions=REGIONS,
        provinces=PROVINCES,
        pagetitle=gettext(WEBSITE_TITLE),
        chartID=CHART_ID,
        chart=chart,
        series=series,
        chart_title=chart_title,
        xAxis=x_axis,
        yAxis=y_axis,
        ts=str(time.time()),
        lockdown_days=(dt.datetime.today() - LOCKDOWN_DAY).days,
        latest_update=updated_at
    )


@app.route("/regions/<string:territory>")
@app.route("/provinces/<string:territory>")
def provincial(territory):
    if territory in REGIONS:
        data = json.loads(get_regional_data().data)
        updated_at = latest_update(data["regional"])
    elif territory in PROVINCES:
        data = json.loads(get_provincial_data().data)
        updated_at = latest_update(data["provincial"])
    else:
        return render_template("404.html", pagetitle=WEBSITE_TITLE)
    init_data()
    dates, series, trend = parse_data(data, territory=territory)
    chart_title = {"text": territory, "align": "left"}
    chart, x_axis, y_axis = init_chart(CHART_ID, CHART_TYPE, dates)
    return render_template(
        "dashboard.html",
        trend=trend,
        territory=territory,
        provinces=PROVINCES,
        regions=REGIONS,
        pagetitle=gettext(WEBSITE_TITLE),
        chartID=CHART_ID,
        chart=chart,
        series=series,
        chart_title=chart_title,
        xAxis=x_axis,
        yAxis=y_axis,
        ts=str(time.time()),
        lockdown_days=(dt.datetime.today()-LOCKDOWN_DAY).days,
        latest_update=updated_at
    )
