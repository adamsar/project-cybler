"""
Index views that don't have any information to display whatsoever
"""

from pyramid.view import view_config
from cybler_mobile.lib.cybler_api import CyblerAPI

@view_config(route_name="index", renderer="index.mako")
def splash_page(request):
    """
    The splash page that waits for a user to decide to geolocate or not
    """
    return {}

    
@view_config(route_name="location", renderer="location.mako")
def location(request):
    """
    Displays a list of cities to choose from
    """
    return {
        "cities": request.api.get("city")
    }
