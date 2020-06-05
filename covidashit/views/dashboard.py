from flask import render_template, redirect, Blueprint

from config import (
    REGIONS, PROVINCES, ITEN_MAP, CUSTOM_CARDS
)
from covidashit.datatools import (
    parse_data, init_data, latest_update, get_national_data,
    get_regional_data, get_provincial_data, populate_data_to_frontend
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
def national_view():
    covid_data = get_national_data()
    init_data()
    dates, series, trend_cards = parse_data(covid_data)
    updated_at = latest_update(covid_data["national"])
    data = populate_data_to_frontend(
        dates, trend_cards, series, updated_at, DATA_SERIES
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
    data = populate_data_to_frontend(
        dates, trend_cards, series, updated_at, DATA_SERIES, territory
    )
    return render_template("dashboard.html", **data)
