"""
Views for dealing directly with listings
"""

from pyramid.view import view_config
from cybler_mobile.lib import validators, formatters

import pyramid.httpexceptions as exc
import urllib

@view_config(route_name="listings", renderer="listings.mako")
@validators.locational
def listings(request):
    """
    Main page for displaying a large amount of listings
    """
    p = request.params
    location = request.api.get("location", params={
        "lat": p["lat"],
        "lon": p["lon"],
        "rows": 1,
        "start": 0
    })
    
    params = dict((k, v) for k, v in p.iteritems())
    if location and  len(location["results"]):
        location = location["results"][0] #Grab closest location
    
    return {
        "location": location,
        "queryParams": urllib.urlencode(params) if params else None
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
    
    return [formatters.main_listings_json(listing) for listing in listings["results"]]


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

    return {
        "listing": listing
        }
