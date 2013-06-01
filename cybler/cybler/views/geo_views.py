"""
Views pertaining to geo information
"""

from pyramid.view import view_config
import cybler.resources
from cybler.lib import formatters
import logging
log = logging.getLogger(__name__)

@view_config(context=cybler.resources.Location, request_method='GET', renderer="json")
def get(location, request):
    """
    Handler for location queries
    """
    if location.data:
        return formatters.full_location_json(location.data)
    else:
        return formatters.locations_list_json(
            request.handler.query_from_params(request.params)
        )
