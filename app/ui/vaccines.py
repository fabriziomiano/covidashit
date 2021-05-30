"""
Vaccines blueprint views
"""
import time

from flask import render_template
from flask_babel import gettext

from app.data_tools import (
    get_latest_vax_update, get_perc_pop_vax, enrich_frontend_data,
    get_tot_admins, get_admins_perc, get_vax_trends, get_area_population
)
from app.ui import vaccines
from settings import PAGE_BASE_TITLE, REGIONS, PC_TO_OD_MAP

URL_VACCINES = "/vaccines"
view_type = 'vaccines'


@vaccines.get('/')
def national_vax_view():
    """Render the vax report"""
    dashboard_title = gettext("Italy")
    page_title = f'{gettext("Vaccines")} | {PAGE_BASE_TITLE}'
    population = get_area_population('Italia')
    tot_admins = get_tot_admins(dtype='totale')
    perc_pop_vax = get_perc_pop_vax(population)
    report_data = enrich_frontend_data(
        page_title=page_title,
        view_type=view_type,
        dashboard_title=dashboard_title,
        ts=int(time.time()),
        latest_update=get_latest_vax_update(),
        tot_admins_str="{:,d}".format(tot_admins),
        tot_admins=tot_admins,
        admins_perc=get_admins_perc(),
        perc_pop_vax=perc_pop_vax,
        trends=get_vax_trends(),
        population="{:,d}".format(population)
    )
    return render_template("vaccines.html", **report_data)


@vaccines.get('/<region>')
def regional_vax_view(region):
    """Render the vax regional view"""
    dashboard_title = region
    page_title = f'{gettext("Vaccines")} | {region} | {PAGE_BASE_TITLE}'
    area = PC_TO_OD_MAP[region]
    population = get_area_population(region)
    tot_admins = get_tot_admins(dtype='totale', area=area)
    perc_pop_vax = get_perc_pop_vax(population, area)
    region_index = REGIONS.index(region)
    previous_url = f"{URL_VACCINES}/{REGIONS[region_index - 1]}"
    try:
        next_region_url = f"{URL_VACCINES}/{REGIONS[region_index + 1]}"
    except IndexError:
        next_region_url = f"{URL_VACCINES}/{REGIONS[-1]}"
    report_data = enrich_frontend_data(
        page_title=page_title,
        view_type=view_type,
        dashboard_title=dashboard_title,
        ts=int(time.time()),
        latest_update=get_latest_vax_update(),
        tot_admins_str="{:,d}".format(tot_admins),
        tot_admins=tot_admins,
        admins_perc=get_admins_perc(area=area),
        perc_pop_vax=perc_pop_vax,
        previous_area_url=previous_url,
        next_area_url=next_region_url,
        areas_length=len(REGIONS),
        area_index=region_index,
        area=region,
        trends=get_vax_trends(area),
        population="{:,d}".format(population)
    )
    return render_template("vaccines.html", **report_data)
