from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import NewRequest
import pymongo

from cybler_mobile.resources import Root

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    config = Configurator(settings=settings, root_factory=Root)
    config.add_static_view('static', 'cybler_mobile:static')
    config.add_static_view('js', 'cybler_mobile:static/js')
    config.add_static_view('img', 'cybler_mobile:static/img')
    config.add_static_view('images', 'cybler_mobile:static/images')
    config.add_route('index', '/')
    config.add_route('location', '/location')
    config.add_route('listings', '/listing')
    config.add_route('listing', '/listing/{listing_id}')
    config.add_route('about', '/about')
    
    # MongoDB
    def add_mongo_db(event):
        settings = event.request.registry.settings
        url = settings['mongodb.url']
        db_name = settings['mongodb.db_name']
        db = settings['mongodb_conn'][db_name]
        event.request.db = db
        
    #CyblerAPI
    def add_cybler_api(event):
        from cybler_mobile.lib import cybler_api
        settings = event.request.registry.settings
        cybler_api.BASE_URL = settings['cybler.api.url']
        event.request.api = cybler_api.CyblerAPI()
        
    db_uri = settings['mongodb.url']
    MongoDB = pymongo.Connection
    if 'pyramid_debugtoolbar' in set(settings.values()):
        class MongoDB(pymongo.Connection):
            def __html__(self):
                return 'MongoDB: <b>{}></b>'.format(self)
    conn = MongoDB(db_uri)
    config.registry.settings['mongodb_conn'] = conn
    config.add_subscriber(add_mongo_db, NewRequest)
    config.add_subscriber(add_cybler_api, NewRequest)
    config.scan('cybler_mobile.views')
    return config.make_wsgi_app()
