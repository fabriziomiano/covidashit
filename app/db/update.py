"""
DB Update
"""
import pandas as pd
from flask import current_app as app
from pymongo import UpdateOne

from app.data import (
    NAT_DATA_COLL, NAT_TRENDS_COLL, NAT_SERIES_COLL, REG_DATA_COLL,
    REG_TRENDS_COLL, REG_BREAKDOWN_COLL, PROV_DATA_COLL, PROV_SERIES_COLL,
    PROV_BREAKDOWN_COLL, PROV_TRENDS_COLL, REG_SERIES_COLL, TREND_CARDS,
    VAX_COLL, VAX_SUMMARY_COLL
)
from app.data.etl import (
    load_df, build_series, build_national_trends, build_provincial_series,
    build_provincial_trends, build_regional_breakdown,
    build_provincial_breakdowns, build_national_series, build_trend,
    augment_national_df, augment_regional_df, augment_provincial_df,
    augment_vax_df, augment_summary_vax_df
)
from config import (
    DATE_KEY, PROVINCES, PROVINCE_KEY, REGIONS, REGION_KEY,
    URL_PROVINCIAL, URL_REGIONAL, URL_NATIONAL, URL_VAX_DATA,
    URL_VAX_SUMMARY_DATA, VAX_DATE_KEY
)


def update_national_collection():
    """Update national collection"""
    response = {"status": "ko", "n_inserted_docs": 0, "errors": []}
    try:
        df = load_df(URL_NATIONAL)
        df = augment_national_df(df)
        df['_id'] = df[DATE_KEY]
        inserted_ids = []
        records_in_db = list(NAT_DATA_COLL.find())
        if records_in_db:
            df_mongo = pd.DataFrame(records_in_db)
            common = df.merge(df_mongo, on=[DATE_KEY])
            df_to_db = df[(~df[DATE_KEY].isin(common[DATE_KEY]))]
            if not df_to_db.empty:
                new_records = df_to_db.to_dict(orient='records')
                r = NAT_DATA_COLL.insert_many(new_records, ordered=True)
                inserted_ids.extend(r.inserted_ids)
                response["n_inserted_docs"] = len(inserted_ids)
                response["inserted_ids"] = inserted_ids
                response["status"] = "ok"
        else:
            msg = f"Filling empty {NAT_DATA_COLL.name}"
            app.logger.warning(msg)
            r = NAT_DATA_COLL.insert_many(df.to_dict(orient='records'))
            inserted_ids.extend(r.inserted_ids)
            response["n_inserted_docs"] = len(inserted_ids)
            response["status"] = "ok"
            response["msg"] = msg
        msg = f"{len(inserted_ids)} docs updated in {NAT_DATA_COLL.name}"
        app.logger.warning(msg)
    except Exception as e:
        response["errors"], response["msg"] = f"{e}", f"{e}"
    return response


def update_national_series_collection():
    """Update national series collection"""
    response = {"status": "ko", "updated": False, "errors": []}
    df = load_df(URL_NATIONAL)
    df = augment_national_df(df)
    df['_id'] = df[DATE_KEY]
    national_series = build_national_series(df)
    cursor = NAT_SERIES_COLL.find({})
    try:
        doc = cursor.next()
        mongo_id = doc['_id']
        _filter, update = {'_id': mongo_id}, {"$set": national_series}
        r = NAT_SERIES_COLL.update_one(_filter, update, upsert=True)
        msg = f"Updated {NAT_SERIES_COLL.name}"
        app.logger.warning(msg)
        response["status"], response["updated"] = "ok", r.acknowledged
        app.logger.warning(msg)
    except StopIteration:
        r = NAT_SERIES_COLL.insert_one(national_series)
        msg = f"Filled empty collection {NAT_SERIES_COLL.name}"
        response["status"], response["updated"] = "ok", r.acknowledged
    response["msg"] = msg
    return response


def update_national_trends_collection():
    """Update national trends collection"""
    response = {"ids": [], "updated": False, "errors": []}
    df = load_df(URL_NATIONAL)
    df = augment_national_df(df)
    n_docs = 0
    for col in TREND_CARDS:
        response["status"] = "ok"
        try:
            _filter = {'id': col}
            trend = {"$set": build_trend(df, col)}
            results = NAT_TRENDS_COLL.update_one(_filter, trend, upsert=True)
            if results.modified_count:
                n_docs += 1
                response["ids"].append(col)
        except Exception as e:
            response["status"] = "ko"
            response["errors"].append(f"{e}")
            app.logger.error(f"{e}")
            continue
    response["n_docs"] = n_docs
    msg = f"{n_docs} docs updated in {NAT_TRENDS_COLL.name}"
    app.logger.warning(msg)
    response["msg"] = msg
    return response


def update_regional_collection():
    """Update regional-data collection"""
    inserted_ids = []
    response = {"status": "ko", "updated": False, "errors": [], "msg": ""}
    try:
        df = load_df(URL_REGIONAL)
        df = augment_regional_df(df)
        latest_dt = df[DATE_KEY].max()
        cursor = REG_DATA_COLL.find().sort(DATE_KEY, -1).limit(1)
        latest_dt_db = cursor.next()[DATE_KEY]
        if latest_dt.date() == latest_dt_db.date():
            msg = "DB up-to-date"
            app.logger.warning(msg)
        else:
            df = df[df[DATE_KEY] > latest_dt_db]
            app.logger.warning("Latest data missing! Updating...")
            new_records = df.to_dict(orient='records')
            r = REG_DATA_COLL.insert_many(new_records, ordered=True)
            inserted_ids.extend(r.inserted_ids)
            msg = f"{len(inserted_ids)} docs updated in {REG_DATA_COLL.name}"
            response["updated"] = True
        response["status"], response["msg"] = "ok", msg
        app.logger.warning(msg)
    except Exception as e:
        err = f"{e}"
        app.logger.error(err)
        response["errors"].append(err)
    response["n_docs"] = len(inserted_ids)
    return response


def update_regional_series_collection():
    """Update regional series collection"""
    n_docs = 0
    response = {"status": "ko", "regions": [], "updated": False, "errors": []}
    updated = False
    try:
        df = load_df(URL_REGIONAL)
        df = augment_regional_df(df)
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
            results = REG_SERIES_COLL.update_one(_filter, update, upsert=True)
            if results.modified_count:
                n_docs += 1
                response["regions"].append(r)
                response["n_docs"] = n_docs
                response["updated"] = results.acknowledged
                updated = True
        msg = f"{n_docs} docs updated in {REG_DATA_COLL.name}"
        response["msg"] = msg
        if not updated:
            msg = f"Nothing to update in {REG_SERIES_COLL.name}"
            response["msg"] = msg
        response["status"] = "ok"
        app.logger.warning(msg)
    except Exception as e:
        response["errors"].append(f"{e}")
        app.logger.error(f"{e}")
    return response


def update_regional_trends_collection():
    """Update regional trends collection"""
    n_docs = 0
    response = {"status": "ko", "regions": [], "updated": False, "errors": []}
    try:
        df = load_df(URL_REGIONAL)
        df = augment_regional_df(df)
        for r in REGIONS:
            _filter = {REGION_KEY: r}
            update = {
                "$set": {
                    REGION_KEY: r,
                    "trends": build_national_trends(df[df[REGION_KEY] == r])
                }
            }
            results = REG_TRENDS_COLL.update_one(_filter, update, upsert=True)
            if results.modified_count:
                n_docs += 1
                response["regions"].append(r)
                response["n_docs"] = n_docs
                response["updated"] = results.acknowledged
        msg = f"{n_docs} docs updated in {REG_TRENDS_COLL.name}"
        response["msg"] = msg
        if not response["updated"]:
            msg = f"Nothing to update in {REG_TRENDS_COLL.name}"
            response["msg"] = msg
        response["status"] = "ok"
        app.logger.warning(msg)
    except Exception as e:
        response["errors"].append(f"{e}")
        app.logger.error(f"{e}")
    return response


def update_regional_breakdown_collection():
    """Update regional breakdown"""
    response = {"status": "ko", "updated": False, "errors": []}
    try:
        df = load_df(URL_REGIONAL)
        df = augment_regional_df(df)
        breakdown = build_regional_breakdown(df)
        try:
            doc = REG_BREAKDOWN_COLL.find().next()
            mongo_id = doc["_id"]
            _filter = {"_id": mongo_id}
            update = {"$set": breakdown}
            res = REG_BREAKDOWN_COLL.update_one(_filter, update, upsert=True)
            msg = f"Updated regional breakdown in {REG_BREAKDOWN_COLL.name}"
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


def update_provincial_collection():
    """Update provincial data collection"""
    response = {"status": "ko", "updated": False, "errors": [], "msg": ""}
    inserted_ids = []
    try:
        df = load_df(URL_PROVINCIAL)
        df = augment_provincial_df(df)
        latest_dt = df[DATE_KEY].max()
        cursor = PROV_DATA_COLL.find().sort(DATE_KEY, -1).limit(1)
        latest_dt_db = next(cursor)[DATE_KEY]
        if latest_dt.date() == latest_dt_db.date():
            msg = "DB up-to-date"
            app.logger.warning(msg)
        else:
            app.logger.warning("Latest data missing! Updating...")
            df = df[df[DATE_KEY] > latest_dt_db]
            new_records = df.to_dict(orient='records')
            r = PROV_DATA_COLL.insert_many(new_records, ordered=True)
            inserted_ids.extend(r.inserted_ids)
            msg = f"{len(inserted_ids)} docs updated in {PROV_DATA_COLL.name}"
            response["updated"] = True
        response["status"], response["msg"] = "ok", msg
        app.logger.warning(msg)
    except Exception as e:
        err = f"{e}"
        app.logger.error(err)
        response["errors"].append(err)
    response["n_docs"] = len(inserted_ids)
    return response


def update_provincial_breakdown_collection():
    """Update provincial breakdown"""
    n_docs = 0
    response = {"status": "ko", "regions": [], "updated": False, "errors": []}
    updated, msg = False, ""
    try:
        df = load_df(URL_PROVINCIAL)
        pattern = "|".join(PROVINCES)
        df = df[df[PROVINCE_KEY].str.contains(pattern)]
        df = augment_provincial_df(df)
        breakdowns = build_provincial_breakdowns(df)
        for b in breakdowns:
            _filter = {REGION_KEY: b[REGION_KEY]}
            update = {"$set": b}
            res = PROV_BREAKDOWN_COLL.update_one(_filter, update, upsert=True)
            if res.modified_count:
                n_docs += 1
                response["regions"].append(b[REGION_KEY])
                response["n_docs"] = n_docs
                response["updated"] = res.acknowledged
                updated = True
        msg = f"Updated {n_docs} docs in {PROV_BREAKDOWN_COLL.name}"
        if not updated:
            msg = f"Nothing to update in {PROV_BREAKDOWN_COLL.name}"
            app.logger.warning(msg)
        response["status"], response["msg"] = "ok", msg
        app.logger.warning(msg)
    except Exception as e:
        response["errors"].append(f"{e}")
        app.logger.error(f"{e}")
    return response


def update_provincial_series_or_trends_collection(coll_type):
    """Update provincial series or trends collection"""
    n_docs = 0
    response = {"status": "ko", "provs": [], "updated": False, "errors": []}
    updated, msg = False, ""
    df = load_df(URL_PROVINCIAL)
    pattern = "|".join(PROVINCES)
    df = df[df[PROVINCE_KEY].str.contains(pattern)]
    df = augment_provincial_df(df)
    if coll_type == "trends":
        records = build_provincial_trends(df)
        coll = PROV_TRENDS_COLL
    elif coll_type == "series":
        records = build_provincial_series(df)
        coll = PROV_SERIES_COLL
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
        msg = f"Updated {n_docs} docs in {PROV_BREAKDOWN_COLL.name}"
        if not updated:
            msg = f"Nothing to update in {PROV_BREAKDOWN_COLL.name}"
        app.logger.warning(msg)
        response["status"], response["msg"] = "ok", msg
    except Exception as e:
        response["errors"].append(f"{e}")
        app.logger.error(f"{e}")
    return response


def update_vax_collection(summary=False):
    """Update vax / vax_summary collection"""
    response = {"status": "ko", "n_inserted_docs": 0, "errors": []}
    inserted_ids = []
    if not summary:
        collection = VAX_COLL
        df = pd.read_csv(URL_VAX_DATA, parse_dates=[VAX_DATE_KEY])
        df = augment_vax_df(df)
    else:
        collection = VAX_SUMMARY_COLL
        df = pd.read_csv(URL_VAX_SUMMARY_DATA, parse_dates=[VAX_DATE_KEY])
        df = augment_summary_vax_df(df)
    try:
        records_in_db = list(collection.find())
        if records_in_db:
            df_mongo = pd.DataFrame(records_in_db)
            latest_dt_target = df_mongo[VAX_DATE_KEY].max()
            latest_dt_source = df[VAX_DATE_KEY].max()
            if latest_dt_target < latest_dt_source:
                df_to_db = df[df[VAX_DATE_KEY] > latest_dt_target]
                new_records = df_to_db.to_dict(orient='records')
                r = collection.insert_many(new_records, ordered=True)
                inserted_ids.extend(r.inserted_ids)
            elif latest_dt_target == latest_dt_source:
                df = df[df[VAX_DATE_KEY] == latest_dt_source]
                operations = []
                for index, row in df.iterrows():
                    _id = row['_id']
                    new_value = row.to_dict()
                    operations.append(
                        UpdateOne({'_id': _id}, {'$set': new_value})
                    )
                r = collection.bulk_write(operations)
                response['bulk_update'] = r.bulk_api_result
            response["status"] = "ok"
        else:
            msg = f"Filling empty {collection.name}"
            app.logger.warning(msg)
            r = collection.insert_many(df.to_dict(orient='records'))
            inserted_ids.extend(r.inserted_ids)
            response["status"] = "ok"
            response["msg"] = msg
        response["n_inserted_docs"] = len(inserted_ids)
        msg = f"{len(inserted_ids)} docs updated in {collection.name}"
        app.logger.warning(msg)
    except Exception as e:
        app.logger.error(f"While updating vax collection: {e}")
        response["errors"], response["msg"] = f"{e}", f"{e}"
    return response
