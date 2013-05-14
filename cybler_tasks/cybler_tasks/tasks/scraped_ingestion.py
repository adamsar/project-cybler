"""
Tasks for ingestion done by web scraping. For the moment this includes:

+backpage.com
+craigslist casual encounters
"""
import os.path
from cybler_tasks.data import feed_scraper
CRAIGS_LIST_FILE = os.path.join(os.path.dirname(__file__), "../../static/craigslist_sources.txt")
BACKPAGE_LIST_FILE = os.path.join(os.path.dirname(__file__), "../../static/backpage_sources.txt")

def ingest_backpage():
    """Ingests all backpage entries
    """
    data = open(BACKPAGE_LIST_FILE).read()
    entries = data.split("\n")
    for entry in entries:
        url, state, city = entry.split(",")
        print "Processing %s" % url
        feed_scraper.process_backpage(url, city, state)

    

def ingest_craigslist():
    """Ingests all backpage entries
    """
    data = open(CRAIGS_LIST_FILE).read()
    entries = data.split("\n")
    for entry in entries:
        url, state, city = entry.split(",")
        print "Processing %s" % url
        feed_scraper.process_craigslist(url, city, state)

    
