"""Tools for interfacing with pymongo"""

#This should be set up during config
db = None

def collection(collection_name):
    """Returns a python mongo connection for the specified
    collection name"""
    return db[collection_name]
