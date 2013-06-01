"""
Code for massaging data in from requests
"""
from functools import wraps
import http_statuses

def listing_from_params(params):
    """
    Takes a request param and extracts listing data from it.
    """
    #First lets build a basic resource
    resource = {
        "_id": params.get("id"),
        "type": params.get("type"),
        "url": params.get("url"),
        "title": params.get("title"),
        "description": params.get("description"),
        "contact": {
            "city": params.get("city"),
            "state": params.get("state"),
            "country": params.get("country"),
            "phone_number": params.get("phone_number"),
            "email": params.get("email"),
            "address": params.get("address"),
            "zipcode": params.get("zipcode")
            },
        "loc": {
            "lat": float(params["lat"]) if params.get("lat") else None,
            "lon": float(params["lon"]) if params.get("lon") else None
            },
        "images": params["images"].split(",") if params.get("images") else None
    }

    if not resource["_id"]:
        del resource["_id"]

    return resource


    
def rest_handler(formatter=None, return_status=http_statuses.OK):
    """
    Decorator for smoothly handling a REST style request. Optionally
    takes a formatter and a return status (if successful)
    """
    
    def decorator(fn):
        @wraps(fn)    
        def do_request(resource, request):
            returnable = fn(resource, request)
            if formatter:
                returnable = formatter(returnable)
            if return_status:
                request.response.status = return_status
            return returnable
        return do_request
    return decorator
