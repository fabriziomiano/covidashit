import pandas as pd
from flask import current_app as app

from app.db.collections import NATIONAL_DATA
from config import URL_NATIONAL_DATA, DATE_KEY


def update_national_collection():
    """
    Update national-data collection
    :return: list: inserted IDs
    """
    national_df = pd.read_csv(URL_NATIONAL_DATA)
    national_df[DATE_KEY] = pd.to_datetime(national_df[DATE_KEY])
    national_df['_id'] = national_df[DATE_KEY]
    inserted_ids = []
    records_in_db = list(NATIONAL_DATA.find())
    if records_in_db:
        national_db_df = pd.DataFrame(records_in_db)
        common = national_df.merge(national_db_df, on=[DATE_KEY])
        df_to_db = national_df[(~national_df.data.isin(common.data))]
        if not df_to_db.empty:
            app.logger.info("Updating collection")
            app.logger.info(df_to_db[DATE_KEY])
            new_records = df_to_db.to_dict(orient='records')
            r = NATIONAL_DATA.insert_many(new_records, ordered=True)
            inserted_ids.extend(r.inserted_ids)
        else:
            app.logger.info("Nothing to update: no new national data")
    else:
        app.logger.info("collection empty. Filling it up")
        r = NATIONAL_DATA.insert_many(national_df.to_dict(orient='records'))
        inserted_ids.extend(r.inserted_ids)
    return inserted_ids
