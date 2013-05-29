"""
Feed parsing using feedparser and some url scraping
"""

from celery import task
from cybler_tasks.lib import geolocation, text
from cybler_tasks.data.cybler_api import CyblerAPI

from bs4 import BeautifulSoup

import urllib
import feedparser
import logging

log = logging.getLogger(__name__)

LISTING_COLLECTION = "listing"
CONTACT_COLLECTION = "contactInfo"

@task
def build_listing_backpage(item):

        #Lets start scraping, we need the posting body, location data, and image data
        soup = BeautifulSoup(urllib.urlopen(item['url']).read())
        image_container = soup.find("ul", {"id": "viewAdPhotoLayout"})
        images = []
        if image_container:
            images = image_container.find_all("img")
            images = [text.image_format(i.attrs["src"]) for i in images]
        if not images:
            return #No images, no dice
        
        listing_body = soup.find("div", "postingBody")
        if listing_body:
            listing_body = "".join([unicode(i) for i in listing_body.contents])
            item['description'] = listing_body
            
        checkable_containers = soup.find_all("div")
        location_data = ""
        for container in checkable_containers:
            if "Location" in container.contents:
                location_data = container.contents.replace("Location:", "")

        phone_number = text.extract_phone_number(item['description'])
        if not phone_number:
            if listing_body:
                phone_number = text.extract_phone_number(listing_body)

        #Now assemble and submit to the API
        if location_data:
            #TODO massage this later
            item['address'] = location_data
            
        if images:
            item['images'] = ",".join(images)
        if phone_number:
            item['phone_number'] = phone_number
            
        #Massage any unicode data
        item['title'] = item['title']
        item['description'] = text.strip_tags(item['description'])
        return CyblerAPI().insert("listing", data=item)            
    

@task
def process_backpage(rss_url, city, state):
    """
    Processes a backpage rss feed. Requires a link to the rss_url,
    what city and what state it's in
    """

    city_address = geolocation.get_best_guess_address(city=city, state=state)
    city_lat, city_lon = geolocation.decode_to_latlon(city_address)

    #Return data on all listings in feed if they are not in mongo
    def get_listing(item):
        data = {
            "id": text.url_to_id(item['id']),
            "url": item['link'],
            "city": city,
            "state": state,
            "title": item["title"],
            "description": item.get("summary", ""),
            "type": "backpage"
            }
        return data

    #Grab un processed listings
    feed = feedparser.parse(rss_url)
    new_listings = [item for item in feed['items'] \
                    if not CyblerAPI().get("listing", _id=text.url_to_id(item['id']))]

    #And the main algorithm, build listings with feed items and combine them with scraped data
    #then persist to mongo
    new_listings = map(get_listing, new_listings)
    listings = []
    for data in new_listings:
        build_listing_backpage.delay(data)

@task
def build_listing_craigslist(item):        
        #Lets start scraping, we need the posting body, location data, and image data
        soup = BeautifulSoup(urllib.urlopen(item['url']).read())
        images = [img.attrs['src'].replace("thumb/", "") for img in soup.find_all('img') if "thumb" in img.attrs['src']]
        listing_body = soup.find("section", {"id": "postingbody"})
        if listing_body:
            listing_body = "".join([str(i) for i in listing_body.contents])
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
            
        if phone_number:
            item['phone_number'] = phone_number
            
        #Massage any unicode data
        item['title'] = item['title']
        item['images'] = ",".join(images)
        return CyblerAPI().insert("listing", data=item)            
    
    
@task    
def process_craigslist(rss_url, city, state):
    """
    Processes and generates listings for a craiglist casual encounters
    page
    """
    city_address = geolocation.get_best_guess_address(city=city, state=state)
    city_lat, city_lon = geolocation.decode_to_latlon(city_address)

    #Return data on all listings in feed if they are not in mongo
    def get_listing(item):
        #If not, then update
        data = {
            "id": text.url_to_id(item['id']),
            "url": item['link'],
            "city": city,
            "state": state,
            "title": item["title"],
            "description": item["summary"],
            "type": "craigslist"
            }
        return data

    #Grab un processed listings
    feed = feedparser.parse(rss_url)
    new_listings = [item for item in feed['items'] \
                    if not CyblerAPI().get("listing", _id=text.url_to_id(item['id']))]

    #And the main algorithm, build listings with feed items and combine them with scraped data
    #then persist to mongo
    new_listings = map(get_listing, new_listings)
    for data in new_listings:
        build_listing_craigslist.delay(data)

        
@task
def build_listing_adultsearch(listing):
    #Lets start scraping, we need the posting body, location data, and image data
    soup = BeautifulSoup(urllib.urlopen(listing['url']).read())
    try:
        number = str(soup.find("h1", "name").find("span").contents[0])
        number = text.extract_phone_number(number)
    except:
        number = None

    try:
        images = soup.find("div", {"id": "gallery"}).find_all("img")
        images = [text.image_format(i.attrs['src']) for i in images]
    except:
        return #No images, no dice
    if number:
        listing["phone_number"] = number
    if images:
        listing["images"] = ",".join(images)
    return CyblerAPI().insert("listing", data=listing)     
    
@task
def process_adultsearch(rss_url, city, state):
    """Process adultsearch rss feeds"""
    city_address = geolocation.get_best_guess_address(city=city, state=state)
    city_lat, city_lon = geolocation.decode_to_latlon(city_address)

    #Return data on all listings in feed if they are not in mongo
    def get_listing(item):
        #If not, then update
        data = {
            "id": text.url_to_id(item['id']),
            "url": item['link'],
            "city": city,
            "state": state,
            "lat": city_lat,
            "lon": city_lon,
            "title": item["title"],
            "description": text.strip_tags(item["summary"]),
            "type": "adultsearch"
            }
        return data

    #Grab un processed listings
    feed = feedparser.parse(urllib.urlopen(rss_url).read())
    new_listings = [item for item in feed['items'] \
                    if not CyblerAPI().get("listing", _id=text.url_to_id(item['id']))]

    #And the main algorithm, build listings with feed items and combine them with scraped data
    #then persist to mongo
    new_listings = map(get_listing, new_listings)
    for data in new_listings:
        build_listing_adultsearch.delay(data)

@task
def build_naughtyreviews(listing):
    """
    Scrapes and completes a naughty review listing. Then updates the api with the data
    """
    
    soup = BeautifulSoup(urllib.urlopen(listing['url']).read())
    
    #Get the full text, the RSS feed doesn't have this for now    
    body = text.format_contents(soup.find("div", "classified_ad"))
    #Next try for images
    images = []
    img_link_container = soup.find("span", "value")
    if img_link_container:
        img_links = img_link_container.find_all("a")
        if img_links:
                images = [link.attrs['href'] for link in img_links if 'href' in link.attrs]
    #Now contact information
    email = text.extract_email(body)
    phone_number = text.extract_phone_number(body)

    #Combine it all together
    listing.update({
            "description": text.strip_tags(body),
            "phone_number": phone_number,
            "email": email,
            "images": ",".join(images)
            })
    #Push it out to the API
    return CyblerAPI().insert("listing", listing)
    
@task
def process_naughtyreview(rss_url, city, state):
    city_address = geolocation.get_best_guess_address(city=city, state=state)
    city_lat, city_lon = geolocation.decode_to_latlon(city_address)


    #Return data on all listings in feed if they are not in mongo
    def get_listing(item):
        #If not, then update
        data = {
            "id": text.url_to_id(item['id']),
            "url": item['link'],
            "city": city,
            "state": state,
            "lat": city_lat,
            "lon": city_lon,
            "title": item["title"],
            "description": None,
            "type": "naughtyreviews"
            }
        return data
    
    #Grab un processed listings
    feed = feedparser.parse(rss_url)
    new_listings = [item for item in feed['items'] \
                    if not CyblerAPI().get("listing", _id=text.url_to_id(item['id']))][:1]

    #And the main algorithm, build listings with feed items and combine them with scraped data
    #then persist to mongo
    new_listings = map(get_listing, new_listings)
    for data in new_listings:
        build_naughtyreviews.delay(data)
    
