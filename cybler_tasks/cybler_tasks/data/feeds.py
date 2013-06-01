from celery import task
from cybler_tasks.lib import text
from cybler_tasks.data.cybler_api import CyblerAPI
import feedparser

@task
def ingest_element(listing, Parser):
    """
    Ingests a feed element using the given parser
    """
    parser = Parser(listing)
    parser.ingest()
    

@task
def process_feed(rss_url, city, state, Parser):
    """
    Processes all elements in the url with the specified Parser
    """
    api = CyblerAPI()
    feed = feedparser.parse(rss_url)
    listings = [
        item for item in feed['items'] \
        if not api.get("listing", _id=text.url_to_id(item["id"]))
        ]
    for listing in listings:
        massaged = {
            "id": text.url_to_id(listing["id"]),
            "url": item["link"],
            "city": city,
            "state": state,
            "title": item["title"],
            "description": text.strip_tags(item.get("summary", "")),
            "type": Parser.__type__
        }
        ingest_element.delay(massaged, Parser)
