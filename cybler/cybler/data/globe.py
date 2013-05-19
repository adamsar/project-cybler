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
import os.path
from cybler.lib import geolocation

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

def get_city(db, city, state):
    """
    Returns a city based on a name
    """
    
    #Start with just a city name 
    query = {
        "city": city.lower()
        }

    if state and  len(state) > 2:
        state = STATESF.get(state.lower())
        if state:
            query["state"] = state
            
    return db[COLLECTION].find_one(query)

    
def insert_city(db, city, state):
    """
    Attempted to extract a sity from geolocation lite and insert into mongodb
    """
    if state and len(state) > 2:        
        state = STATESF.get(state.lower())

    all_entries = open(GEODATA_FILE).read().lower().split("\n")
    submitable = {}
    for entry in all_entries:
        if not len(entry.strip()):
            continue
        try:
            locId, country, region, cityName, postalCode, latitude, longitude, metroCode, areaCode = entry.replace('"', "").split(",")
        except:
            print "aborting"
            continue
        if state and region == state and cityName == city:
            submitable = {
                "country": country.lower(),
                "city": city.lower(),
                "state": state,
                "lat": float(latitude),
                "lon": float(longitude)
                }
            break
            
        #Best guess if no state
        if not state and cityName == city:
            submitable = {
                "country": country.lower(),
                "city": city.lower(),
                "state": state,
                "loc": {
                    "lat": float(latitude),
                    "lon": float(longitude)
                    }
                }
            break
            
    #Use google to look things up if you can determine where the city is        
    if not submitable:
        latitude, longitude = geolocation.decode_to_latlon(geolocation.get_best_guess_address(city=city,
                                                                                              state=state))
        submitable = {
            "country": None,
            "city": city,
            "state": state,
            "loc": {
                "lat": float(latitude),
                "lon": float(longitude)
                }
            }
            
    return db[COLLECTION].insert(submitable)
        
