"""
DB Recovery
"""
import pandas as pd
from flask import current_app as app

from app.db_utils import (
    NAT_DATA_COLL, NAT_TRENDS_COLL, NAT_SERIES_COLL, REG_DATA_COLL,
    REG_TRENDS_COLL, REG_SERIES_COLL, REG_BREAKDOWN_COLL, PROV_DATA_COLL,
    PROV_TRENDS_COLL, PROV_SERIES_COLL, PROV_BREAKDOWN_COLL, VAX_ADMINS_COLL,
    VAX_ADMINS_SUMMARY_COLL, IT_POP_COLL
)
from app.db_utils.etl import (
    preprocess_national_df, preprocess_regional_df, preprocess_provincial_df,
    build_national_trends, build_regional_trends, build_provincial_trends,
    build_regional_breakdown, build_provincial_breakdowns,
    build_national_series, build_regional_series, build_provincial_series,
    COLUMNS_TO_DROP, preprocess_vax_admins_df,
    preprocess_vax_admins_summary_df, create_istat_population_df
)
from settings.urls import (
    URL_NATIONAL, URL_REGIONAL, URL_PROVINCIAL, URL_VAX_ADMINS_DATA,
    URL_VAX_ADMINS_SUMMARY_DATA
)
from settings.vars import DATE_KEY, VAX_DATE_KEY


class CollectionCreator:
    """Collection Creator"""

    @staticmethod
    def create_national_collection():
        """Drop and recreate national data collection"""
        df = pd.read_csv(URL_NATIONAL, parse_dates=[DATE_KEY])
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_national_augmented = preprocess_national_df(df)
        national_records = df_national_augmented.to_dict(orient='records')
        try:
            app.logger.info("Creating national collection")
            NAT_DATA_COLL.drop()
            NAT_DATA_COLL.insert_many(national_records, ordered=True)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_national_trends_collection():
        """Drop and recreate national trends data collection"""
        df = pd.read_csv(URL_NATIONAL, parse_dates=[DATE_KEY])
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_national_augmented = preprocess_national_df(df)
        national_trends = build_national_trends(df_national_augmented)
        try:
            app.logger.info("Creating national trends collection")
            NAT_TRENDS_COLL.drop()
            NAT_TRENDS_COLL.insert_many(national_trends)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_national_series_collection():
        """Drop and recreate national series data collection"""
        df = pd.read_csv(URL_NATIONAL, parse_dates=[DATE_KEY])
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_national_augmented = preprocess_national_df(df)
        national_series = build_national_series(df_national_augmented)
        try:
            app.logger.info("Creating national series collection")
            NAT_SERIES_COLL.drop()
            NAT_SERIES_COLL.insert_one(national_series)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_regional_collection():
        """Drop and recreate regional data collection"""
        df = pd.read_csv(URL_REGIONAL, parse_dates=[DATE_KEY])
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_regional_augmented = preprocess_regional_df(df)
        regional_records = df_regional_augmented.to_dict(orient='records')
        try:
            app.logger.info("Creating regional collection")
            REG_DATA_COLL.drop()
            REG_DATA_COLL.insert_many(regional_records, ordered=True)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_regional_breakdown_collection():
        """Drop and recreate regional breakdown data collection"""
        df = pd.read_csv(URL_REGIONAL, parse_dates=[DATE_KEY])
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_regional_augmented = preprocess_regional_df(df)
        regional_breakdown = build_regional_breakdown(df_regional_augmented)
        try:
            app.logger.info("Creating regional breakdown collection")
            REG_BREAKDOWN_COLL.drop()
            REG_BREAKDOWN_COLL.insert_one(regional_breakdown)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_regional_series_collection():
        """Drop and recreate regional series data collection"""
        df = pd.read_csv(URL_REGIONAL, parse_dates=[DATE_KEY])
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_regional_augmented = preprocess_regional_df(df)
        regional_series = build_regional_series(df_regional_augmented)
        try:
            app.logger.info("Creating regional series collection")
            REG_SERIES_COLL.drop()
            REG_SERIES_COLL.insert_many(regional_series)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_regional_trends_collection():
        """Drop and recreate regional trends data collection"""
        df = pd.read_csv(URL_REGIONAL, parse_dates=[DATE_KEY])
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_regional_augmented = preprocess_regional_df(df)
        regional_trends = build_regional_trends(df_regional_augmented)
        try:
            app.logger.info("Creating regional trends collection")
            REG_TRENDS_COLL.drop()
            REG_TRENDS_COLL.insert_many(regional_trends)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_provincial_collections():
        """Drop and recreate provincial collection"""
        df = pd.read_csv(URL_PROVINCIAL, parse_dates=[DATE_KEY])
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_provincial_augmented = preprocess_provincial_df(df)
        provincial_records = df_provincial_augmented.to_dict(orient='records')
        try:
            app.logger.info("Creating provincial")
            PROV_DATA_COLL.drop()
            PROV_DATA_COLL.insert_many(provincial_records, ordered=True)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_provincial_breakdown_collection():
        """Drop and create provincial breakdown collection"""
        df = pd.read_csv(URL_PROVINCIAL, parse_dates=[DATE_KEY])
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_provincial_augmented = preprocess_provincial_df(df)
        provincial_breakdowns = build_provincial_breakdowns(
            df_provincial_augmented)
        try:
            app.logger.info("Creating provincial breakdowns collection")
            PROV_BREAKDOWN_COLL.drop()
            PROV_BREAKDOWN_COLL.insert_many(provincial_breakdowns)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_provincial_series_collection():
        """Drop and recreate provincial series data collection"""
        df = pd.read_csv(URL_PROVINCIAL, parse_dates=[DATE_KEY])
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_provincial_augmented = preprocess_provincial_df(df)
        provincial_series = build_provincial_series(
            df_provincial_augmented)
        try:
            app.logger.info("Creating provincial series collection")
            PROV_SERIES_COLL.drop()
            PROV_SERIES_COLL.insert_many(provincial_series)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_provincial_trends_collection():
        """Create provincial trends data collection"""
        df = pd.read_csv(URL_PROVINCIAL, parse_dates=[DATE_KEY])
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_provincial_augmented = preprocess_provincial_df(df)
        provincial_trends = build_provincial_trends(df_provincial_augmented)
        try:
            app.logger.info("Creating provincial trends collection")
            PROV_TRENDS_COLL.drop()
            PROV_TRENDS_COLL.insert_many(provincial_trends)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_vax_admins_collection():
        """Create vaccine administrations colleciton"""
        df = pd.read_csv(URL_VAX_ADMINS_DATA, parse_dates=[VAX_DATE_KEY])
        df = preprocess_vax_admins_df(df)
        records = df.to_dict(orient='records')
        try:
            app.logger.info("Creating vax admins collection")
            VAX_ADMINS_COLL.drop()
            VAX_ADMINS_COLL.insert_many(records, ordered=True)
        except Exception as e:
            app.logger.error(f"While creating vax admins collection: {e}")

    @staticmethod
    def create_vax_admins_summary_collection():
        """Create vaccine administrations summary colleciton"""
        df = pd.read_csv(
            URL_VAX_ADMINS_SUMMARY_DATA, parse_dates=[VAX_DATE_KEY])
        df = preprocess_vax_admins_summary_df(df)
        records = df.to_dict(orient='records')
        try:
            app.logger.info("Creating vax admins summary collection")
            VAX_ADMINS_SUMMARY_COLL.drop()
            VAX_ADMINS_SUMMARY_COLL.insert_many(records, ordered=True)
        except Exception as e:
            app.logger.error(
                f"While creating vax admins summary collection: {e}")

    @staticmethod
    def create_istat_pop_collection():
        """Create italy population collection from ISTAT data"""
        try:
            pop_df = create_istat_population_df()
            records = pop_df.to_dict(orient='records')
            app.logger.info("Creating ISTAT Italy population collection")
            IT_POP_COLL.drop()
            IT_POP_COLL.insert_many(records)
        except Exception as e:
            app.logger.error(f"While creating ISTAT Italy population: {e}")
