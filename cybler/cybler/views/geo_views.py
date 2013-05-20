"""
Views pertaining to geo information
"""

from pyramid.view import view_config
from cybler.data import globe
from cybler.lib import http_statuses
import cybler.resources

@view_config(context=cybler.resources.City, request_method='GET', renderer="json")
def get(city, request):
    """
    Handler for cities
    """
    request.response.status = http_statuses.OK
    return globe.all_cities(request.db)
