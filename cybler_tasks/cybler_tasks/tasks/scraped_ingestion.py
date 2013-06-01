"""
Tasks for ingestion done by web scraping. For the moment this includes:

+backpage.com
+craigslist casual encounters
"""
import os.path
from celery import task
from cybler_tasks.data import feeds, page_parsers
ADULTSEARCH_FILE = os.path.join(os.path.dirname(__file__), "../../static/adultsearch_sources.txt")
CRAIGS_LIST_FILE = os.path.join(os.path.dirname(__file__), "../../static/craigslist_sources.txt")
BACKPAGE_LIST_FILE = os.path.join(os.path.dirname(__file__), "../../static/backpage_sources.txt")
NAUGHTYREVIEW_FILE = os.path.join(os.path.dirname(__file__), "../../static/naughtyreviews_sources.txt")
PROVIDERGUIDE_FILE = os.path.join(os.path.dirname(__file__), "../../static/providerguide_sources.txt")

@task
def ingest_backpage():
    """Ingests all backpage entries
    """
    data = open(BACKPAGE_LIST_FILE).read()
    entries = data.split("\n")
    for entry in entries:
        try:
            url, state, city = entry.split(",")
            feeds.process_feed.delay(url, city, state, page_parsers.BackPageParser)
        except:
            print "Error with one of the feeds"
@task
def ingest_adultsearch():
    """Ingests all adultsearch entries"""
    data = open(ADULTSEARCH_FILE).read()
    entries = data.split("\n")
    for entry in entries:
        try:
            url, state, city = entry.split(",")
            feeds.process_feed.delay(url, city, state, page_parsers.AdultSearchParser)
        except:
            print "Error with one of the feeds"

@task
def ingest_providerguide():
    """Ingests all provider guide content"""
    data = open(PROVIDERGUIDE_FILE).read()
    entries = data.split("\n")
    for entry in entries:
        try:
            url, state, city = entry.split(",")
            feeds.process_feed.delay(url, city, state, page_parsers.AdultSearchParser)
        except:
            print "Error with one of the feeds"
