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
    :return: template
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


@dashboard.route("/regions/<area>")
def regional_view(area):
    """
    Render the regional view
    :param area: str: region
    :return: template
    """
    if area not in REGIONS:
        error = (
            'Area "{}" not found. '
            'Please try with "{}"'.format(area, area.capitalize()))
        return render_template("errors/404.html", error=error)
    init_data()
    regional_data = get_covid_data(
        data_type="regional", query_type="area", area=area)
    latest_provincial_data = get_covid_data(
        data_type="provincial", query_type="latest")
    breakdown = get_provincial_breakdown(latest_provincial_data, area)
    covid_data = regional_data
    area_index = REGIONS.index(area)
    positive_swabs_percentage = get_positive_swabs_percentage(
        covid_data, area=area)
    view_data = dict(
        breakdown=breakdown,
        positive_swabs_percentage=positive_swabs_percentage
    )
    return build_area_dashboard(area, area_index, covid_data, **view_data)


@dashboard.route("/provinces/<area>")
def provincial_view(area):
    """
    Render the provincial view
    :param area: str
    :return: template
    """
    if area not in PROVINCES:
        error = (
            'Area "{}" not found. '
            'Please try with "{}"'.format(area, area.capitalize()))
        return render_template("errors/404.html", error=error)
    init_data()
    provincial_data = get_covid_data(
        data_type="provincial", query_type="area", area=area)
    covid_data = provincial_data
    area_index = PROVINCES.index(area)
    return build_area_dashboard(area, area_index, covid_data)


def build_area_dashboard(area, area_index, covid_data, **kwargs):
    breakdown = kwargs.get("breakdown")
    positive_swabs_percentage = kwargs.get("positive_swabs_percentage")
    app.logger.debug(
        "{} {} {}".format(area, area_index, len(REGIONS) - 1))
    updated_at = latest_update(covid_data)
    dates, series, trend_cards = parse_area_data(covid_data, area)
    notes = get_notes(covid_data, area=area)
    data = enrich_frontend_data(
        ts=int(time.time()),
        page_title="{} | {}".format(area, gettext("COVID-19 Italy")),
        dashboard_title=area,
        area=area,
        area_index=area_index,
        areas_length=len(REGIONS),
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
    return render_template("dashboard.html", **data)
