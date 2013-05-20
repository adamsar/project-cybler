"""
Views for dealing directly with listings
"""

from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
from pyramid.view import view_config
from cybler_mobile.lib.cybler_api import CyblerAPI
from cybler_mobile.lib import text


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

