"""
A library to assist with geolocational centric tasks. Most of these will be
calls out to the googlemaps api
"""

from httplib2 import Http
from urllib import urlencode

import json
import logging
log = logging.getLogger(__name__)

#Base url to for the google maps Geocode link. Can look up a places geo
#info with this (like lat and lon)
GOOGLE_MAPS_GEOCODE = "http://maps.google.com/maps/api/geocode/json"

def get_entry(address):
    """
    Returns the raw results for a look up based on an address
    """
    h = Http()
    url_params = {
        'address': address,
        'sensor': 'false',
    }    

    url = "%s?%s" % (GOOGLE_MAPS_GEOCODE, urlencode(url_params))
    log.debug("Making a geolocation lookup for Url(%s)" % url)
    response, content = h.request(url)
    log.debug("Got back: Response(%s) and Content(%s)" % (str(response), str(content)))
    result = json.loads(content)
    if "status" not in result or result["status"] != "OK":
        return
    return result
    

def decode_to_latlon(address):
    """
    Takes a string address and attempts to decode it to some meaningful geolocational
    data
    """
    entry = get_entry(address)
    if not entry:
        return None, None
    else:        
        return entry['results'][0]['geometry']['location']['lat'], entry['results'][0]['geometry']['location']['lng']


def get_best_guess_address(country=None, city=None, state=None, address=None, zipcode=None):
    """
    Assembles given components for an address into a best guess for a displayable address string
    """
    full_address = ""
    if address:
        full_address += address
    if city:
        full_address += " " + city
    if state:
        full_address += " " + state
    if zipcode:
        full_address += " " + zipcode
    if country:
        full_address += " " + country
    return full_address.strip()
