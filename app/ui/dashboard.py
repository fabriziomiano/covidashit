import time

from flask import render_template, redirect, current_app as app
from flask_babel import gettext

from app.utils.data import (
    EXP_STATUS, parse_national_data, parse_area_data,
    init_data, latest_update, get_covid_data, enrich_frontend_data,
    get_regional_breakdown, get_provincial_breakdown,
    get_positive_swabs_percentage, get_notes
)
from app.ui import dashboard
from config import (
    DATA_SERIES, VARS_CONFIG, BCR_TYPES, REGIONS, PROVINCES, ITALY_MAP
)

SCATTERPLOT_SERIES = {
    "name": gettext("New Positive VS Total Cases"),
    "data": EXP_STATUS
}


@dashboard.route("/national")
def old_national_view():
    return redirect('/')


@dashboard.route("/")
def national_view():
    """
    Render the national view
    :return: flask.render_template
    """
    national_data = get_covid_data(data_type="national", query_type="full")
    latest_regional_data = get_covid_data(
        data_type="regional", query_type="latest")
    breakdown = get_regional_breakdown(latest_regional_data)
    init_data()
    dates, series, trend_cards = parse_national_data(national_data)
    updated_at = latest_update(national_data)
    positive_swabs_percentage = get_positive_swabs_percentage(national_data)
    notes = get_notes([national_data[-1]])
    data = enrich_frontend_data(
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
        bcr_types=BCR_TYPES,
        scatterplot_series=SCATTERPLOT_SERIES,
        positive_swabs_percentage=positive_swabs_percentage,
        italy_map=ITALY_MAP,
        notes=notes)
    return render_template("dashboard.html", **data)


@dashboard.route("/<areas>/<area>")
def area_view(areas, area):
    """
    Render the areas/sub_area views, e.g. /regions/Sicilia
    :param areas: str
    :param area: str
    :return: flask.render_template
    """
    init_data()
    breakdown = {}
    positive_swabs_percentage = None
    try:
        if any(area in region for region in REGIONS):
            assert areas == "regions"
            areas = REGIONS
            regional_data = get_covid_data(
                data_type="regional", query_type="area", area=area)
            latest_provincial_data = get_covid_data(
                data_type="provincial", query_type="latest")
            breakdown = get_provincial_breakdown(latest_provincial_data, area)
            covid_data = regional_data
            area_index = REGIONS.index(area)
            positive_swabs_percentage = get_positive_swabs_percentage(
                covid_data, area=area)
        elif any(area in province for province in PROVINCES):
            assert areas == "provinces"
            areas = PROVINCES
            provincial_data = get_covid_data(
                data_type="provincial", query_type="area", area=area)
            covid_data = provincial_data
            area_index = PROVINCES.index(area)
        else:
            raise AssertionError
        app.logger.debug(
            "{} {} {}".format(area, area_index, len(areas)-1))
        updated_at = latest_update(covid_data)
        dates, series, trend_cards = parse_area_data(covid_data, area)
        notes = get_notes(covid_data, area=area)
        data = enrich_frontend_data(
            ts=int(time.time()),
            page_title="{} | {}".format(area, gettext("COVID-19 Italy")),
            dashboard_title=area,
            area=area,
            area_index=area_index,
            areas_length=len(areas),
            dates=dates,
            series=series,
            trend_cards=trend_cards,
            latest_update=updated_at,
            data_series=DATA_SERIES,
            breakdown=breakdown,
            vars_config=VARS_CONFIG,
            bcr_types=BCR_TYPES,
            scatterplot_series=SCATTERPLOT_SERIES,
            positive_swabs_percentage=positive_swabs_percentage,
            italy_map=ITALY_MAP,
            notes=notes)
        template, status_code = render_template("dashboard.html", **data), 200
    except AssertionError:
        err_log_msg = "{}/{} is not a valid pattern".format(areas, area)
        app.logger.error(err_log_msg)
        template = render_template("errors/404.html")
        status_code = 400
    return template, status_code
