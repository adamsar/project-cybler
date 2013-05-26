"""
Validators used for dealing with requests.  If something fails to validate, a
403 Bad Request is typically thrown
"""
import pyramid.httpexceptions as exc

def locational(fn):
    """A decorator that enforces that the call is locational and requires
    a lat and lon in the query parameters
    """
    def check(request):
        p = request.params
        if "lat" not in p or "lon" not in p:
            exc.HTTPNotFound()
        return fn(request)
    return check
