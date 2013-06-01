"""
Formatters for properly returning data
"""

from bson.objectid import ObjectId

def full_listing_json(listing):
    """Does some data massaging for a json"""
    
    if isinstance(listing["_id"], ObjectId):
        listing["_id"] = str(listing["_id"])
    return listing

def listings_json(listings):
    """
    Pared down version of the json
    """
    results = [{
        "_id": str(listing["_id"]),
        "images": listing.get("images", []),
        "title": listing["title"],
        "description": listing["description"],
        "created_on": listing.get("created_on"),
        "type": listing["type"]
        } for listing in listings]
    return {
        "results": results
        }
        

def full_location_json(location):
    """
    Basic location return
    """
    if isinstance(location["_id"], ObjectId):
        location["_id"] = str(location["_id"])
    return location

def locations_list_json(locations):
    """
    Basic list of locational data
    """
    results = [{
        "_id": str(l["_id"]),
        "city": str(l["city"]),
        "state": str(l["state"]),
        } for l in locations]
    return {
        "results": results
        }
