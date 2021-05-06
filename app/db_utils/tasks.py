"""
Celery tasks
"""
import pandas as pd
from flask import current_app as app
from pymongo import UpdateOne, InsertOne

from app import celery
from app.data import TREND_CARDS
from app.db_utils import (
    nat_data_coll, nat_series_coll, nat_trends_coll, reg_data_coll,
    reg_series_coll, reg_trends_coll, reg_bdown_coll, prov_data_coll,
    prov_bdown_coll, prov_trends_coll, prov_series_coll, vax_admins_coll,
    vax_admins_summary_coll, it_pop_coll
)
from app.db_utils.etl import (
    load_df, preprocess_national_df, build_national_series, build_trend,
    preprocess_regional_df, build_series, build_national_trends,
    build_regional_breakdown, preprocess_provincial_df,
    build_provincial_breakdowns, build_provincial_trends,
    build_provincial_series, preprocess_vax_admins_df,
    preprocess_vax_admins_summary_df, create_istat_population_df
)
from settings import REGIONS, PROVINCES
from settings.urls import (
    URL_NATIONAL, URL_REGIONAL, URL_PROVINCIAL, URL_VAX_ADMINS_DATA,
    URL_VAX_ADMINS_SUMMARY_DATA
)
from settings.vars import (
    REGION_KEY, PROVINCE_KEY, DATE_KEY, VAX_DATE_KEY, POP_ISTAT_KEY
)


@celery.task
def update_national_collection():
    """Update national collection"""
    response = {"status": "ko", "n_inserted_docs": 0, "errors": []}
    try:
        df = load_df(URL_NATIONAL)
        df = preprocess_national_df(df)
        df['_id'] = df[DATE_KEY]
        inserted_ids = []
        records_in_db = list(nat_data_coll.find())
        if records_in_db:
            df_mongo = pd.DataFrame(records_in_db)
            common = df.merge(df_mongo, on=[DATE_KEY])
            df_to_db = df[(~df[DATE_KEY].isin(common[DATE_KEY]))]
            if not df_to_db.empty:
                new_records = df_to_db.to_dict(orient='records')
                r = nat_data_coll.insert_many(new_records, ordered=True)
                inserted_ids.extend(r.inserted_ids)
                response["n_inserted_docs"] = len(inserted_ids)
                response["inserted_ids"] = inserted_ids
        else:
            msg = f"Filling empty {nat_data_coll.name}"
            app.logger.warning(msg)
            r = nat_data_coll.insert_many(df.to_dict(orient='records'))
            inserted_ids.extend(r.inserted_ids)
            response["n_inserted_docs"] = len(inserted_ids)
            response["msg"] = msg
        msg = f"{len(inserted_ids)} docs updated in {nat_data_coll.name}"
        app.logger.warning(msg)
        response["status"] = "ok"
    except Exception as e:
        response["errors"], response["msg"] = f"{e}", f"{e}"
    return response


@celery.task
def update_national_series_collection():
    """Update national series collection"""
    response = {"status": "ko", "updated": False, "errors": []}
    df = load_df(URL_NATIONAL)
    df = preprocess_national_df(df)
    df['_id'] = df[DATE_KEY]
    national_series = build_national_series(df)
    cursor = nat_series_coll.find({})
    try:
        doc = cursor.next()
        mongo_id = doc['_id']
        _filter, update = {'_id': mongo_id}, {"$set": national_series}
        r = nat_series_coll.update_one(_filter, update, upsert=True)
        msg = f"Updated {nat_series_coll.name}"
        app.logger.warning(msg)
        response["status"], response["updated"] = "ok", r.acknowledged
    except StopIteration:
        r = nat_series_coll.insert_one(national_series)
        msg = f"Filled empty collection {nat_series_coll.name}"
        response["status"], response["updated"] = "ok", r.acknowledged
    response["msg"] = msg
    return response


@celery.task
def update_national_trends_collection():
    """Update national trends collection"""
    response = {"ids": [], "updated": False, "errors": []}
    df = load_df(URL_NATIONAL)
    df = preprocess_national_df(df)
    n_docs = 0
    for col in TREND_CARDS:
        response["status"] = "ok"
        try:
            _filter = {'id': col}
            trend = {"$set": build_trend(df, col)}
            results = nat_trends_coll.update_one(_filter, trend, upsert=True)
            if results.modified_count:
                n_docs += 1
                response["ids"].append(col)
        except Exception as e:
            response["status"] = "ko"
            response["errors"].append(f"{e}")
            app.logger.error(f"{e}")
            continue
    response["n_docs"] = n_docs
    msg = f"{n_docs} docs updated in {nat_trends_coll.name}"
    app.logger.warning(msg)
    response["msg"] = msg
    return response


@celery.task
def update_regional_collection():
    """Update regional-data collection"""
    inserted_ids = []
    response = {"status": "ko", "updated": False, "errors": [], "msg": ""}
    try:
        df = load_df(URL_REGIONAL)
        df = preprocess_regional_df(df)
        latest_dt = df[DATE_KEY].max()
        cursor = reg_data_coll.find().sort(DATE_KEY, -1).limit(1)
        latest_dt_db = cursor.next()[DATE_KEY]
        if latest_dt.date() == latest_dt_db.date():
            msg = "DB up-to-date"
            app.logger.warning(msg)
        else:
            df = df[df[DATE_KEY] > latest_dt_db]
            msg = f"Latest data missing in {reg_data_coll.name} ! Updating..."
            app.logger.warning(msg)
            new_records = df.to_dict(orient='records')
            r = reg_data_coll.insert_many(new_records, ordered=True)
            inserted_ids.extend(r.inserted_ids)
            msg = f"{len(inserted_ids)} docs updated in {reg_data_coll.name}"
            response["updated"] = True
        response["status"], response["msg"] = "ok", msg
        app.logger.warning(msg)
    except Exception as e:
        err = f"{e}"
        app.logger.error(err)
        response["errors"].append(err)
    response["n_docs"] = len(inserted_ids)
    return response


@celery.task
def update_regional_series_collection():
    """Update regional series collection"""
    n_docs = 0
    response = {"status": "ko", "regions": [], "updated": False, "errors": []}
    updated = False
    try:
        df = load_df(URL_REGIONAL)
        df = preprocess_regional_df(df)
        for r in REGIONS:
            _filter = {REGION_KEY: r}
            r_series = build_series(df[df[REGION_KEY] == r])
            update = {
                "$set": {
                    REGION_KEY: r,
                    "dates": r_series[0],
                    "daily": r_series[1],
                    "current": r_series[2],
                    "cum": r_series[3]
                }
            }
            results = reg_series_coll.update_one(_filter, update, upsert=True)
            if results.modified_count:
                n_docs += 1
                response["regions"].append(r)
                response["n_docs"] = n_docs
                response["updated"] = results.acknowledged
                updated = True
        msg = f"{n_docs} docs updated in {reg_data_coll.name}"
        response["msg"] = msg
        if not updated:
            msg = f"Nothing to update in {reg_series_coll.name}"
            response["msg"] = msg
        response["status"] = "ok"
        app.logger.warning(msg)
    except Exception as e:
        response["errors"].append(f"{e}")
        app.logger.error(f"{e}")
    return response


@celery.task
def update_regional_trends_collection():
    """Update regional trends collection"""
    n_docs = 0
    response = {"status": "ko", "regions": [], "updated": False, "errors": []}
    try:
        df = load_df(URL_REGIONAL)
        df = preprocess_regional_df(df)
        for r in REGIONS:
            _filter = {REGION_KEY: r}
            update = {
                "$set": {
                    REGION_KEY: r,
                    "trends": build_national_trends(df[df[REGION_KEY] == r])
                }
            }
            results = reg_trends_coll.update_one(_filter, update, upsert=True)
            if results.modified_count:
                n_docs += 1
                response["regions"].append(r)
                response["n_docs"] = n_docs
                response["updated"] = results.acknowledged
        msg = f"{n_docs} docs updated in {reg_trends_coll.name}"
        response["msg"] = msg
        if not response["updated"]:
            msg = f"Nothing to update in {reg_trends_coll.name}"
            response["msg"] = msg
        response["status"] = "ok"
        app.logger.warning(msg)
    except Exception as e:
        response["errors"].append(f"{e}")
        app.logger.error(f"{e}")
    return response


@celery.task
def update_regional_breakdown_collection():
    """Update regional breakdown"""
    response = {"status": "ko", "updated": False, "errors": []}
    try:
        df = load_df(URL_REGIONAL)
        df = preprocess_regional_df(df)
        breakdown = build_regional_breakdown(df)
        try:
            doc = reg_bdown_coll.find().next()
            mongo_id = doc["_id"]
            _filter = {"_id": mongo_id}
            update = {"$set": breakdown}
            res = reg_bdown_coll.update_one(_filter, update, upsert=True)
            msg = f"Updated regional breakdown in {reg_bdown_coll.name}"
            response["updated"], response["msg"] = res.acknowledged, msg
            response["status"] = "ok"
            app.logger.warning(msg)
        except StopIteration as e:
            msg = f"{e}"
            app.logger.error(msg)
            response["msg"] = msg
    except Exception as e:
        response["errors"].append(f"{e}")
        app.logger.error(f"{e}")
    return response


@celery.task
def update_provincial_collection():
    """Update provincial data collection"""
    response = {"status": "ko", "updated": False, "errors": [], "msg": ""}
    inserted_ids = []
    try:
        df = load_df(URL_PROVINCIAL)
        df = preprocess_provincial_df(df)
        latest_dt = df[DATE_KEY].max()
        cursor = prov_data_coll.find().sort(DATE_KEY, -1).limit(1)
        latest_dt_db = next(cursor)[DATE_KEY]
        if latest_dt.date() == latest_dt_db.date():
            msg = "DB up-to-date"
            app.logger.warning(msg)
        else:
            msg = f"Latest data missing in {prov_data_coll.name}! Updating..."
            app.logger.warning(msg)
            df = df[df[DATE_KEY] > latest_dt_db]
            new_records = df.to_dict(orient='records')
            r = prov_data_coll.insert_many(new_records, ordered=True)
            inserted_ids.extend(r.inserted_ids)
            msg = f"{len(inserted_ids)} docs updated in {prov_data_coll.name}"
            response["updated"] = True
        response["status"], response["msg"] = "ok", msg
        app.logger.warning(msg)
    except Exception as e:
        err = f"{e}"
        app.logger.error(err)
        response["errors"].append(err)
    response["n_docs"] = len(inserted_ids)
    return response


@celery.task
def update_provincial_breakdown_collection():
    """Update provincial breakdown"""
    n_docs = 0
    response = {"status": "ko", "regions": [], "updated": False, "errors": []}
    updated, msg = False, ""
    try:
        df = load_df(URL_PROVINCIAL)
        pattern = "|".join(PROVINCES)
        df = df[df[PROVINCE_KEY].str.contains(pattern)]
        df = preprocess_provincial_df(df)
        breakdowns = build_provincial_breakdowns(df)
        for b in breakdowns:
            _filter = {REGION_KEY: b[REGION_KEY]}
            update = {"$set": b}
            res = prov_bdown_coll.update_one(_filter, update, upsert=True)
            if res.modified_count:
                n_docs += 1
                response["regions"].append(b[REGION_KEY])
                response["n_docs"] = n_docs
                response["updated"] = res.acknowledged
                updated = True
        msg = f"Updated {n_docs} docs in {prov_bdown_coll.name}"
        if not updated:
            msg = f"Nothing to update in {prov_bdown_coll.name}"
            app.logger.warning(msg)
        response["status"], response["msg"] = "ok", msg
        app.logger.warning(msg)
    except Exception as e:
        response["errors"].append(f"{e}")
        app.logger.error(f"{e}")
    return response


@celery.task
def update_provincial_series_or_trends_collection(coll_type):
    """Update provincial series or trends collection"""
    n_docs = 0
    response = {"status": "ko", "provs": [], "updated": False, "errors": []}
    updated, msg = False, ""
    df = load_df(URL_PROVINCIAL)
    pattern = "|".join(PROVINCES)
    df = df[df[PROVINCE_KEY].str.contains(pattern)]
    df = preprocess_provincial_df(df)
    if coll_type == "trends":
        records = build_provincial_trends(df)
        coll = prov_trends_coll
    elif coll_type == "series":
        records = build_provincial_series(df)
        coll = prov_series_coll
    else:
        msg = "Invalid collection type"
        app.logger.error(msg)
        response["errors"].append(msg)
        return response
    try:
        for r in records:
            _filter = {PROVINCE_KEY: r[PROVINCE_KEY]}
            update = {"$set": r}
            results = coll.update_one(_filter, update, upsert=True)
            if results.modified_count:
                n_docs += 1
                response["provs"].append(r[PROVINCE_KEY])
                response["n_docs"] = n_docs
                response["updated"] = results.acknowledged
                updated = True
        msg = f"Updated {n_docs} docs in {prov_bdown_coll.name}"
        if not updated:
            msg = f"Nothing to update in {prov_bdown_coll.name}"
        app.logger.warning(msg)
        response["status"], response["msg"] = "ok", msg
    except Exception as e:
        response["errors"].append(f"{e}")
        app.logger.error(f"{e}")
    return response


@celery.task
def update_vax_collections(summary=False):
    """Update vax / vax_summary collection"""
    response = {"status": "ko", "n_inserted_docs": 0, "errors": []}
    operations = []
    if not summary:
        collection = vax_admins_coll
        url = URL_VAX_ADMINS_DATA
        df = pd.read_csv(url, parse_dates=[VAX_DATE_KEY])
        df = preprocess_vax_admins_df(df)
    else:
        collection = vax_admins_summary_coll
        url = URL_VAX_ADMINS_SUMMARY_DATA
        df = pd.read_csv(url, parse_dates=[VAX_DATE_KEY])
        df = preprocess_vax_admins_summary_df(df)
    try:
        for index, row in df.iterrows():
            _id = row['_id']
            cursor = collection.find({'_id': _id})
            new_value = row.to_dict()
            try:
                next(cursor)
                operations.append(UpdateOne({'_id': _id}, {'$set': new_value}))
            except StopIteration:
                operations.append(InsertOne(new_value))
        r = collection.bulk_write(operations)
        bulk_result = r.bulk_api_result
        response['bulk_update'] = bulk_result
        response["status"] = "ok"
        n_inserted = bulk_result['nInserted']
        n_modified = bulk_result['nModified']
        msg = f"{n_inserted} inserted and {n_modified} modified"
        app.logger.warning(msg)
    except Exception as e:
        app.logger.error(f"While updating vax collection: {e}")
        response["errors"], response["msg"] = f"{e}", f"{e}"
    return response


@celery.task
def update_istat_it_population_collection():
    """Update ISTAT Italy population collection"""
    ops = []
    cols = [POP_ISTAT_KEY, REGION_KEY]
    istat_df = create_istat_population_df()
    try:
        df_db = pd.DataFrame(list(it_pop_coll.find({})))
        df_compare = df_db[cols].compare(istat_df)
        if not df_compare.empty:
            new_df = istat_df.loc[df_compare.index.values].reset_index()
            ids = df_db.loc[df_compare.index.values]['_id'].to_list()
            for r in it_pop_coll.find({'_id': {'$in': ids}}):
                mask = new_df[REGION_KEY] == r[REGION_KEY]
                new_value = new_df[mask].to_dict(orient='records')[0]
                ops.append(UpdateOne({'_id': r['_id']}, {'$set': new_value}))
            app.logger.info(f"Updating {len(ops)} region population")
            results = it_pop_coll.bulk_write(ops)
            app.logger.info(f"Bulk update result: {results.bulk_api_result}")
        else:
            app.logger.info("No region population to update")
    except Exception as e:
        app.logger.error(f"While updating italy population collection: {e}")
