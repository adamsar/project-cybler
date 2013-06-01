import pyramid.httpexceptions as exc
from cybler.data.directory import ListingDirectory
from cybler.data.globe import Globe

import logging
log = logging.getLogger(__name__)

class Root(object):
    __name__ = ''
    __parent__ = None
    
    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        """This looks up the first part of the path
        available resources at this time are:
        
        listing
        account
        """
        log.debug("Root with key: (%s)" % key)
        if key == "listing":
            return Listing(self.request)
        elif key == "location":
            return Location(self.request)
        elif key == "account":
            pass
        #Force a 404 if not a proper resource
        raise KeyError 

        
class MongoResource(object):
    """
    Basic class for a Mongo based resource. Requires each inheriting class
    to specified a __collection__name__ to tie the resource to
    """
    
    __name__ = ''
    __handler__ = None
    __parent__ = Root

    def __init__(self, request, _id=None):        
        self.request = request
        self.request.handler = self.__handler__(request.db)
        self.data = None
        if _id:
            try:
                self.data = self.request.handler.get(_id)
            except:
                self.data = None
            if not self.data:
                raise exc.HTTPNotFound() 

class Listing(MongoResource):
    """
    A listing for a contact stored within Mongo
    """
    __name__ = ''
    __handler__ = ListingDirectory
    __parent__ = Root
    __collection_name__ = "listing"

    def __getitem__(self, listing_id):
        if listing_id:
            return Listing(self.request, _id=listing_id)
        raise KeyError
    
        
class Location(MongoResource):
    """
    A location that's in the DB
    """
    __name__ = ''
    __handler__ = Globe
    __parent__ = Root
    __collection_name__ = "cities"

    def __getitem__(self, location_id):
        if location_id:
            return Location(self.request, _id=location_id)
        raise KeyError
