import time

from flask import render_template, redirect
from flask_babel import gettext

from app.datatools import (
    parse_data, init_data, latest_update, get_national_data,
    get_regional_data, get_provincial_data, frontend_data, EXP_STATUS,
    get_regional_breakdown, get_latest_regional_data,
    get_latest_provincial_data, get_provincial_breakdown
)
from app.ui import dashboard
from config import REGIONS, PROVINCES, DATA_SERIES, VARS_CONFIG


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
        page_title=gettext("COVID-19 Italy"),
        dashboard_title=gettext("National Dashboard"),
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


@dashboard.route("/regions/<area>")
@dashboard.route("/provinces/<area>")
def regional_or_provincial_view(area):
    breakdown = {}
    if area in REGIONS:
        covid_data = get_regional_data()
        updated_at = latest_update(covid_data["regional"])
        latest_provincial_data = get_latest_provincial_data()
        breakdown = get_provincial_breakdown(
            latest_provincial_data["latest_provincial"], area
        )
    elif area in PROVINCES:
        covid_data = get_provincial_data()
        updated_at = latest_update(covid_data["provincial"])
    else:
        return render_template("errors/404.html")
    init_data()
    dates, series, trend_cards = parse_data(covid_data, area=area)
    data = frontend_data(
        ts=int(time.time()),
        page_title="{} | {}".format(area, gettext("COVID-19 Italy")),
        dashboard_title=area,
        area=area,
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
    return render_template("dashboard.html", **data)
