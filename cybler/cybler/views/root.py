from pyramid.view import view_config
import cybler.resources
from pyramid.httpexceptions import HTTPFound

#this line defines our root view
@view_config(context=cybler.resources.Root)
#this line also attaches /home to our root view
@view_config(context=cybler.resources.Root, name='home')
def my_view(request):
    return "Test"
    

#this handles our 404 not found view
@view_config(context='pyramid.httpexceptions.HTTPNotFound', renderer='templates/404_error.pt')
def not_found(request):
    return{'message': 'Error 404, Page Not Found',
           'cur_page': '', 'page_title': 'Requested Page Not Found'}
