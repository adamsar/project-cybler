from cybler.data import directory
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
        elif key == "account":
            return Account(self.request)
        #Force a 404 if not a proper resource
        raise KeyError 

        
class MongoResource(object):
    """
    Basic class for a Mongo based resource. Requires each inheriting class
    to specified a __collection__name__ to tie the resource to
    """
    
    __name__ = ''
    __parent__ = Root

    def __init__(self, request, _id=None):
        self.request = request
        self.collection = self.request.db[self.__collection_name__]
        self.data = None
        
        if _id:
            self.data = directory.get_listing(self.request.db, _id)
            if not self.data:
                #Kick a 404 out if you try to get a non-existent resource
                raise KeyError
            
        
class Listing(MongoResource):
    """
    A listing for a contact stored within Mongo
    """
    __name__ = ''
    __parent__ = Root
    __collection_name__ = "listing"

    def __getitem__(self, listing_id):
        if listing_id:
            return Listing(self.request, _id=listing_id)
        
