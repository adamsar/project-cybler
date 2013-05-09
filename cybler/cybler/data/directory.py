"""This module defines methods for grabbing Listing items"""
from bson.objectid import ObjectId

import logging
log = logging.getLogger(__name__)

def get_listing(db, listing_id):
    """Get listing from mongodb properly massaged for use in python/json"""
    if not isinstance(listing_id, ObjectId):
        listing_id = ObjectId(listing_id)
    log.debug("Looking up listing with id: (%s)" % str(listing_id))
    listing = db["listing"].find_one({"_id": listing_id})
    if listing:
        listing["_id"] = str(listing["_id"])
        listing["contact"] = db["contactInfos"].find_one({"_id": ObjectId(listing["contact"])})
        listing["contact"]["_id"] = str(listing["contact"]["_id"])
    return listing

    
def get_listings(db):
    """Gets a bunch of listings based on criteria TBD"""
    listings = [l for l in db["listing"].find(fields=['_id', 'title'])[:10]]
    for listing in listings:
        listing["_id"] = str(listing["_id"])
    return [l for l in listings[:10]]
