import time

from flask import render_template, redirect
from flask_babel import gettext

from config import REGIONS, PROVINCES, DATA_SERIES, VARS_CONFIG
from app.datatools import (
    parse_data, init_data, latest_update, get_national_data,
    get_regional_data, get_provincial_data, frontend_data, EXP_STATUS,
    get_regional_breakdown, get_latest_regional_data,
    get_latest_provincial_data, get_provincial_breakdown
)
from app.ui import dashboard


@dashboard.route("/national")
def old_national():
    return redirect('/')


@dashboard.route("/")
def national_view():
    covid_data = get_national_data()
    latest_regional_data = get_latest_regional_data()
    breakdown = get_regional_breakdown(latest_regional_data["latest_regional"])
    init_data()
    dates, series, trend_cards = parse_data(covid_data)
    updated_at = latest_update(covid_data["national"])
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
    breakdown = {}
    if territory in REGIONS:
        covid_data = get_regional_data()
        updated_at = latest_update(covid_data["regional"])
        latest_provincial_data = get_latest_provincial_data()
        breakdown = get_provincial_breakdown(
            latest_provincial_data["latest_provincial"], territory
        )
        print(breakdown)
    elif territory in PROVINCES:
        covid_data = get_provincial_data()
        updated_at = latest_update(covid_data["provincial"])
    else:
        return render_template("errors/404.html")
    init_data()
    dates, series, trend_cards = parse_data(covid_data, territory=territory)
    covid_data = frontend_data(
        ts=int(time.time()),
        navtitle=territory,
        territory=territory,
        dates=dates,
        series=series,
        trend_cards=trend_cards,
        latest_update=updated_at,
        data_series=DATA_SERIES,
        breakdown=breakdown,
        vars_config=VARS_CONFIG,
        scatterplot_series={
            "name": gettext("New Positive VS Total Cases"),
            "data": EXP_STATUS
        }
    )
    return render_template("dashboard.html", **covid_data)
