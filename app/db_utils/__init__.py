"""
DB-Utils module
"""
import os

from app import mongo

nat_data_coll = mongo.db[os.environ["NATIONAL_DATA_COLLECTION"]]
nat_trends_coll = mongo.db[os.environ["NATIONAL_TRENDS_COLLECTION"]]
nat_series_coll = mongo.db[os.environ["NATIONAL_SERIES_COLLECTION"]]
reg_data_coll = mongo.db[os.environ["REGIONAL_DATA_COLLECTION"]]
reg_trends_coll = mongo.db[os.environ["REGIONAL_TRENDS_COLLECTION"]]
reg_series_coll = mongo.db[os.environ["REGIONAL_SERIES_COLLECTION"]]
reg_bdown_coll = mongo.db[os.environ["REGIONAL_BREAKDOWN_COLLECTION"]]
prov_data_coll = mongo.db[os.environ["PROVINCIAL_DATA_COLLECTION"]]
prov_trends_coll = mongo.db[os.environ["PROVINCIAL_TRENDS_COLLECTION"]]
prov_series_coll = mongo.db[os.environ["PROVINCIAL_SERIES_COLLECTION"]]
prov_bdown_coll = mongo.db[os.environ["PROVINCIAL_BREAKDOWN_COLLECTION"]]
vax_admins_coll = mongo.db[os.environ["VAX_ADMINS_COLLECTION"]]
vax_admins_summary_coll = mongo.db[os.environ["VAX_ADMINS_SUMMARY_COLLECTION"]]
it_pop_coll = mongo.db[os.environ["ISTAT_IT_POP_COLLECTION"]]
