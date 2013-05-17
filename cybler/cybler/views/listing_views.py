"""Views related to resources.Listing objects. This is all REST stuff, so it should all
return json"""

from pyramid.view import view_config
import pyramid.httpexceptions as exc

from cybler.data import directory
from cybler.lib import geolocation
from cybler.lib import http_statuses

from bson.objectid import ObjectId

import cybler.resources
import datetime
import logging
log = logging.getLogger(__name__)

#RESOURCE - GET:/listing/
@view_config(context=cybler.resources.Listing, request_method='GET', renderer="json")
def get(listing, request):
    """
    Get handler for resources. If there is a resource specified, the context,
    the listing will contain data. If not, get all listings based on query string
    params
    """
    request.response.status = http_statuses.OK
    if listing.data is None:
        params = request.params
        rows = params.get("rows")
        start = params.get("start")
        city = params.get("city")
        query = {
            "city": city
            }
        if rows:
            query["rows"] = int(rows)
        if start:
            query["start"] = int(start)
        return directory.get_listings(listing.request.db, **query)
    return listing.data

#RESOURCE - GET:/listing/debug_list
@view_config(context=cybler.resources.Listing,
             request_method='GET',
             name="debug_list",
             renderer="debug_list.mako")
def debug_list(listing, request):
    """
    Displays a pretty-printed html list for debugging listings
    """
    params = request.params
    rows = params.get("rows")
    start = params.get("start")
    city = params.get("city")
    query = {
        "city": city
    }
    if rows:
        query["rows"] = int(rows)
    if start:
        query["start"] = int(start)
    return {"listings": directory.get_listings(listing.request.db, all_fields=True, **query)}

    
#RESOURCE: POST:/listing/
@view_config(context=cybler.resources.Listing, request_method='POST', renderer="json")
def post(listing, request):
    """    
    Make a new listing with POST data.
    Required:
      title
      city
      email or phone_number

    Optional:
      id
      url
      place_name
      country
      state
      description
      address
      lat
      lon
      zip
      image
      type
    """
    
    params = request.params
    #Quick validation, will update late
    if "city" not in params or \
       "title" not in params or \
       ("email" not in params and "phone_number" not in params):
        raise exc.HTTPBadRequest()

    #Extract required parameters
    city = params["city"]
    place_name = params.get("place_name")
    email = params.get("email")
    if email and "@" not in email:
        raise exc.HTTPBadRequest()
        
    phone_number = params.get("phone_number")
    if phone_number:
        try:
            phone_number = int(phone_number)
        except:
            raise exc.HTTPBadRequest()
            
    title = params["title"]

    #Extract optional parameters
    _id = params.get("id")
    _type = params.get("type")
    url = params.get("url")
    country = params.get("country")
    state = params.get("state")    
    address = params.get("address")
    lat = params.get("lat")
    if lat:
        try:
            lat = float(lat)
        except:
            lat = None
            
    lon = params.get("lon")
    if lon:
        try:
            lon = float(lon)
        except:
            lon = None

    zipcode = params.get("zip")

    #Use google maps api to try to get a lat and lon if they weren't given
    if not lat or not lon:
        assumed_address = geolocation.get_best_guess_address(country=country,
                                                             city=city,
                                                             state=state,
                                                             address=address,
                                                             zipcode=zipcode)
        lat, lon = geolocation.decode_to_latlon(assumed_address)
        
    images = params.get("images")
    description = params.get("description")

    #Add ContactInformation into mongo
    contact_id = listing.request.db["contactInfo"].insert({
        "name": place_name,
        "city": city,
        "country": country,
        "zipcode": zipcode,
        "state": state,
        "lon": lon,
        "lat": lat,
        "address": address,
        "email": email,
        "phone_number": phone_number
    })
    
    #Add into MongoDB
    listing_data = {
        "type": _type,
        "url": url,
        "createdOn": datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        "title": title,
        "description": description,
        "images": images.split(",") if images else None,
        "contact": contact_id
    }
    if _id:
        listing_data["_id"] = str(_id)

    listing_id = listing.collection.insert(listing_data)
    log.debug("New listing add with id: (%s)" % str(listing_id))
    request.response.status = http_statuses.CREATED
    
    #And return    
    return directory.get_listing(listing.request.db, listing_id)

    
#Resource DELETE: /listing/{id}
@view_config(context=cybler.resources.Listing, request_method='DELETE', renderer="json")
def delete(listing, request):
    """Deletes the listing from mongo"""
    if listing.data:
        directory.remove_listing(listing.request.db, listing.data['_id'])
        request.response.status = http_statuses.NO_CONTENT

        
#Resource PUT: /listing/{id}
@view_config(context=cybler.resources.Listing, request_method='PUT', renderer="json")
def put(listing, request):
    """
    Updates listing with same parameters as creating one
    """

    params = request.params
    #Get contact info to update as well
    contact_info = request.db["contactInfo"].find_one({"_id": ObjectId(listing.data["contact"]["_id"])})
    print 

    #Extract parameters, all of them options, updating along the way
    if "title" in params:
        listing.data["title"] = params["title"]

    if "description" in params:
        listing.data["description"] = params["description"]

    if "image" in params:
        listing.data["image"] = params["image"]

    #Now do an update for contact information. Will need to call out to google maps
    if "phone_number" in params:
        contact_info["phone_number"] = params["phone_number"]
    if "email" in params:
        contact_info["email"] = params["email"]

    name = params.get("place_name")
    if name:
        contact_info["name"] = name
    country = params.get("country")
    if country:
        contact_info["country"] = country
    state = params.get("state")
    if state:
        contact_info["state"] = state
    address = params.get("address")
    if address:
        contact_info["address"] = address
    zipcode = params.get("zipcode")
    if zipcode:
        contact_info["zipcode"] = zipcode
    city = params.get("city")
    if city:
        contact_info["city"] = city
    lat, lon = params.get("lat"), params.get("lon")
    try:
        lat, lon = float(lat), float(lon)
    except:
        lat, lon = None, None

    if not lat or not lon:
        assumed_address = geolocation.get_best_guess_address(country=country,
                                                             city=city,
                                                             address=address,
                                                             state=state,
                                                             zipcode=zipcode)
        lat, lon = geolocation.decode_to_latlon(assumed_address)
    request.db["contactInfo"].save(contact_info)
    listing.collection.save(listing.data)

    listing.data["contact"] = contact_info
    contact_info["_id"] = str(contact_info["_id"])
    request.response.status = http_statuses.ACCEPTED
    return listing.data
    


