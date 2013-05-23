"""
Views pertaining to geo information
"""

from pyramid.view import view_config
from cybler.data import globe
from cybler.lib import http_statuses
import cybler.resources
import logging
log = logging.getLogger(__name__)

@view_config(context=cybler.resources.City, request_method='GET', renderer="json")
def get(city, request):
    """
    Handler for cities queries
    """
    request.response.status = http_statuses.OK
    p = request.params
    params = dict((k, v) for k, v in p.iteritems())
    cities = [c for c in globe.cities_query(request.db, **params)]
    log.debug("Returning (%s) cities" % str(cities))
    return cities
