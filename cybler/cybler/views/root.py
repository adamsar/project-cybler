from pyramid.view import view_config
import cybler.resources
from pyramid.httpexceptions import HTTPFound
import pyramid.httpexceptions as exc

#this line defines our root view
@view_config(context=cybler.resources.Root)
#this line also attaches /home to our root view
@view_config(context=cybler.resources.Root, name='home')
def my_view(request):
    return "Test"
    

#this handles our 404 not found view
@view_config(context=exc.HTTPNotFound, renderer='json')
def not_found(request):
    """Default handler for 404s"""
    request.response.status = 404    
    return {
        "error": "Not found",
        "code": 404,
        "message": "The requested resource was not found"
        }

@view_config(context=exc.HTTPBadRequest, renderer='json')
def bad_request(request):
    """Default handler for 400s"""
    request.response.status = 400
    return {
        "error": "Bad Request",
        "code": 400,
        "message": "The data supplied to complete the request was malformed"
    }
