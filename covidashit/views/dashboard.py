import datetime as dt
import time

from flask import render_template, redirect, Blueprint
from flask_babel import gettext

from config import (
    WEBSITE_TITLE, LOCKDOWN_DAY, REGIONS, PROVINCES, SCATTER_TITLE, CREDITS,
    SCATTER_XAXIS, SCATTER_YAXIS, SOURCE_SUBTITLE
)
from covidashit.dataset import (
    init_data, parse_data, init_chart, latest_update, EXP_STATUS,
    get_national_data, get_regional_data, get_provincial_data
)

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/national")
def national():
    return redirect('/')


@dashboard.route("/")
def index():
    data = get_national_data()
    init_data()
    dates, series, trend = parse_data(data)
    chart_title = {"text": gettext("Italy"), "align": "left"}
    updated_at = latest_update(data["national"])
    x_axis, y_axis = init_chart(dates)
    scatterplot_series = {
        "name": gettext("New Positive VS Total Cases"),
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


@dashboard.route("/regions/<string:territory>")
@dashboard.route("/provinces/<string:territory>")
def provincial(territory):
    if territory in REGIONS:
        data = get_regional_data()
        updated_at = latest_update(data["regional"])
    elif territory in PROVINCES:
        data = get_provincial_data()
        updated_at = latest_update(data["provincial"])
    else:
        return render_template("404.html", pagetitle=WEBSITE_TITLE)
    init_data()
    dates, series, trend = parse_data(data, territory=territory)
    chart_title = {"text": territory, "align": "left"}
    scatterplot_series = {
        "name": gettext("New Positive VS Total Cases"),
        "data": EXP_STATUS
    }
    x_axis, y_axis = init_chart(dates)
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
        lockdown_days=(dt.datetime.today() - LOCKDOWN_DAY).days,
        latest_update=updated_at,
        scatterplot_series=scatterplot_series,
        scatter_title=SCATTER_TITLE,
        credits_data=CREDITS,
        scatter_xaxis=SCATTER_XAXIS,
        scatter_yaxis=SCATTER_YAXIS,
        source_subtitle=SOURCE_SUBTITLE
    )
