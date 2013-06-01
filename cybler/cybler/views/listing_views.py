"""Views related to resources.Listing objects. This is all REST stuff, so it should all
return json"""

from pyramid.view import view_config

from cybler.data import directory
from cybler.lib import geolocation
from cybler.lib import http_statuses
from cybler.lib import request_validators
from cybler.lib import formatters


from bson.objectid import ObjectId

import cybler.resources
import logging
log = logging.getLogger(__name__)

#RESOURCE - GET:/listing/
@view_config(context=cybler.resources.Listing, request_method='GET', renderer="json")
@request_validators.rest_handler(return_status=http_statuses.OK)
def get(listing, request):
    """
    Get handler for resources. If there is a resource specified, the context,
    the listing will contain data. If not, get all listings based on query string
    params
    """
    if listing.data is None:
        return formatters.listings_json(
            request.handler.query_from_params(request.params)
            )
    return formatters.full_listing_json(listing.data)
    

#RESOURCE: POST:/listing/
@view_config(context=cybler.resources.Listing, request_method='POST', renderer="json")
@request_validators.rest_handler(formatter=formatters.full_listing_json,
                                 return_status=http_statuses.CREATED)
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
    resource = request_validators.listing_from_params(request.params)
    return request.handler.insert(resource)

    
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
    


