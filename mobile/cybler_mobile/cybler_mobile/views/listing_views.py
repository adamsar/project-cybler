"""
Views for dealing directly with listings
"""

from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
from pyramid.view import view_config
from cybler_mobile.lib.cybler_api import CyblerAPI
from cybler_mobile.lib import text
import pyramid.httpexceptions as exc

@view_config(route_name="listings", renderer="listings.mako")
def listings(request):
    """
    Main page for displaying a large amount of listings
    """
    p = request.params
    if "lat" not in p or "lon" not in p:
        return HTTPFound(route_url("location"))
    listings = request.api.get("listing", params={"lat": p["lat"], "lon": p["lon"]})
    for listing in listings:
        listing["description"] = text.smart_truncate(listing["description"])
    return {
        "listings": listings
        }

@view_config(route_name="listing", renderer="listing.mako")
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
    return {
        "listing": listing
        }
