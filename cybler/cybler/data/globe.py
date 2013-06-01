"""
Acts as an interface for querying locations, cities, addresses, etc.

Deals directly with mongo
"""
"""
{
  _id: standard,
  name: "Dallas",
  state: "TX",
  country: "US",
  loc: {lat: 26.3453,
        lon: 26.3453}
}
"""

from cybler.lib import geolocation
from cybler.data.base import CyblerResourceHandler
import os.path
import logging

COLLECTION = "cities"

STATESAB = {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'
    }

#List of all abbreviations to states, mapped
STATESAB = dict((key.lower(), value.lower()) for key, value in STATESAB.iteritems())
#And the reverse
STATESF = dict((value, key) for key, value in STATESAB.iteritems())

#Houses that file that contains all geo locational information
GEODATA_FILE = os.path.join(os.path.dirname(__file__), "../../geobootstrap/geodata.csv")


log = logging.getLogger(__name__)
    
class Globe(CyblerResourceHandler):
    """
    Handler for location based Queries
    """
    __resource__ = "location"
    __collection__ = "location"

    def _from_geolite(self, city=None, state=None, country=None):
        """
        Grabs entry from geolite file
        """
        def city_validate(candidate):
            return candidate["city"] == city
        def state_validate(candidate):
            return candidate["state"] == state
        def country_validate(candidate):
            return candidate["country"] == country
        pipeline = []
        if city: pipeline.append(city_validate)
        if state: pipeline.append(state_validate)
        if country: pipeline.append(country_validate)
        
        for entry in open(GEODATA_FILE).read().lower().split("\n"):
            #24327,"US","MT","Baker","59313",46.2835,-104.2803,687,406
            if not len(entry.strip()):
                continue
            try:
                locId, country, region, cityName, postalCode, latitude, longitude, metroCode, areaCode = entry.replace('"', "").split(",")
            except:
                log.error("Error trying to unmarshal entry")
                continue
            entry={
                "city": cityName.lower(),
                "state": state.lower(),
                "country": country.lower()
            }
            valid = reduce(lambda x, y: x and y, map(lambda fn: fn(entry), pipeline))
            if valid:
                entry.update({
                    "loc": {
                        "lat": float(latitude),
                        "lon": float(longitude)
                    },
                    "postal_code": postalCode,
                    "area_code": areaCode
                })
                return entry


    def _from_googlemaps(self, **params):
        """
        Use google maps API to lookup a location. This is intended to be a
        fallback for geolite look ups
        """
        assumed_address = geolocation.get_best_guess_address(**params)
        google_maps_entry = geolocation.get_entry(assumed_address)
        if not google_maps_entry:
            return
        lat = float(google_maps_entry["results"][0]["geometry"]["location"]["lat"])
        lon = float(google_maps_entry["results"][0]["geometry"]["location"]["lng"])
        components = google_maps_entry["results"][0]["address_components"]
        city = components[0]["long_name"].lower()
        state = None
        if len(components) > 2:
            for comp in components:
                if "administrative_area_level_1" in comp:
                    state = comp["short_name"].lower()
        country = components[len(components) - 1]["long_name"].lower()
        return {
            "city": city,
            "state": state,
            "country": country,
            "loc": {
                "lat": lat,
                "lon": lon
            },
            "postal_code": None,
            "area_code": None
        }
        
        
    def generate_location(self, city=None, state=None, country=None):
        """Generates a location using first the internal geo lookup and
        Google Maps if all else fails"""
        if not city:
            #Can't do anything without a city, too wide an area
            return
            
        #American states should be abbreviated if possible
        if state:
            state = state.lower()
            if len(state) > 2 and state in STATESF:
                state = STATESF[state]
        
        entry = self._from_geolite(city=city, state=state, country=country)
        if not entry:
            entry = self._from_googlemaps(city=city, state=state, country=country)
        if not entry:
            return
        self.insert(entry)

    def query_from_params(self, params):
        """
        Builds and executes a query based on the parameters that
        are passed into from the app
        """
        q = {}
        start, rows = 0, 10
        if "start" in params:
            start = int(params["start"])
        if "rows" in params:
            rows = int(params["rows"])

        if "lat" in params and "lon" in params:
            lat = float(params["lat"])
            lon = float(params["lon"])
            q["loc"] = {
                "$near": [lat, lon]
                }
        for atr in ["city", "state", "country"]:
            if atr in params:
                q[atr] = params[atr]
        return self.query(start=start, rows=rows, **q)
