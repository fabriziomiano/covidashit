import time

from flask import render_template, redirect
from flask_babel import gettext

from config import REGIONS, PROVINCES, DATA_SERIES, VARS_CONFIG
from app.datatools import (
    parse_data, init_data, latest_update, get_national_data,
    get_regional_data, get_provincial_data, frontend_data, EXP_STATUS,
    get_regional_breakdown, get_latest_regional_data
)
from app.ui import dashboard


@dashboard.route("/national")
def old_national():
    return redirect('/')


@dashboard.route("/")
def national_view():
    national_covid_data = get_national_data()
    latest_regional_data = get_latest_regional_data()
    breakdown = get_regional_breakdown(latest_regional_data["regional_latest"])
    init_data()
    dates, series, trend_cards = parse_data(national_covid_data)
    updated_at = latest_update(national_covid_data["national"])
    data = frontend_data(
        ts=int(time.time()),
        dates=dates,
        trend_cards=trend_cards,
        series=series,
        latest_update=updated_at,
        data_series=DATA_SERIES,
        breakdown=breakdown,
        vars_config=VARS_CONFIG,
        scatterplot_series={
            "name": gettext("New Positive VS Total Cases"),
            "data": EXP_STATUS
        }
    )
    return render_template("dashboard.html", **data)


@dashboard.route("/regions/<string:territory>")
@dashboard.route("/provinces/<string:territory>")
def regional_or_provincial_view(territory):
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
    data = frontend_data(
        ts=int(time.time()),
        navtitle=territory,
        territory=territory,
        dates=dates,
        series=series,
        trend_cards=trend_cards,
        latest_update=updated_at,
        data_series=DATA_SERIES,
        scatterplot_series={
            "name": gettext("New Positive VS Total Cases"),
            "data": EXP_STATUS
        }
    )
    return render_template("dashboard.html", **data)
