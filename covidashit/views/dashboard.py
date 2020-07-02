import datetime as dt

from flask import render_template, redirect, Blueprint
from flask_babel import gettext

from config import (
    REGIONS, PROVINCES, ITEN_MAP, CUSTOM_CARDS, BARCHART_RACE_QUERY,
    COLLECTION_NAME, UPDATE_FMT
)
from covidashit.datatools import (
    parse_data, init_data, latest_update, get_national_data,
    get_regional_data, get_provincial_data, frontend_data, EXP_STATUS
)

DATA_SERIES = [
    ITEN_MAP[key]["title"]
    for key in ITEN_MAP
    if key not in CUSTOM_CARDS
]
dashboard = Blueprint("dashboard", __name__)


def get_bcr_data():
    from covidashit import mongo
    bcr_data = mongo.db[COLLECTION_NAME].find(BARCHART_RACE_QUERY)[0]
    return bcr_data


@dashboard.route("/national")
def old_national():
    return redirect('/')


@dashboard.route("/")
def national_view():
    covid_data = get_national_data()
    init_data()
    dates, series, trend_cards = parse_data(covid_data)
    updated_at = latest_update(covid_data["national"])
    bcr_data = get_bcr_data()
    bcr_ts = bcr_data["ts"].strftime(UPDATE_FMT)
    bcr_html = bcr_data["html_str"]
    data = frontend_data(
        ts=dt.datetime.now(),
        dates=dates,
        trend_cards=trend_cards,
        series=series,
        latest_update=updated_at,
        data_series=DATA_SERIES,
        bcr_ts=bcr_ts,
        bcr_html=bcr_html,
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
    bcr_data = get_bcr_data()
    bcr_ts = bcr_data["ts"].strftime(UPDATE_FMT)
    bcr_html = bcr_data["html_str"]
    data = frontend_data(
        bcr_ts=bcr_ts,
        bcr_html=bcr_html,
        ts=dt.datetime.now(),
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
