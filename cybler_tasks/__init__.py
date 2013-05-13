"""
Basic configuration for the tasks app
"""
from logging.config import fileConfig
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

    #Setup mongo    
    log.debug("Setting up mongo")
    from cybler_tasks.lib import mongo
    mongo.db = MongoClient(config.get('cybler', 'mongo.host'),
                           config.get('cybler', 'mongo.port'))[config.get('cybler', 'mongo.db')]
    

    
