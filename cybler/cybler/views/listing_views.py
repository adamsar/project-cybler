from pyramid.view import view_config
import pyramid.httpexceptions as exc

from cybler.data import directory


import cybler.resources
import logging
log = logging.getLogger(__name__)

#RESOURCE - GET:/listing/
@view_config(context=cybler.resources.Listing, request_method='GET', renderer="json")
def get(listing, request):
    """
    Get handler for resources. If there is a resource specified, the context,
    the listing will contain data. If not, get all listings based on query string
    params
    """
    if listing.data is None:
        return directory.get_listings(listing.request.db)
    return listing.data

    
#RESOURCE: POST:/listing/
@view_config(context=cybler.resources.Listing, request_method='POST', renderer="json")
def post(listing, request):
    """
    Make a new listing with POST data.
    Required:
      title
      city
      email or phone_number

    Optional:
      place_name
      country
      description
      address
      lat
      lon
      zip
      image
    """
    
    params = request.params
    #Quick validation, will update late
    if "city" not in params or \
       "title" not in params or \
       ("email" not in params and "phone_number" not in params):
        raise exc.HTTPBadRequest()

    #Extract required parameters
    city = params["city"]
    place_name = params.get("place_name")
    email = params.get("email")
    if email and "@" not in email:
        raise exc.HTTPBadRequest()
        
    phone_number = params.get("phone_number")
    if phone_number:
        try:
            phone_number = int(phone_number)
        except:
            raise exc.HTTPBadRequest()
            
    title = params["title"]

    #Extract optional parameters
    country = params.get("country")
    address = params.get("address")
    lat = params.get("lat")
    if lat:
        try:
            lat = float(lat)
        except:
            lat = None
            
    lon = params.get("lon")
    if lon:
        try:
            lon = float(lon)
        except:
            lon = None
            
    zipcode = params.get("zip")    
    image = params.get("image")
    description = params.get("description")

    contact_id = listing.request.db["contactInfos"].insert({
        "name": place_name,
        "city": city,
        "country": country,
        "zipcode": zipcode,
        "lon": lon,
        "lat": lat,
        "address": address,
        "email": email,
        "phone_number": phone_number
    })
    
    #Add into mongo
    listing_id = listing.collection.insert({
        "title": title,
        "description": description,
        "image": image,
        "contact": contact_id
    })

    log.debug("New listing add with id: (%s)" % str(listing_id))

    #And return
    return directory.get_listing(listing.request.db, listing_id)
