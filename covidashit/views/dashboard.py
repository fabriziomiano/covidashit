import datetime as dt
import time

from flask import render_template, redirect, Blueprint
from flask_babel import gettext

from config import WEBSITE_TITLE, LOCKDOWN_DAY, REGIONS, PROVINCES
from covidashit.dataset import (
    init_data, parse_data, latest_update, EXP_STATUS,
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
    updated_at = latest_update(data["national"])
    scatterplot_series = {
        "name": gettext("New Positive VS Total Cases"),
        "data": EXP_STATUS
    }
    return render_template(
        "index.html",
        dates=dates,
        trend=trend,
        regions=REGIONS,
        provinces=PROVINCES,
        pagetitle=gettext(WEBSITE_TITLE),
        series=series,
        ts=str(time.time()),
        lockdown_days=(dt.datetime.today() - LOCKDOWN_DAY).days,
        latest_update=updated_at,
        scatterplot_series=scatterplot_series
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
    scatterplot_series = {
        "name": gettext("New Positive VS Total Cases"),
        "data": EXP_STATUS
    }
    return render_template(
        "index.html",
        dates=dates,
        trend=trend,
        territory=territory,
        provinces=PROVINCES,
        regions=REGIONS,
        pagetitle=gettext(WEBSITE_TITLE),
        series=series,
        ts=str(time.time()),
        lockdown_days=(dt.datetime.today() - LOCKDOWN_DAY).days,
        latest_update=updated_at,
        scatterplot_series=scatterplot_series
    )
