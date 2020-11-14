from flask import jsonify

from app.api import api
from app.db.update import (
    update_national_collections, update_regional_collections,
    update_provincial_collections
)


@api.route("/update/<coll>", methods=["POST"])
def update_db(coll):
    """
    Trigger db-collection updates
    :param coll: str
    :return: json str
    """
    response = {"status": "ok", "collections_updated": [], "errors": []}
    if coll == "national":
        response = update_national_collections(response)
    if coll == "regional":
        response = update_regional_collections(response)
    if coll == "provincial":
        response = update_provincial_collections(response)
    return jsonify(**response)
