"""
Pandemic blueprint views
"""
import time

from flask import redirect, render_template
from flask_babel import format_number, gettext

from app.data_tools import (
    enrich_frontend_data,
    get_area_population,
    get_latest_update,
    get_national_series,
    get_national_trends,
    get_notes,
    get_positivity_idx,
    get_provincial_breakdown,
    get_provincial_series,
    get_provincial_trends,
    get_regional_breakdown,
    get_regional_series,
    get_regional_trends,
)
from app.ui import pandemic
from app.utils import region_of_province
from settings import ITALY_MAP, PAGE_BASE_TITLE, PROVINCES, REGIONS

URL_REGIONS = "/regions"
URL_PROVINCES = "/provinces"


@pandemic.get("/national")
def old_national_view():
    """Redirect old national view to home"""
    return redirect("/")


@pandemic.get("/")
def national_view():
    """
    Render the national view
    :return: template
    """
    data_type = "national"
    cards = get_national_trends()
    breakdown = get_regional_breakdown()
    series = get_national_series()
    notes = get_notes(notes_type=data_type)
    updated_at = get_latest_update(data_type=data_type)
    positivity_idx = get_positivity_idx(area_type=data_type)
    population = get_area_population()
    data = enrich_frontend_data(
        page_title=PAGE_BASE_TITLE,
        dashboard_title=gettext("Italy"),
        ts=int(time.time()),
        trend_cards=cards,
        series=series,
        latest_update=updated_at,
        breakdown=breakdown,
        positivity_idx=positivity_idx,
        data_type=data_type,
        notes=notes,
        population=format_number(population),
    )
    return render_template("pandemic.html", **data)


@pandemic.get(f"{URL_REGIONS}/<region>")
def regional_view(region):
    """
    Render the regional view
    :param region: str: region
    :return: template
    """
    data_type = "regional"
    if region not in REGIONS:
        error = f"Area {region} not found"
        return render_template("errors/404.html", error=error)
    cards = get_regional_trends(region)
    breakdown = get_provincial_breakdown(region=region)
    series = get_regional_series(region=region)
    notes = get_notes(notes_type=data_type, area=region)
    latest_update = get_latest_update(data_type=data_type)
    positivity_idx = get_positivity_idx(area_type=data_type, area=region)
    provinces = ITALY_MAP[region]
    population = get_area_population(region)
    view_data = dict(
        ts=int(time.time()),
        page_title=f"{PAGE_BASE_TITLE} | {region}",
        dashboard_title=region,
        region=region,
        region_provinces=provinces,
        trend_cards=cards,
        breakdown=breakdown,
        positivity_idx=positivity_idx,
        series=series,
        notes=notes,
        latest_update=latest_update,
        data_type=data_type,
        cards=cards,
        population=format_number(population),
    )
    dashboard_data = enrich_frontend_data(area=region, **view_data)
    return render_template("pandemic.html", **dashboard_data)


@pandemic.get(f"{URL_PROVINCES}/<province>")
def provincial_view(province):
    """
    Render the provincial view
    :param province: str
    :return: template
    """
    data_type = "provincial"
    if province not in PROVINCES:
        error = f'Area "{province}" not found.'
        return render_template("errors/404.html", error=error)
    cards = get_provincial_trends(province=province)
    series = get_provincial_series(province=province)
    notes = get_notes(notes_type=data_type, area=province)
    latest_update = get_latest_update(data_type=data_type)
    region = region_of_province(province)
    region_provinces = ITALY_MAP[region]
    view_data = dict(
        ts=int(time.time()),
        page_title=f"{PAGE_BASE_TITLE} | {province}",
        dashboard_title=province,
        province=province,
        region=region,
        region_provinces=region_provinces,
        trend_cards=cards,
        series=series,
        notes=notes,
        latest_update=latest_update,
        data_type=data_type,
    )
    dashboard_data = enrich_frontend_data(area=province, **view_data)
    return render_template("pandemic.html", **dashboard_data)


@pandemic.get("/thanks")
def thanks_view():
    """
    Render the "thank you" view
    :return: HTML
    """
    return render_template("thanks.html")
