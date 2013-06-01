"""
Code dealing with the parsing of a page of data
"""
from bs4 import BeautifulSoup
from cybler_tasks.data.cybler_api import CyblerAPI
from cybler_tasks.lib import text
import urllib

ASSOCIATED_RESOURCE = "listing"
class BaseParser(object):
    """
    The basic parser that will be inherited by all. Provides an ingestion
    interface
    """
    
    def __init__(self, listing):
        """
        Constructor requires a listing massaged in from the an rssfeed
        """
        self.listing = listing
        self.soup = BeautifulSoup(urllib.urlopen(self.listing['url']).read())
        self.api = CyblerAPI()

    @property
    def valid(self):
        raise NotImplementedError()

    def _parse_soup(self):
        raise NotImplementedError()
        
    def ingest(self):
        """
        The actual ingestion code
        """
        #Use the soup to modify the listing
        self._parse_soup()
        #Check if the listing is valid and update via the API
        if self.valid:
            self.api.insert(ASSOCIATED_RESOURCE, self.listing)

class CyblerParser(BaseParser):
    """Parser used for generic cybler ingestion"""

    @property
    def valid(self):
        """
        Checks if a listing is valid for sending to the Cybler API
        """
        return self.listing.get("description") and self.listing.get("title")

        
class BackPageParser(CyblerParser):
    """
    Parser for a backpage listing
    """

    __type__ = "backpage"
    
    def _parse_soup(self):
        """
        Grab out the appropriate elements in the soup
        """
        #First get the full listings body
        listing_body = self.soup.find("div", "postingBody")
        if listing_body:
            listing_body = text.body_format(listing_body)
            if listing_body:
                self.listing["description"] = listing_body

        #Next, look for images
        image_container = self.soup.find("ul", {"id": "viewAdPhotoLayout"})
        if image_container:
            images = [text.image_format(i.attrs["src"]) for i in image_container.find_all("img")]
            self.listing["images"] = ",".join(images)
        else:
            self.listing["images"] = []

class AdultSearchParser(CyblerParser):
    """
    Parser for all adultsearch.com listings
    """

    __type__ = "adultsearch"

    def _parse_soup(self):
        """Massage the html from an adultsearch listing"""

        #Grab any images associated with the post
        image = self.soup.find("div", {"id": "gallery"})
        images = []
        if image:
            images = image.find_all("img")
            if images:
                images = [i.attrs['src'] for i in images]
            else:
                images = []

        self.listing["images"] = ",".join(images)

class ProviderGuideParser(CyblerParser):
    """Parser for providerguide.com"""

    __type__ = "providerguide"

    def _parse_soup(self):
        """Massage HTML from provider guide"""
        #Get full text from the article
        body = text.body_format(
            self.soup.find(
                "div", {
                    "id": "post_bodytext"
                }
            )
        )

        #Now do images
        images = []
        img_link_container = self.soup.find(
            "div", {
                "id": "post_photos"
            })
        if img_link_container:
            image_links = [link.attrs['href'] for link in img_link_container.find_all("a")]
            for i in image_links:
                if "myproviderguide.com" not in i:
                    images.append("http://www.myproviderguide.com" + i)
                else:
                    images.append(i)
        self.listing.update({
            "description": body,
            "images": ",".join(images)
            })
