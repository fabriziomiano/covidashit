import datetime as dt
import json
import time

from flask import render_template, redirect
from flask_babel import gettext

from config import (
    WEBSITE_TITLE, LOCKDOWN_DAY, REGIONS, PROVINCES, SCATTER_TITLE, CREDITS,
    SCATTER_XAXIS, SCATTER_YAXIS, SOURCE_SUBTITLE
)
from covidashit import app
from covidashit.dataset import (
    init_data, parse_data, init_chart, latest_update, EXP_STATUS
)
from covidashit.routes import (
    get_national_data, get_regional_data, get_provincial_data
)


@app.route("/national")
def national():
    return redirect('/')


@app.route("/")
def index():
    data = json.loads(get_national_data().data)
    init_data()
    dates, series, trend = parse_data(data)
    chart_title = {"text": gettext("Italy"), "align": "left"}
    updated_at = latest_update(data["national"])
    x_axis, y_axis = init_chart(dates)
    SCATTER_TITLE["text"] = gettext(SCATTER_TITLE["text"])
    scatterplot_series = {
        "name": gettext(SCATTER_TITLE["text"]),
        "data": EXP_STATUS
    }
    CREDITS["text"] = gettext(CREDITS["text"])
    SOURCE_SUBTITLE["text"] = gettext(SOURCE_SUBTITLE["text"])
    SCATTER_XAXIS["title"]["text"] = gettext(SCATTER_XAXIS["title"]["text"])
    SCATTER_YAXIS["title"]["text"] = gettext(SCATTER_YAXIS["title"]["text"])
    return render_template(
        "index.html",
        trend=trend,
        regions=REGIONS,
        provinces=PROVINCES,
        pagetitle=gettext(WEBSITE_TITLE),
        series=series,
        chart_title=chart_title,
        xAxis=x_axis,
        yAxis=y_axis,
        ts=str(time.time()),
        lockdown_days=(dt.datetime.today() - LOCKDOWN_DAY).days,
        latest_update=updated_at,
        scatterplot_series=scatterplot_series,
        scatter_title=SCATTER_TITLE,
        credits_data=CREDITS,
        scatter_xaxis=SCATTER_XAXIS,
        scatter_yaxis=SCATTER_YAXIS,
        source_subtitle=SOURCE_SUBTITLE
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
    x_axis, y_axis = init_chart(dates)
    scatterplot_series = {
        "name": gettext(SCATTER_TITLE["text"]),
        "data": EXP_STATUS
    }
    CREDITS["text"] = gettext(CREDITS["text"])
    return render_template(
        "index.html",
        trend=trend,
        territory=territory,
        provinces=PROVINCES,
        regions=REGIONS,
        pagetitle=gettext(WEBSITE_TITLE),
        series=series,
        chart_title=chart_title,
        xAxis=x_axis,
        yAxis=y_axis,
        ts=str(time.time()),
        lockdown_days=(dt.datetime.today()-LOCKDOWN_DAY).days,
        latest_update=updated_at,
        scatterplot_series=scatterplot_series,
        scatter_title=SCATTER_TITLE,
        credits_data=CREDITS,
        scatter_xaxis=SCATTER_XAXIS,
        scatter_yaxis=SCATTER_YAXIS,
        source_subtitle=SOURCE_SUBTITLE
    )
