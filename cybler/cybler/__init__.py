from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import NewRequest
import pymongo

from cybler.resources import Root

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    config = Configurator(settings=settings, root_factory=Root)
#    config.add_view('cybler.views.my_view',
#                    context='cybler:resources.Root',
#                    renderer='cybler:templates/mytemplate.pt')
    config.add_static_view('static', 'cybler:static')
    
    # MongoDB
    def add_mongo_db(event):
        settings = event.request.registry.settings
        url = settings['mongodb.url']
        db_name = settings['mongodb.db_name']
        db = settings['mongodb_conn'][db_name]
        #Make sure we can make geo queries
        from cybler.data import globe, directory
        db[globe.COLLECTION].ensure_index([("loc", pymongo.GEO2D)])
        db[directory.COLLECTION].ensure_index([("loc", pymongo.GEO2D)])
        event.request.db = db
    db_uri = settings['mongodb.url']
    MongoDB = pymongo.Connection
    if 'pyramid_debugtoolbar' in set(settings.values()):
        class MongoDB(pymongo.Connection):
            def __html__(self):
                return 'MongoDB: <b>{}></b>'.format(self)
                
    conn = MongoDB(db_uri)
    config.registry.settings['mongodb_conn'] = conn
    config.add_subscriber(add_mongo_db, NewRequest)
    config.scan('cybler')
    return config.make_wsgi_app()
