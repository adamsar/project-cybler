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

    
def get_listings(db, all_fields=False, rows=10, start=0, **query):
    """Gets a bunch of listings based on criteria TBD"""
    fields = ["_id",  "createdOn", "title",  "description",  "url", "images"]
    if all_fields: fields.append("type")
    sort = [("createdOn", pymongo.DESCENDING)]
    if "city" in query and (not "lat" in query or not "lon" in query):
        city_entry = globe.get_city(db, query["city"], query.get("state"))
        lat, lon = (city_entry['loc']['lat'], city_entry['loc']['lon'])
    elif "lat" in query and "lon" in query:
        lat, lon = query['lat'], query['lon']
        q = {
            "loc": {
                "$within": {
                    "$center": [[lat, lon], .5]
                }
            }
        }
        q.update(query)
        if "city" in q:
            del q["city"]
        if "lat" in q:
            del q["lat"]
        if "lon" in q:
            del q["lon"]
        log.debug("Query (%s)" % str(q))
        results = db[COLLECTION].find(q, fields=fields)
    elif query:        
        log.debug("Query (%s)" % str(query))
        results = db[COLLECTION].find(query, fields=fields)
    else:
        log.debug("No query")
        results = db[COLLECTION].find(fields=fields)

    listings = [l for l in results.limit(rows).skip(start)]
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
