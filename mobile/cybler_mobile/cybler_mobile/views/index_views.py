"""
Index views that don't have any information to display whatsoever
"""

from pyramid.view import view_config

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
    locations = request.api.get("location", params={
        "start": 0,
        "rows": 0
    })

    locations = sorted(locations["results"], key=lambda x: x['city'])
    return {
        "locations": locations
    }

@view_config(route_name="about", renderer="about.mako")
def about(request):
    """
    Basic page detailing random links
    """
    
    return {}
