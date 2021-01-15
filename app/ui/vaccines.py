"""
Vaccines blueprint views
"""
import time

from flask import render_template
from flask_babel import gettext

from app.data import (
    enrich_frontend_data, get_latest_vax_update, get_total_administrations,
    get_age_chart_data, get_category_chart_data, get_region_chart_data,
    get_perc_pop_vax
)
from app.ui import vaccines
from config import PAGE_BASE_TITLE, ITALY_POPULATION, PC_TO_OD_MAP, REGIONS

URL_VACCINES = "/vaccines"
view_type = 'vaccines'


@vaccines.route('/')
def national_vax_view():
    """Render the vax report"""
    area = 'ITA'
    dashboard_title = gettext("Italy")
    page_title = f'{gettext("Vaccines")} | {PAGE_BASE_TITLE}'
    population = ITALY_POPULATION['Italia']
    tot_admins = get_total_administrations(area=area)
    perc_pop_vax = get_perc_pop_vax(tot_admins, population)
    report_data = enrich_frontend_data(
        page_title=page_title,
        view_type=view_type,
        dashboard_title=dashboard_title,
        ts=int(time.time()),
        latest_update=get_latest_vax_update(),
        tot_admins_str="{:,d}".format(tot_admins),
        tot_admins=tot_admins,
        perc_pop_vax=f"{perc_pop_vax}%",
        age_chart_data=get_age_chart_data(),
        cat_chart_data=get_category_chart_data(area=area),
        region_chart_data=get_region_chart_data()
    )
    return render_template("vaccines.html", **report_data)


@vaccines.route('/<region>')
def regional_vax_view(region):
    """Render the vax regional view"""
    dashboard_title = region
    page_title = f'{gettext("Vaccines")} | {region} | {PAGE_BASE_TITLE}'
    area = PC_TO_OD_MAP[region]
    population = ITALY_POPULATION[region]
    tot_admins = get_total_administrations(area=area)
    perc_pop_vax = get_perc_pop_vax(tot_admins, population)
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
        perc_pop_vax=f"{perc_pop_vax}%",
        age_chart_data=get_age_chart_data(area),
        cat_chart_data=get_category_chart_data(area=area),
        previous_area_url=previous_url,
        next_area_url=next_region_url,
        areas_length=len(REGIONS),
        area_index=region_index,
        area=region
    )
    return render_template("vaccines.html", **report_data)
