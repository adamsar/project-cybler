"""This module defines methods for grabbing Listing items as it intended to be a Directory
for the listings"""
from bson.objectid import ObjectId

import logging
log = logging.getLogger(__name__)
COLLECTION = "listing"
CONTACT_COLLECTION = "contactInfo"

def get_listing(db, listing_id):
    """Get listing from mongodb properly massaged for use in python/json"""
    if not isinstance(listing_id, ObjectId):
        try:
            listing_id = ObjectId(listing_id)
        except:
            pass #It's ok, it's not a mongo id
    log.debug("Looking up listing with id: (%s)" % str(listing_id))
    listing = db[COLLECTION].find_one({"_id": listing_id})
    if listing:
        listing["_id"] = str(listing["_id"])
        listing["contact"] = db["contactInfo"].find_one({"_id": ObjectId(listing["contact"])})
        if listing["contact"]:
            listing["contact"]["_id"] = str(listing["contact"]["_id"])
    return listing

    
def get_listings(db, city=None, assumed_address=None, lat=None, lon=None, rows=10, start=0):
    """Gets a bunch of listings based on criteria TBD"""
    #TODO: Assumed address integration
    query = {}
    if city:
        query['city'] = city
    if lat and lon:
        #Search within about a 30 mile square of the specified lat and lon
        query["lat"] = {
            "$gt": lat - .5,
            "$lt": lat + .5            
            }
        query["lon"] = {
            "$gt": lon - .5,
            "$lt": lon + .5            
            }
    if query:
        possible_contacts = [l['_id'] for l in db[CONTACT_COLLECTION].find(query, fields=["_id"])]
        listings = [l for l in db[COLLECTION].find({
            "contact": {
                "$in": possible_contacts                
                }
            }, fields=["_id", "title", "description"])[start:start+rows]]
    else:
        listings = [l for l in db[COLLECTION].find(fields=["_id", "title", "description"])[start:start+rows]]
    for listing in listings:
        listing["_id"] = str(listing["_id"])
    return listings


def remove_listing(db, listing_id):
    """Removes a listing from mongo"""
    if not isinstance(listing_id, ObjectId):
        try:
            listing_id = ObjectId(listing_id)
        except:
            pass #It's ok not to be a mongo id
    log.debug("Removing listing (%s)" % str(listing_id))
    db[COLLECTION].remove({"_id": listing_id})
