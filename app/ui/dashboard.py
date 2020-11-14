import time

from flask import render_template, redirect, current_app as app
from flask_babel import gettext

from app.ui import dashboard
from app.utils.data import (
    latest_update, enrich_frontend_data, get_regional_breakdown,
    get_notes, get_national_cards, get_national_series, get_positivity_idx,
    get_regional_cards, get_regional_series, get_provincial_breakdown,
    get_provincial_cards, get_provincial_series
)
from config import (
    DATA_SERIES, VARS, BCR_TYPES, REGIONS, PROVINCES, ITALY_MAP
)


def build_area_dashboard(area, area_index, area_length, cards, **kwargs):
    breakdown = kwargs.get("breakdown")
    series = kwargs.get("series")
    updated_at = kwargs.get("updated_at")
    notes = kwargs.get("notes")
    positivity_idx = kwargs.get("positivity_idx")
    app.logger.debug(
        "{} {} {}".format(area, area_index, area_length - 1))
    data = enrich_frontend_data(
        ts=int(time.time()),
        page_title="{} | {}".format(area, gettext("COVID-19 Italy")),
        dashboard_title=area,
        area=area,
        area_index=area_index,
        areas_length=area_length,
        series=series,
        trend_cards=cards,
        latest_update=updated_at,
        data_series=DATA_SERIES,
        breakdown=breakdown,
        vars_config=VARS,
        bcr_types=BCR_TYPES,
        positivity_idx=positivity_idx,
        italy_map=ITALY_MAP,
        notes=notes)
    return render_template("dashboard.html", **data)


@dashboard.route("/national")
def old_national_view():
    return redirect('/')


@dashboard.route("/")
def new_national():
    cards = get_national_cards()
    app.logger.debug(f"Cards: {cards}")
    breakdown = get_regional_breakdown()
    series = get_national_series()
    notes = get_notes(notes_type="national")
    updated_at = latest_update(data_type="national")
    positivity_idx = get_positivity_idx(area_type="national")
    data = enrich_frontend_data(
        page_title=gettext("COVID-19 Italy"),
        dashboard_title=gettext("National Dashboard"),
        ts=int(time.time()),
        trend_cards=cards,
        series=series,
        latest_update=updated_at,
        data_series=DATA_SERIES,
        breakdown=breakdown,
        vars_config=VARS,
        bcr_types=BCR_TYPES,
        positivity_idx=positivity_idx,
        italy_map=ITALY_MAP,
        notes=notes)
    return render_template("dashboard.html", **data)


@dashboard.route("/regions/<region>")
def regional_view(region):
    """
    Render the regional view
    :param region: str: region
    :return: template
    """
    if region not in REGIONS:
        error = f'Area {region} not found'
        return render_template("errors/404.html", error=error)
    cards = get_regional_cards(region)
    app.logger.debug(f"Cards: {cards}")
    breakdown = get_provincial_breakdown(region=region)
    series = get_regional_series(region=region)
    notes = get_notes(notes_type="regional", area=region)
    updated_at = latest_update(data_type="regional")
    positivity_idx = get_positivity_idx(area_type="regional", area=region)
    region_index = REGIONS.index(region)
    n_regions = len(REGIONS)
    view_data = dict(
        breakdown=breakdown,
        positivity_idx=positivity_idx,
        series=series,
        notes=notes,
        updated_at=updated_at
    )
    return build_area_dashboard(
        region, region_index, n_regions, cards, **view_data)


@dashboard.route("/provinces/<province>")
def provincial_view(province):
    """
    Render the provincial view
    :param province: str
    :return: template
    """
    if province not in PROVINCES:
        error = (
            'Area "{}" not found. '
            'Please try with "{}"'.format(province, province.capitalize()))
        return render_template("errors/404.html", error=error)
    cards = get_provincial_cards(province=province)
    app.logger.debug(f"Cards: {cards}")
    series = get_provincial_series(province=province)
    notes = get_notes(notes_type="provincial", area=province)
    updated_at = latest_update(data_type="provincial")
    province_index = PROVINCES.index(province)
    n_provinces = len(PROVINCES)
    view_data = dict(
        series=series,
        notes=notes,
        updated_at=updated_at
    )
    return build_area_dashboard(
        province, province_index, n_provinces, cards, **view_data)
