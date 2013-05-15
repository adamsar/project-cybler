"""
Feed parsing using feedparser and some url scraping
"""

from cybler_tasks.lib import geolocation, text, scraper
from cybler_tasks.data.cybler_api import CyblerAPI

from bs4 import BeautifulSoup

import urllib
import httplib2
import feedparser
import logging

log = logging.getLogger(__name__)

LISTING_COLLECTION = "listing"
CONTACT_COLLECTION = "contactInfo"

def process_backpage(rss_url, city, state):
    """
    Processes a backpage rss feed. Requires a link to the rss_url,
    what city and what state it's in
    """

    city_address = geolocation.get_best_guess_address(city=city, state=state)
    city_lat, city_lon = geolocation.decode_to_latlon(city_address)

    #The "reduce" part of map-reduce. Construct listing from it's parts and
    #save via the API
    def build_listing(item, actual_listing):
        if not item or not actual_listing:
            log.debug("Error processing link, not adding new entry")
            return None

        #Lets start scraping, we need the posting body, location data, and image data
        soup = BeautifulSoup(actual_listing)
        images = soup.find("ul", {"id": "viewAdPhotoLayout"})
        if images:
            images = images.find_all("li")
            images = [i.find("img").attrs["src"] for i in images]
        
        listing_body = soup.find("div", "postingBody")
        if listing_body:
            listing_body = "".join([str(i.encode("utf-8")) for i in listing_body.contents])
            item['description'] = listing_body
            
        checkable_containers = soup.find_all("div")
        location_data = ""
        for container in checkable_containers:
            if "Location" in container.contents:
                location_data = contain.contents.replace("Location:", "")

#        emails = text.extract_emails(item['summary'])
        phone_number = text.extract_phone_number(item['description'])
        if not phone_number:
            if listing_body:
                phone_number = text.extract_phone_number(listing_body)

        #Now assemble and submit to the API
        if location_data:
            #TODO massage this later
            item['address'] = location_data

        lat, lon = None, None
        try:
            assumed_address = geolocation.get_best_guess_address(country="USA",
                                                                 address=location_data)
            lat, lon = geolocation.decode_to_latlon(assumed_address)
        except:
            pass
        if lat and lon:
            item['lat'] = lat
            item['lon'] = lon
            
        if images:
            item['images'] = ",".join(images)
        if phone_number:
            item['phone_number'] = phone_number
            
        #Massage any unicode data
        item['title'] = item['title'].encode('utf-8')
        item['description'] = item['description'].encode('utf-8')
        return CyblerAPI().insert("listing", data=item)            
            

    #Return data on all listings in feed if they are not in mongo
    def get_listing(item):
        #If not, then update
        h = httplib2.Http()
        response, content = h.request(item['link'])
        if int(response['status']) != 200:
            return (None, None)
        data = {
            "id": text.url_to_id(item['id']),
            "url": item['link'],
            "city": city,
            "state": state,
            "title": item["title"],
            "description": item.get("summary", ""),
            "type": "backpage"
            }
        return (data, content)

    #Grab un processed listings
    feed = feedparser.parse(rss_url)
    new_listings = [item for item in feed['items'] \
                    if not CyblerAPI().get("listing", _id=text.url_to_id(item['id']))]

    #And the main algorithm, build listings with feed items and combine them with scraped data
    #then persist to mongo
    new_listings = map(get_listing, new_listings)
    listings = []
    for data, actual_listing in new_listings:
        listing = build_listing(data, actual_listing)
        if listing:
            listings.append(listing)

    return listings

    
def process_craigslist(rss_url, city, state):
    """
    Processes and generates listings for a craiglist casual encounters
    page
    """
    city_address = geolocation.get_best_guess_address(city=city, state=state)
    city_lat, city_lon = geolocation.decode_to_latlon(city_address)

    
    #The "reduce" part of map-reduce. Construct listing from it's parts and
    #save via the API
    def build_listing(item, actual_listing):
        if not item or not actual_listing:
            log.debug("Error processing link, not adding new entry")
            return None

        #Lets start scraping, we need the posting body, location data, and image data
        soup = BeautifulSoup(actual_listing)
        images = [img.attrs['src'].replace("thumb/", "") for img in soup.find_all('img') if "thumb" in img.attrs['src']]
        listing_body = soup.find("section", {"id": "postingbody"})
        if listing_body:
            listing_body = "".join([str(i.encode("utf-8")) for i in listing_body.contents])
            item['description'] = listing_body
        else:
            listing_body = ""
            
        checkable_containers = soup.find("ul", "blurbs")
        if checkable_containers:
            checkable_containers = checkable_containers.find_all("li")
        else:
            checkable_containers = []
            
        location_data = ""
        for container in checkable_containers:
            if "Location" in container.contents[0]:
                location_data = container.contents[0].replace("Location:", "")

        links = soup.find_all("a")
        for link in links:
            if "mailto" in str(link.attrs['href']):
                item['email'] = link.contents[0]
                
                
        phone_number = text.extract_phone_number(item['description'])
        if not phone_number:
            phone_number = text.extract_phone_number(str(listing_body))

        #Now assemble and submit to the API
        if location_data:
            #TODO massage this later
            item['address'] = location_data

        lat, lon = None, None
        try:
            assumed_address = geolocation.get_best_guess_address(country="USA",
                                                                 address=location_data)
            lat, lon = geolocation.decode_to_latlon(assumed_address)
        except:
            pass
        if lat and lon:
            item['lat'] = lat
            item['lon'] = lon
            
#        if images:
#            item['images'] = ",".join(images)
        if phone_number:
            item['phone_number'] = phone_number
            
        #Massage any unicode data
        item['title'] = item['title'].encode('utf-8')
        item['images'] = ",".join(images)
        return CyblerAPI().insert("listing", data=item)            
            

    #Return data on all listings in feed if they are not in mongo
    def get_listing(item):
        #If not, then update
        content = urllib.urlopen(item['link']).read()
        data = {
            "id": text.url_to_id(item['id']),
            "url": item['link'],
            "city": city,
            "state": state,
            "title": item["title"],
            "description": item["summary"],
            "type": "craigslist"
            }
        return (data, content)

    #Grab un processed listings
    feed = feedparser.parse(rss_url)
    new_listings = [item for item in feed['items'] \
                    if not CyblerAPI().get("listing", _id=text.url_to_id(item['id']))]

    #And the main algorithm, build listings with feed items and combine them with scraped data
    #then persist to mongo
    new_listings = map(get_listing, new_listings)
    listings = []
    for data, actual_listing in new_listings:
        listing = build_listing(data, actual_listing)
        if listing:
            listings.append(listing)

    return listings
