import datetime as dt
import time

from flask import render_template, redirect, Blueprint
from flask_babel import gettext

from config import (
    PHASE2_DAY, REOPENING_DAY, REGIONS, PROVINCES, ITEN_MAP, CUSTOM_CARDS
)
from covidashit.datatools import (
    EXP_STATUS, parse_data, init_data, latest_update, get_national_data,
    get_regional_data, get_provincial_data
)
DATA_SERIES = [
    ITEN_MAP[key]["title"]
    for key in ITEN_MAP
    if key not in CUSTOM_CARDS
]
dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/national")
def national():
    return redirect('/')


@dashboard.route("/")
def index():
    data = get_national_data()
    init_data()
    dates, series, trend_cards = parse_data(data)
    updated_at = latest_update(data["national"])
    scatterplot_series = {
        "name": gettext("New Positive VS Total Cases"),
        "data": EXP_STATUS
    }
    return render_template(
        "dashboard.html",
        dates=dates,
        trend_cards=trend_cards,
        regions=REGIONS,
        provinces=PROVINCES,
        series=series,
        ts=str(time.time()),
        days_since_phase2=(dt.datetime.today() - PHASE2_DAY).days,
        days_since_reopening=(dt.datetime.today() - REOPENING_DAY).days,
        latest_update=updated_at,
        scatterplot_series=scatterplot_series,
        data_series=DATA_SERIES
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
        return render_template("errors/404.html")
    init_data()
    dates, series, trend_cards = parse_data(data, territory=territory)
    scatterplot_series = {
        "name": gettext("New Positive VS Total Cases"),
        "data": EXP_STATUS
    }
    return render_template(
        "dashboard.html",
        navtitle=territory,
        dates=dates,
        trend_cards=trend_cards,
        territory=territory,
        provinces=PROVINCES,
        regions=REGIONS,
        series=series,
        ts=str(time.time()),
        days_since_phase2=(dt.datetime.today() - PHASE2_DAY).days,
        days_since_reopening=(dt.datetime.today() - REOPENING_DAY).days,
        latest_update=updated_at,
        scatterplot_series=scatterplot_series,
        data_series=DATA_SERIES
    )
