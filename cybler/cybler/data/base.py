"""
Base data handler
"""

import logging
from bson.objectid import ObjectId
log = logging.getLogger(__name__)

class CyblerResourceHandler(object):
    """
    A resource within the cybler system
    """
    __resource__ = ""
    __collection__ = ""

    def __init__(self, db):
        """
        Basic constructor for a CyberResourceHandler object. Binds a mongo
        db for use in future calls
        """
        self.db = db
        self.store = self.db[self.__collection__]

        
    def get(self, _id):
        """
        Returns a single resource based on id
        """
        log.debug("Looking up %s with id: (%s)" % (self.__resource__, str(_id)))
        #First check to see if the resoure is trying to use object ids
        if not isinstance(_id, ObjectId):
            try:
                _id = ObjectId(_id)
            except:
                #Continue on, non-ObjectIds are fine
                pass
        listing = self.store.find_one({"_id": _id})

        return listing

        
    def query(self, start=0, rows=10, fields=[], distinct_field=None,
              sort=None, no_nulls=False, **query):
        """
        Basic query functionality. no_nulls specifies whether to remove possible
        nulls from the query or not
        """
        if no_nulls:
            deletes = [key for key, value in query.iteritems() if not value]
            for removable_key in deletes:
                del query[removable_key]
        
        log.debug("Making query for %s: params: (%s), start: %s, rows: %s, fields: %s" %
                  (self.__resource__, str(query), start, rows, fields))
        results = []
        

        if distinct_field:
            results = self.store.distinct(distinct_field, query)
        else:
            if fields:
                results = self.store.find(query, fields=fields)
            else:
                results = self.store.find(query)  

        if sort:
            results = results.sort(sort)
            
        if start != None and rows:
            results = results.limit(int(rows)).skip(int(start))

        return results

        
    def remove(self, _id):
        """
        Removes a listing from mongo
        """
        if not isinstance(_id, ObjectId):
            try:
                _id = ObjectId(_id)
            except:
                #A nonObjectId is fine for some resources
                pass
        log.debug("Removing %s (%s)" % (self.__resource__, str(_id)))
        self.store.remove({"_id": _id})

    def insert(self, resource):
        """
        Inserts a new resource into mongo
        """
        
        #Check if exists
        if "_id" in resource:
            existing_listing = self.get(resource["_id"])
            if existing_listing:
                existing_listing.update(resource)
                self.update(existing_listing)
                return resource

        log.debug("Inserting %s (%s)" % (self.__resource__, str(resource)))
        return self.get(self.store.insert(resource))
