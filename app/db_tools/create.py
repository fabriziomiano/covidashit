"""
DB Recovery
"""
import pandas as pd
from flask import current_app as app

from app.db_tools import (
    nat_data_coll, nat_trends_coll, nat_series_coll, reg_data_coll,
    reg_trends_coll, reg_series_coll, reg_bdown_coll, prov_data_coll,
    prov_trends_coll, prov_series_coll, prov_bdown_coll, vax_admins_coll,
    vax_admins_summary_coll, it_pop_coll
)
from app.db_tools.etl import (
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
            nat_data_coll.drop()
            nat_data_coll.insert_many(national_records, ordered=True)
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
            nat_trends_coll.drop()
            nat_trends_coll.insert_many(national_trends)
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
            nat_series_coll.drop()
            nat_series_coll.insert_one(national_series)
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
            reg_data_coll.drop()
            reg_data_coll.insert_many(regional_records, ordered=True)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_regional_breakdown_collection():
        """Drop and recreate regional breakdown data collection"""
        df = pd.read_csv(
            URL_REGIONAL, parse_dates=[DATE_KEY], low_memory=False)
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_regional_augmented = preprocess_regional_df(df)
        regional_breakdown = build_regional_breakdown(df_regional_augmented)
        try:
            app.logger.info("Creating regional breakdown collection")
            reg_bdown_coll.drop()
            reg_bdown_coll.insert_one(regional_breakdown)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_regional_series_collection():
        """Drop and recreate regional series data collection"""
        df = pd.read_csv(
            URL_REGIONAL, parse_dates=[DATE_KEY], low_memory=False)
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_regional_augmented = preprocess_regional_df(df)
        regional_series = build_regional_series(df_regional_augmented)
        try:
            app.logger.info("Creating regional series collection")
            reg_series_coll.drop()
            reg_series_coll.insert_many(regional_series)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_regional_trends_collection():
        """Drop and recreate regional trends data collection"""
        df = pd.read_csv(
            URL_REGIONAL, parse_dates=[DATE_KEY], low_memory=False)
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_regional_augmented = preprocess_regional_df(df)
        regional_trends = build_regional_trends(df_regional_augmented)
        try:
            app.logger.info("Creating regional trends collection")
            reg_trends_coll.drop()
            reg_trends_coll.insert_many(regional_trends)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_provincial_collections():
        """Drop and recreate provincial collection"""
        df = pd.read_csv(
            URL_PROVINCIAL, parse_dates=[DATE_KEY], low_memory=False)
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_provincial_augmented = preprocess_provincial_df(df)
        provincial_records = df_provincial_augmented.to_dict(orient='records')
        try:
            app.logger.info("Creating provincial")
            prov_data_coll.drop()
            prov_data_coll.insert_many(provincial_records, ordered=True)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_provincial_breakdown_collection():
        """Drop and create provincial breakdown collection"""
        df = pd.read_csv(
            URL_PROVINCIAL, parse_dates=[DATE_KEY], low_memory=False)
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_provincial_augmented = preprocess_provincial_df(df)
        provincial_breakdowns = build_provincial_breakdowns(
            df_provincial_augmented)
        try:
            app.logger.info("Creating provincial breakdowns collection")
            prov_bdown_coll.drop()
            prov_bdown_coll.insert_many(provincial_breakdowns)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_provincial_series_collection():
        """Drop and recreate provincial series data collection"""
        df = pd.read_csv(
            URL_PROVINCIAL, parse_dates=[DATE_KEY], low_memory=False)
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_provincial_augmented = preprocess_provincial_df(df)
        provincial_series = build_provincial_series(
            df_provincial_augmented)
        try:
            app.logger.info("Creating provincial series collection")
            prov_series_coll.drop()
            prov_series_coll.insert_many(provincial_series)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_provincial_trends_collection():
        """Create provincial trends data collection"""
        df = pd.read_csv(
            URL_PROVINCIAL, parse_dates=[DATE_KEY], low_memory=False)
        df.drop(columns=COLUMNS_TO_DROP, inplace=True)
        df_provincial_augmented = preprocess_provincial_df(df)
        provincial_trends = build_provincial_trends(df_provincial_augmented)
        try:
            app.logger.info("Creating provincial trends collection")
            prov_trends_coll.drop()
            prov_trends_coll.insert_many(provincial_trends)
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def create_vax_admins_collection():
        """Create vaccine administrations colleciton"""
        df = pd.read_csv(
            URL_VAX_ADMINS_DATA, parse_dates=[VAX_DATE_KEY], low_memory=False)
        df = preprocess_vax_admins_df(df)
        records = df.to_dict(orient='records')
        try:
            app.logger.info("Creating vax admins collection")
            vax_admins_coll.drop()
            vax_admins_coll.insert_many(records, ordered=True)
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
            vax_admins_summary_coll.drop()
            vax_admins_summary_coll.insert_many(records, ordered=True)
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
            it_pop_coll.drop()
            it_pop_coll.insert_many(records)
        except Exception as e:
            app.logger.error(f"While creating ISTAT Italy population: {e}")
