"""
Library for interfacing with the internal API
"""

import json
import logging
import httplib2
import urllib
import urllib2

log = logging.getLogger(__name__)
BASE_URL = None

class CyblerAPI(object):

    def get(self, resource, _id=None, params={}):
        """
        Retrieves a resource on the api.
        """
        suffix = "/%s" % resource if _id is None else "/%s/%s" % (resource, urllib.quote(_id))
        if params:
            suffix += "?%s" % urllib.urlencode(params)
        full_url = "http://" + BASE_URL + suffix
        log.debug("Hitting the internal API for (%s)" % full_url)

        h = httplib2.Http()
        response, content = h.request(full_url)

        if int(response["status"]) == 200:
            log.debug("Got proper response, returning (%s)" % str(content))
            return json.loads(content)

        log.debug("Got bad response (%s), not returning data" % str(response))
        return None

        
    def insert(self, resource, data={}):
        """
        Inserts a resource via the api
        """
        #First remove any blank data
        keys_to_remove = [key for key in data.keys() if not data[key]]
        for key in keys_to_remove: del data[key]
        encoded_data = urllib.urlencode(data)
        full_url = "http://%s/%s" % (BASE_URL, resource)
        log.debug("Inserting a new %s with data %s" % (resource, encoded_data))

        request = urllib2.Request(full_url, encoded_data)
        try:
            response = urllib2.urlopen(request)
        except:
            response = None
        if response and response.code == 201:
            log.debug("Successfully created")
            return json.load(response)
        log.debug("Failed to create resource")
        

    def update(self, resource, _id, data={}):
        """
        Updates a resource with the given data set
        """
        
        encoded_data = urllib.urlencode(data)
        full_url = "http://%s/%s/%s" % (BASE_URL, resource, urllib.quote(_id))
        log.debug("Updating resource (%s) with data (%s)" % (full_url, encoded_data))

        h = httplib2.Http()
        response, content = h.request(full_url, "PUT")

        if int(response["status"]) == 202:
            log.debug("Successfully updated")
            return True
            
        return json.loads(content)

        
    def delete(self, resource, _id):
        """
        Deletes a resource
        """
        full_url = "http://%s/%s/%s" % (BASE_URL, resource, urllib.quote(_id))
        log.debug("Deleting resource at (%s)" % full_url)

        h = httplib2.Http()
        response, content = h.request(full_url, "DELETE")

        if int(response["status"]) == 204:
            log.debug("Successfully deleted")
            return True

        return json.loads(content)

