"""
Views for dealing directly with listings
"""

from pyramid.view import view_config
from cybler_mobile.lib import validators, formatters

import pyramid.httpexceptions as exc

@view_config(route_name="listings", renderer="listings.mako")
@validators.locational
def listings(request):
    """
    Main page for displaying a large amount of listings
    """
    p = request.params
    location = request.api.get("city", params={
        "lat": p["lat"],
        "lon": p["lon"]
    })
    if len(location):
        location = location[0] #Grab closest location

    return {
        "location": location
        }


@view_config(route_name="listings.json", renderer="json")
@validators.locational
def listings_json(request):
    """Generates json data for a listing based on query parameters"""
    p = request.params
    params = dict((k, v) for k, v in p.iteritems())
    params["start"] = int(params.get("start", 0))
    params["rows"] = int(params.get("rows", 10))
    listings = request.api.get("listing", params=params)
    
    return [formatters.main_listings_json(listing) for listing in listings]


@view_config(route_name="listing_gallery", renderer="listing_gallery.mako")
def listing_gallery(request):
    """
    A photo gallery page for a request
    """
    listing_id = request.matchdict.get("listing_id")
    if not listing_id:
        exc.HTTPNotFound()
    listing = request.api.get("listing", listing_id)
    return {
        "listing": listing
    }

@view_config(route_name="listing", renderer="listing_show.mako")
def listing(request):
    """
    Single listing full view page
    """
    listing_id = request.matchdict.get("listing_id")
    if not listing_id:
        exc.HTTPNotFound()
    listing = request.api.get("listing", _id=listing_id)
    if not listing:
        exc.HTTPNotFound()
    listing = formatters.full_listing(listing)
    location = request.api.get("city", params={
        "lat": listing["loc"]["lat"],
        "lon": listing["loc"]["lon"]
    })

    return {
        "location": location[0],
        "listing": listing
        }
