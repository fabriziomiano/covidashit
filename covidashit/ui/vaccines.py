"""
Vaccines blueprint views
"""
import time

from flask import render_template
from flask_babel import format_number, gettext

from covidashit.data_tools import (
    enrich_frontend_data,
    get_admins_perc,
    get_area_population,
    get_latest_od_update_date,
    get_perc_pop_vax,
    get_vax_trends,
)
from covidashit.ui import vaccines
from settings import PAGE_BASE_TITLE, PC_TO_OD_MAP, REGIONS

URL_VACCINES = "/vaccines"
VIEW_TYPE = "vaccines"


@vaccines.get("/")
def national_vax_view():
    """Render the vax report"""
    dashboard_title = gettext("Italy")
    page_title = f'{PAGE_BASE_TITLE} | {gettext("Vaccines")}'
    population = get_area_population("Italia")
    perc_pop_vax = get_perc_pop_vax(population)
    report_data = enrich_frontend_data(
        page_title=page_title,
        view_type=VIEW_TYPE,
        dashboard_title=dashboard_title,
        ts=int(time.time()),
        latest_update=get_latest_od_update_date(),
        admins_perc=get_admins_perc(),
        perc_pop_vax=perc_pop_vax,
        trends=get_vax_trends(),
        population=format_number(population),
    )
    return render_template("vaccines.html", **report_data)


@vaccines.get("/<region>")
def regional_vax_view(region):
    """Render the vax regional view"""
    dashboard_title = region
    page_title = f'{PAGE_BASE_TITLE} | {gettext("Vaccines")} | {region}'
    area = PC_TO_OD_MAP[region]
    population = get_area_population(region)
    perc_pop_vax = get_perc_pop_vax(population, area)
    report_data = enrich_frontend_data(
        page_title=page_title,
        view_type=VIEW_TYPE,
        dashboard_title=dashboard_title,
        ts=int(time.time()),
        latest_update=get_latest_od_update_date(),
        admins_perc=get_admins_perc(area=area),
        perc_pop_vax=perc_pop_vax,
        areas_length=len(REGIONS),
        area=region,
        trends=get_vax_trends(area),
        population=format_number(population),
    )
    return render_template("vaccines.html", **report_data)
