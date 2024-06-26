"""
Data tools module
"""
import datetime as dt

import pandas as pd
import requests
from flask import current_app as app
from flask_babel import format_datetime, format_number, gettext

from covidashit.db_tools import (
    nat_data_coll,
    nat_series_coll,
    nat_trends_coll,
    pop_coll,
    prov_bdown_coll,
    prov_data_coll,
    prov_series_coll,
    prov_trends_coll,
    reg_bdown_coll,
    reg_data_coll,
    reg_series_coll,
    reg_trends_coll,
    vax_admins_coll,
    vax_admins_summary_coll,
)
from covidashit.util.misc import rubbish_notes, translate_series_lang
from settings import (
    DOW_FMTY,
    ITALY_MAP,
    KEY_PERIODS,
    OD_TO_PC_MAP,
    PC_TO_OD_MAP,
    PROVINCES,
    REGIONS,
    SERIES_DT_FMT,
    VERSION,
)
from settings.urls import URL_VAX_LATEST_UPDATE, URL_VAX_SUMMARY_DATA
from settings.vars import (
    ADMINS_DOSES_KEY,
    DATE_KEY,
    DELIVERED_DOSES_KEY,
    NEW_POSITIVE_KEY,
    NOTE_KEY,
    OD_POP_KEY,
    POP_KEY,
    POSITIVITY_INDEX,
    PROVINCE_KEY,
    REGION_KEY,
    TOTAL_CASES_KEY,
    VARS,
    VAX_ADMINS_PERC_KEY,
    VAX_AGE_KEY,
    VAX_AREA_KEY,
    VAX_BOOSTER_DOSE_KEY,
    VAX_DATE_FMT,
    VAX_DATE_KEY,
    VAX_FIRST_DOSE_KEY,
    VAX_LATEST_UPDATE_KEY,
    VAX_PROVIDER_KEY,
    VAX_SECOND_DOSE_KEY,
    VAX_TOT_ADMINS_KEY,
)

DATA_SERIES = [VARS[key]["title"] for key in VARS]
DASHBOARD_DATA = {
    "vars_config": VARS,
    "data_series": DATA_SERIES,
    "italy_map": ITALY_MAP,
    "VERSION": VERSION,
    "regions": REGIONS,
    "provinces": PROVINCES,
    "key_periods": KEY_PERIODS,
}
CUM_QUANTITIES = [q for q in VARS if VARS[q]["type"] == "cum"]
NON_CUM_QUANTITIES = [q for q in VARS if VARS[q]["type"] == "current"]
DAILY_QUANTITIES = [
    quantity
    for quantity in VARS
    if VARS[quantity]["type"] == "daily" and quantity.endswith("_ma")
]
TREND_CARDS = [
    quantity
    for quantity in VARS
    if not quantity.endswith("_ma") and VARS[quantity]["type"] != "vax"
]
PROV_TREND_CARDS = [TOTAL_CASES_KEY, NEW_POSITIVE_KEY]
VAX_DOSES = [VAX_FIRST_DOSE_KEY, VAX_SECOND_DOSE_KEY, VAX_BOOSTER_DOSE_KEY]


def get_query_menu(area=None):
    """
    Return the query menu
    :param area: str
    :return: dict
    """
    return {
        "national": {"query": {}, "collection": nat_data_coll},
        "regional": {"query": {REGION_KEY: area}, "collection": reg_data_coll},
        "provincial": {"query": {PROVINCE_KEY: area}, "collection": prov_data_coll},
    }


def get_notes(notes_type="national", area=None):
    """
    Return the notes in the data otherwise empty string when
    the received note is 0 or matches the RUBBISH_NOTE_REGEX
    :param notes_type: str
    :param area: str
    :return: str
    """
    query_menu = get_query_menu(area)
    query = query_menu[notes_type]["query"]
    collection = query_menu[notes_type]["collection"]
    notes = ""
    try:
        doc = next(collection.find(query).sort([(DATE_KEY, -1)]).limit(1))
        notes = doc[NOTE_KEY] if doc[NOTE_KEY] != 0 else None
    except StopIteration:
        app.logger.error("While getting notes: no data")
    return notes if notes is not None and not rubbish_notes(notes) else ""


def format_trends(trends):
    """In-place format count and last week count"""
    try:
        for t in trends:
            t["count"] = format_number(t["count"])
            t["last_week_count"] = format_number(t["last_week_count"])
            t["last_week_dt"] = format_datetime(t["last_week_dt"], DOW_FMTY)
    except Exception as e:
        app.logger.error(f"While formatting trends: {e}")
        pass
    return trends


def get_national_trends():
    """Return national trends from DB"""
    trends = format_trends(list(nat_trends_coll.find({})))
    return trends


def get_regional_trends(region):
    """
    Return a list of regional trends for a given region
    :param region: str
    :return: list
    """
    trends = []
    doc = reg_trends_coll.find_one({REGION_KEY: region})
    if doc:
        trends = format_trends(doc["trends"])
    return trends


def get_provincial_trends(province):
    """
    Return a list of provincial trends for a given province
    :param province: str
    :return: list
    """
    trends = []
    doc = prov_trends_coll.find_one({PROVINCE_KEY: province})
    if doc:
        trends = format_trends(doc["trends"])
    return trends


def get_regional_breakdown():
    """Return regional breakdown from DB"""
    doc = reg_bdown_coll.find_one({}, {"_id": False})
    if doc:
        breakdown = {
            k: sorted(doc[k], key=lambda x: x["count"], reverse=True) for k in doc
        }
        for k in doc:
            areas_breakdown = doc[k]
            for ab in areas_breakdown:
                ab["count"] = format_number(ab["count"])
    else:
        breakdown = {"err": "No data"}
    return breakdown


def get_provincial_breakdown(region):
    """Return provincial breakdown from DB"""
    b = {}
    doc = prov_bdown_coll.find_one({REGION_KEY: region}, {"_id": False})
    if doc:
        b = doc["breakdowns"]
        for k in b.keys():
            b[k] = sorted(b[k], key=lambda x: x["count"], reverse=True)
            areas_breakdown = b[k]
            for ab in areas_breakdown:
                ab["count"] = format_number(ab["count"])
    return b


def get_national_series():
    """Return national series from DB"""
    series = nat_series_coll.find_one({}, {"_id": False})
    if series:
        data = translate_series_lang(series)
    else:
        data = {"err": "No data"}
    return data


def get_regional_series(region):
    """Return regional series from DB"""
    data = {}
    series = reg_series_coll.find_one({REGION_KEY: region}, {"_id": False})
    if series:
        data = translate_series_lang(series)
    return data


def get_provincial_series(province):
    """Return provincial series from DB"""
    translated_series = []
    try:
        series = prov_series_coll.find_one({PROVINCE_KEY: province}, {"_id": False})
        translated_series = translate_series_lang(series)
    except Exception as e:
        app.logger.error(f"While getting provincial series data: {e}")
    return translated_series


def get_positivity_idx(area_type="national", area=None):
    """
    Return the positivity index for either the national or the regional
    views
    :param area_type: str: "national" or "regional"
    :param area: str
    :return: str
    """
    query_menu = get_query_menu(area)
    query = query_menu[area_type]["query"]
    collection = query_menu[area_type]["collection"]
    try:
        doc = next(collection.find(query).sort([(DATE_KEY, -1)]).limit(1))
        idx = doc[POSITIVITY_INDEX]
    except StopIteration:
        app.logger.error("While getting positivity idx: no data")
        idx = "n/a"
    return idx


def get_national_data():
    """Return a data frame of the national data from DB"""
    cursor = nat_data_coll.find({})
    df = pd.DataFrame(list(cursor))
    if df.empty:
        app.logger.error("While getting national data: no data")
    return df


def get_region_data(region):
    """Return a data frame for a given region from the regional collection"""
    cursor = reg_data_coll.find({REGION_KEY: region})
    df = pd.DataFrame(list(cursor))
    if df.empty:
        app.logger.error(f"While getting {region} data: no data")
    return df


def get_province_data(province):
    """
    Return a data frame for a given province from the provincial collection
    """
    cursor = prov_data_coll.find({PROVINCE_KEY: province})
    df = pd.DataFrame(list(cursor))
    if df.empty:
        app.logger.error(f"While getting {province} data: no data")
    return df


def get_latest_dpc_update_date(data_type="national"):
    """
    Return the value of the key PCM_DATE_KEY of the last dict in data
    :return: str
    """
    query_menu = get_query_menu()
    collection = query_menu[data_type]["collection"]
    try:
        doc = next(collection.find({}).sort([(DATE_KEY, -1)]).limit(1))
        latest_update = format_datetime(datetime=doc[DATE_KEY], format="short")
    except StopIteration:
        app.logger.error("While getting latest update: no data")
        latest_update = "n/a"
    return latest_update


def get_latest_od_update_date():
    """Return the lastest update dt"""
    try:
        response = requests.get(URL_VAX_LATEST_UPDATE).json()
        datestr = response["data"][0][VAX_LATEST_UPDATE_KEY]
        date_dt = dt.datetime.strptime(datestr, VAX_DATE_FMT)
        latest_update = format_datetime(datetime=date_dt, format="short")
    except Exception as e:
        app.logger.error(f"While getting latest vax update dt: {e}")
        latest_update = "n/a"
    return latest_update


def get_perc_pop_vax(population, area=None):
    """
    Return the percentages of population vaccinated
    for the first, second, and booster dose
    :param population: int
    :param area: str
    :return: float
    """
    perc_pop_vax = {
        "first": None,
        "second": None,
        "booster": None
    }
    first_count = get_tot_admins(dtype=VAX_FIRST_DOSE_KEY, area=area)
    second_count = get_tot_admins(dtype=VAX_SECOND_DOSE_KEY, area=area)
    booster_count = get_tot_admins(dtype=VAX_BOOSTER_DOSE_KEY, area=area)
    if population != 0:
        perc_pop_vax["first"] = round(
            (first_count / population) * 100, 1)
        perc_pop_vax["second"] = round(
            (second_count / population) * 100, 1)
        perc_pop_vax["booster"] = round(
            (booster_count / population) * 100, 1)
    return perc_pop_vax


def enrich_frontend_data(area=None, **data):
    """
    Return a data dict to be rendered which is an augmented copy of
    DASHBOARD_DATA defined in constants.py
    :param area: optional, str
    :param data: **kwargs
    :return: dict
    """
    try:
        data["area"] = area
    except KeyError:
        pass
    data.update(DASHBOARD_DATA)
    return data


def get_tot_admins(dtype, area=None):
    """
    Return the total of one of the three main vaccine data types
    allowed_types (VAX_TOT_ADMINS_KEY, VAX_FIRST_DOSE_KEY, VAX_SECOND_DOSE_KEY)
    :param dtype: str: must be in allowed_types
    :param area: str: region
    :return: int: the total administrations of a given data type
        if the data type is in allowed_types else 0
    """
    allowed_types = (
        VAX_TOT_ADMINS_KEY,
        VAX_FIRST_DOSE_KEY,
        VAX_SECOND_DOSE_KEY,
        VAX_BOOSTER_DOSE_KEY,
    )
    tot_adms = 0
    if dtype in allowed_types:
        if area:
            pipe = [
                {"$match": {VAX_AREA_KEY: area}},
                {"$group": {"_id": f"${VAX_AREA_KEY}", "tot": {"$sum": f"${dtype}"}}},
            ]
        else:
            pipe = [{"$group": {"_id": "{}", "tot": {"$sum": f"${dtype}"}}}]
        try:
            cursor = vax_admins_summary_coll.aggregate(pipeline=pipe)
            tot_adms = next(cursor)["tot"]
        except Exception as e:
            app.logger.error(f"While getting total admins: {e}")
    return int(tot_adms)


def get_age_chart_data(area=None):
    """Return age series data"""
    chart_data = {}
    vax_group = {
        "$group": {
            "_id": {VAX_AGE_KEY: f"${VAX_AGE_KEY}", VAX_AREA_KEY: f"${VAX_AREA_KEY}"},
            f"{VAX_FIRST_DOSE_KEY}": {"$sum": f"${VAX_FIRST_DOSE_KEY}"},
            f"{VAX_SECOND_DOSE_KEY}": {"$sum": f"${VAX_SECOND_DOSE_KEY}"},
            f"{VAX_BOOSTER_DOSE_KEY}": {"$sum": f"${VAX_BOOSTER_DOSE_KEY}"},
        }
    }
    vax_sort = {"$sort": {"_id": 1}}
    try:
        if area is not None:
            area = PC_TO_OD_MAP[area]
            vax_match = {"$match": {VAX_AREA_KEY: area}}
            vax_pipe = [vax_match, vax_group, vax_sort]
        else:
            vax_pipe = [vax_group, vax_sort]
        age_pop_dict = get_age_pop_dict(area)
        app.logger.debug(age_pop_dict)
        vax_cursor = vax_admins_coll.aggregate(pipeline=vax_pipe)
        pop_cursor = pop_coll.find()
        df_vax = pd.json_normalize(list(vax_cursor))
        df_pop = pd.json_normalize((list(pop_cursor)))
        right_on_col1, right_on_col2 = "_id." + VAX_AREA_KEY, "_id." + VAX_AGE_KEY
        out_df = df_pop.merge(
            df_vax,
            left_on=[VAX_AREA_KEY, VAX_AGE_KEY],
            right_on=[right_on_col1, right_on_col2],
        )
        col_to_group = "_id." + VAX_AGE_KEY
        cols_to_sum = [
            VAX_FIRST_DOSE_KEY,
            VAX_SECOND_DOSE_KEY,
            VAX_BOOSTER_DOSE_KEY,
            OD_POP_KEY,
        ]
        out_df = out_df.groupby(by=[col_to_group]).sum(cols_to_sum)
        categories = df_vax[f"_id.{VAX_AGE_KEY}"].unique().tolist()
        chart_data = {
            "title": gettext("Admins per age"),
            "yAxisTitle": gettext("Counts"),
            "categories": categories,
            "age_dict": age_pop_dict,
            "first": {
                "name": gettext("First Dose"),
                "data": out_df[VAX_FIRST_DOSE_KEY].tolist(),
            },
            "second": {
                "name": gettext("Second Dose"),
                "data": out_df[VAX_SECOND_DOSE_KEY].tolist(),
            },
            "booster": {
                "name": gettext("Booster Dose"),
                "data": out_df[VAX_BOOSTER_DOSE_KEY].tolist(),
            },
            "population": {
                "name": gettext("Population"),
                "data": out_df[OD_POP_KEY].tolist(),
            },
        }
    except Exception as e:
        app.logger.error(f"While getting age chart data: {e}")
    return chart_data


def get_admins_per_region():
    """Return administrations data per region"""
    chart_data = {}
    try:
        pipe = [
            {"$match": {VAX_AREA_KEY: {"$not": {"$eq": "ITA"}}}},
            {
                "$group": {
                    "_id": f"${VAX_AREA_KEY}",
                    "first": {"$sum": f"${VAX_FIRST_DOSE_KEY}"},
                    "second": {"$sum": f"${VAX_SECOND_DOSE_KEY}"},
                    "booster": {"$sum": f"${VAX_BOOSTER_DOSE_KEY}"},
                }
            },
        ]
        cursor = vax_admins_summary_coll.aggregate(pipeline=pipe)
        data = list(cursor)
        df = pd.DataFrame(data)
        df["region"] = df["_id"].apply(lambda x: OD_TO_PC_MAP[x])
        pop_dict = get_region_pop_dict()
        df["population"] = df["region"].apply(lambda x: pop_dict[x])
        df["percentage_2nd"] = df["second"].div(df["population"])
        df["percentage_3rd"] = df["booster"].div(df["population"])
        df.sort_values(by=["population"], ascending=False, inplace=True)
        chart_data = {
            "title": gettext("Admins per region"),
            "categories": df["region"].values.tolist(),
            "pop_dict": pop_dict,
            "first": {
                "name": gettext("First Dose"),
                "data": df["first"].values.tolist(),
            },
            "second": {
                "name": gettext("Second Dose"),
                "data": df["second"].values.tolist(),
            },
            "booster": {
                "name": gettext("Booster Dose"),
                "data": df["booster"].values.tolist(),
            },
            "population": {
                "name": gettext("Population"),
                "data": df["population"].values.tolist(),
            },
        }
        app.logger.debug(f"region df : \n{df}")
    except Exception as e:
        app.logger.error(f"While getting region chart data: {e}")
    return chart_data


def exp_tot_admins(x, tot_admins):
    """Return tot administration scaled to the region pop percentage"""
    pop_dict = get_region_pop_dict()
    it_pop = sum([v for v in pop_dict.values()])
    return round(pop_dict[x] / it_pop * tot_admins)


def get_admins_perc(area=None):
    """
    Return the percentage of administered doses wrt the delivered ones.
    It uses the CSV Url as it's tiny.
    :param area: optional str
    :return: float
    """
    admins_perc = "n/a"
    try:
        df = pd.read_csv(URL_VAX_SUMMARY_DATA)
        if area is None:
            admins_perc = round(
                (df[ADMINS_DOSES_KEY].sum() / df[DELIVERED_DOSES_KEY].sum() * 100), 1
            )
        else:
            df = df[df[VAX_AREA_KEY] == area]
            admins_perc = df[VAX_ADMINS_PERC_KEY].item()
    except Exception as e:
        app.logger.error(f"While getting % administered doses: {e}")
    return admins_perc


def get_admins_timeseries_chart_data():
    """
    Return admins timeseries data to frontend
    :return: dict
    """
    chart_data = {}
    try:
        pipe = [{"$sort": {VAX_DATE_KEY: 1}}]
        cursor = vax_admins_summary_coll.aggregate(pipeline=pipe)
        data = list(cursor)
        df = pd.DataFrame(data)

        dates = (
            df[VAX_DATE_KEY]
            .apply(lambda x: format_datetime(x, SERIES_DT_FMT))
            .unique()
            .tolist()
        )
        data = [
            {
                "name": OD_TO_PC_MAP[r],
                "data": (
                    df[df[VAX_AREA_KEY] == r][VAX_SECOND_DOSE_KEY].cumsum()
                    / df[df[VAX_AREA_KEY] == r][POP_KEY]
                    * 100
                )
                .round(2)
                .to_list(),
            }
            for r in sorted(df[VAX_AREA_KEY].unique())
        ]
        chart_data = {
            "title": gettext("Vaccination trend"),
            "yAxisTitle": gettext("Pop. vaccinated (2nd dose) [%]"),
            "dates": dates,
            "data": data,
        }
        app.logger.debug(f"Time series chart data {chart_data}")
    except Exception as e:
        app.logger.error(f"While getting vax timeseries chart data {e}")
    return chart_data


def get_admins_per_provider_chart_data(area=None):
    """
    Return provider pie-chart data for highcharts
    :return:
    """
    group = {
        "$group": {
            "_id": f"${VAX_PROVIDER_KEY}",
            "tot": {"$sum": f"${VAX_TOT_ADMINS_KEY}"},
        }
    }
    sort = {"$sort": {"tot": -1}}
    if area is not None:
        area = PC_TO_OD_MAP[area]
        match = {"$match": {VAX_AREA_KEY: area}}
        pipe = [match, group, sort]
    else:
        pipe = [group, sort]
    data = list(vax_admins_coll.aggregate(pipeline=pipe))
    chart_data = {
        "title": gettext("Admins per provider"),
        "name": gettext("Doses administered"),
        "data": [[d["_id"], d["tot"]] for d in data],
    }
    return chart_data


def get_vax_trends_data(area=None):
    """
    Return first-, second-, and third-dose data in the last two days
    :param area: optional, str
    :return: list of dicts
    """
    if area is None:
        pipe = [
            {
                "$group": {
                    "_id": f"${VAX_DATE_KEY}",
                    VAX_FIRST_DOSE_KEY: {"$sum": f"${VAX_FIRST_DOSE_KEY}"},
                    VAX_SECOND_DOSE_KEY: {"$sum": f"${VAX_SECOND_DOSE_KEY}"},
                    VAX_BOOSTER_DOSE_KEY: {"$sum": f"${VAX_BOOSTER_DOSE_KEY}"},
                }
            },
            {"$sort": {"_id": -1}},
            {"$limit": 7},
        ]
    else:
        pipe = [
            {"$match": {VAX_AREA_KEY: area}},
            {
                "$group": {
                    "_id": f"${VAX_DATE_KEY}",
                    VAX_FIRST_DOSE_KEY: {"$sum": f"${VAX_FIRST_DOSE_KEY}"},
                    VAX_SECOND_DOSE_KEY: {"$sum": f"${VAX_SECOND_DOSE_KEY}"},
                    VAX_BOOSTER_DOSE_KEY: {"$sum": f"${VAX_BOOSTER_DOSE_KEY}"},
                }
            },
            {"$sort": {"_id": -1}},
            {"$limit": 7},
        ]
    data = list(vax_admins_coll.aggregate(pipeline=pipe))
    return data


def get_vax_trends(area=None):
    """
    Return the vax-trends array
    :param area: optional, str
    :return: list of dicts
    """
    data = get_vax_trends_data(area)
    trends = []
    for d in VAX_DOSES:
        try:
            last_week_dt = data[6]["_id"]
            count = data[0][d]
            last_week_count = data[6][d]
            diff = count - last_week_count
            if diff > 0:
                status = "increase"
            elif diff < 0:
                status = "decrease"
            else:
                status = "stable"
            try:
                perc = f"{round(diff / last_week_count * 100)}%"
            except (ValueError, ZeroDivisionError):
                perc = "n/a"
            trends.append(
                {
                    "id": d,
                    "last_week_count": format_number(last_week_count),
                    "percentage": perc,
                    "title": VARS[d]["title"],
                    "colour": VARS[d][status]["colour"],
                    "icon": VARS[d]["icon"],
                    "status_icon": VARS[d][status]["icon"],
                    "count": format_number(count),
                    "last_week_dt": format_datetime(last_week_dt, DOW_FMTY),
                }
            )
        except Exception as e:
            app.logger.error(f"While getting vax trends: {e}")
    return trends


def get_region_pop_dict():
    """
    Return a region:population dict
    :return: dict
    """
    it_pop_dict = {}
    try:
        pop_pipe = [
            {
                "$group": {
                    "_id": {VAX_AREA_KEY: f"${VAX_AREA_KEY}"},
                    f"{OD_POP_KEY}": {"$sum": f"${OD_POP_KEY}"},
                },
            }
        ]
        records = list(pop_coll.aggregate(pipeline=pop_pipe))
        it_pop_dict = {
            OD_TO_PC_MAP[r["_id"][VAX_AREA_KEY]]: r[OD_POP_KEY] for r in records
        }
    except Exception as e:
        app.logger.error(f"While getting region pop dict: {e}")
    return it_pop_dict


def get_area_population(area=None):
    """
    Return population for a given area if area is defined else for Italy
    :param area: str
    :return: int
    """
    pop_dict = get_region_pop_dict()
    try:
        population = pop_dict[area]
    except KeyError:
        population = sum([v for v in pop_dict.values()])
    return population


def get_age_pop_dict(area=None):
    """
    Return an age_range:population dict
    :return: dict
    """
    age_pop_dict = {}
    try:
        if area is None:
            pop_pipe = [
                {
                    "$group": {
                        "_id": {VAX_AGE_KEY: f"${VAX_AGE_KEY}"},
                        f"{OD_POP_KEY}": {"$sum": f"${OD_POP_KEY}"},
                    },
                }
            ]
        else:
            pop_pipe = [
                {"$match": {VAX_AREA_KEY: area}},
                {
                    "$group": {
                        "_id": {VAX_AGE_KEY: f"${VAX_AGE_KEY}"},
                        f"{OD_POP_KEY}": {"$sum": f"${OD_POP_KEY}"},
                    },
                },
            ]
        records = list(pop_coll.aggregate(pipeline=pop_pipe))
        age_pop_dict = {r["_id"][VAX_AGE_KEY]: r[OD_POP_KEY] for r in records}
    except Exception as e:
        app.logger.error(f"While getting age pop dict: {e}")
    return age_pop_dict
