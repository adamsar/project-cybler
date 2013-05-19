"""
Tasks for ingestion done by web scraping. For the moment this includes:

+backpage.com
+craigslist casual encounters
"""
import os.path
from celery import task
from cybler_tasks.data import feed_scraper
ADULTSEARCH_FILE = os.path.join(os.path.dirname(__file__), "../../static/adultsearch_sources.txt")
CRAIGS_LIST_FILE = os.path.join(os.path.dirname(__file__), "../../static/craigslist_sources.txt")
BACKPAGE_LIST_FILE = os.path.join(os.path.dirname(__file__), "../../static/backpage_sources.txt")
NAUGHTYREVIEW_FILE = os.path.join(os.path.dirname(__file__), "../../static/naughtyreviews_sources.txt")

@task
def ingest_backpage():
    """Ingests all backpage entries
    """
    data = open(BACKPAGE_LIST_FILE).read()
    entries = data.split("\n")
    for entry in entries:
        url, state, city = entry.split(",")
        print "Processing %s" % url
        feed_scraper.process_backpage.delay(url, city, state)

@task
def ingest_craigslist():
    """Ingests all backpage entries
    """
    data = open(CRAIGS_LIST_FILE).read()
    entries = data.split("\n")
    for entry in entries:
        url, state, city = entry.split(",")
        print "Processing %s" % url
        feed_scraper.process_craigslist.delay(url, city, state)

    
@task
def ingest_adultsearch():
    """Ingests all adultsearch entries"""
    data = open(ADULTSEARCH_FILE).read()
    entries = data.split("\n")
    for entry in entries:
        url, state, city = entry.split(",")
        feed_scraper.process_adultsearch.delay(url, city, state)


@task
def ingest_naughtyreview():
    """Ingests all naughty review feeds"""
    data = open(NAUGHTYREVIEW_FILE).read()
    entries = data.split("\n")
    for entry in entries:
        url, state, city = entry.split(",")
        feed_scraper.process_naughtyreview.delay(url, city, state)        
