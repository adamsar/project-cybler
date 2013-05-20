"""This module defines methods for grabbing Listing items as it intended to be a Directory
for the listings"""
from bson.objectid import ObjectId
from cybler.data import globe
import pymongo

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
    return listing

    
def get_listings(db, all_fields=False, city=None,
                 state=None,
                 assumed_address=None,
                 lat=None, lon=None, rows=10, start=0):
    """Gets a bunch of listings based on criteria TBD"""
    #TODO: Assumed address integration
    fields = ["_id", "title", "description", "url", "images"] if not all_fields else ["_id",
                                                                                      "title",
                                                                                      "type",
                                                                                      "images",
                                                                                      "description",
                                                                                      "url"]
    sort = [("createdOn", pymongo.DESCENDING)]
    query = {}
    if city and not lat and not lon:
        city_entry = globe.get_city(db, city, state)
        lat, lon = (city_entry['loc']['lat'], city_entry['loc']['lon'])
    if lat and lon:
        #Search within about a 30 mile square of the specified lat and lon
        query = {
            "loc": {
                "$near": [lat, lon]
                }
            }
        listings = [
            l for l in db[COLLECTION].find(query, fields=fields).sort(sort)[start:start+rows]
        ]
    else:
        listings = [l for l in db[COLLECTION].find(fields=fields).sort(sort)[start:start+rows]]
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

    
def add_listing(db, listing, city=None, state=None):
    """
    Adds a listing to the data. To be stubbed for various permutations
    """
    if not city:
        return

    #Get city information 
    cityEntry = globe.get_city(db, city, state)
    if not cityEntry:
        cityEntry = globe.insert_city(db, city, state)
        cityEntry = globe.get_city(db, city, state)


    listing['loc'] = {
        "lat": cityEntry["loc"]["lat"],
        "lon": cityEntry["loc"]["lon"]
        }
    
    #First check to see if the listing is actually in mongo
    existing_listing = None
    if "_id" in listing:
        existing_listing = db[COLLECTION].find_one({"_id": listing["_id"]})
        if not existing_listing and "url" in listing:
            existing_listing = db[COLLECTION].find_one({"url": listing["url"]})

    if existing_listing:
        #Update the appropriate listings
        if "createdOn" in listing: del listing["createdOn"]
        existing_listing.update(listing)
        db[COLLECTION].save(existing_listing)
        return existing_listing["_id"]
        
    else:
        return db[COLLECTION].insert(listing)
