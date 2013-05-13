"""
Basic configuration for the tasks app
"""
from logging.config import fileConfig
from pymongo import MongoClient
import ConfigParser
import io

#This is established during setup_app, to be called by whatever is using the tasks
config = None

def setup_app(config_file):
    """
    Sets up Mongo and anything else necessary to run tasks via a
    python config file
    """
    
    config = ConfigParser.RawConfigParser()
    config.read(config_file)    
    
    #Configure logger
    fileConfig(config_file)
    import logging
    log = logging.getLogger(__name__)

    #Setup internal API
    from cybler_tasks.data import cybler_api
    cybler_api.BASE_URL = config.get("cybler_tasks", "cybler.api.url")

    #Setup mongo    
    log.debug("Setting up mongo")
    from cybler_tasks.lib import mongo
    mongo.db = MongoClient(config.get('cybler_tasks', 'mongo.host'),
                           int(config.get('cybler_tasks', 'mongo.port')))[config.get('cybler_tasks', 'mongo.db')]
    
