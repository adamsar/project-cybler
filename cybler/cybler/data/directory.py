"""This module defines methods for grabbing Listing items as it intended to be a Directory
for the listings"""
from cybler.data.globe import Globe
from cybler.data.base import CyblerResourceHandler
import pymongo
import datetime
import re
import logging
log = logging.getLogger(__name__)

EMAILS_REGEX = re.compile("[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}")
PHONE_NUMBER_REGEX = re.compile("(\d{3}).*(\d{3}).*(\d{4})")
AREA_CODES = ["201","202","203","204","205","206","207","208","209","210","212","213","214","215","216","217","218","219","225","228","229","231","234","240","242","246","248","250","252","253","254","256","262","264","267","268","270","281","284","301","302","303","304","305","306","307","308","309","310","312","313","314","315","316","317","318","319","320","321","323","330","334","336","337","340","345","347","352","360","361","385","401","402","403","404","405","406","407","408","409","410","412","413","414","415","416","417","418","419","423","425","435","440","441","443","450","456","469","473","478","480","484","500","501","502","503","504","505","506","507","508","509","510","512","513","514","515","516","517","518","519","520","530","540","541","559","561","562","570","571","573","580","600","601","602","603","604","605","606","607","608","609","610","612","613","614","615","616","617","618","619","623","626","630","631","636","641","646","647","649","650","651","660","661","662","664","670","671","678","682","700","701","702","703","704","705","706","707","708","709","710","712","713","714","715","716","717","718","719","720","724","727","732","734","740","757","758","760","763","765","767","770","773","775","780","781","784","785","786","787","800","801","802","803","804","805","806","807","808","809","810","812","813","814","815","816","817","818","819","828","830","831","832","843","845","847","850","856","858","859","860","863","864","865","866","867","867","867","868","869","870","876","877","880","881","882","888","900","901","902","902","903","904","905","906","907","908","909","910","912","913","914","915","916","917","918","919","920","925","931","936","937","940","941","949","952","954","956","970","971","972","973","978","979"]

class ListingDirectory(CyblerResourceHandler):
    """
    Handler for listings. Emulates a directory of listings
    """
    __resource__ = "listing"
    __collection__ = "listing"

    def query_from_params(self, params):
        """
        Builds a query based on parameters passed into the app
        """
        q = {}
        start, rows = 0, 10
        if "start" in params:
            start = int(params["start"])
        if "rows" in params:
            rows = int(params["rows"])
        else:
            rows = 10
        if "lat" in params and "lon" in params:
            lat = float(params["lat"])
            lon = float(params["lon"])
            q["loc"] = {
                "$within": {
                    "$center": [[lat, lon], .5]
                }
            }
        if "city" in params:
            q["contact"] = {
                "city": params["city"].lower()
                }
        if "type" in params:
            q["type"] = params["type"]
        if "images" in params and params["images"] == "true":
            q["images"] = {
                "$ne": None
                }
        sort = [("created_on", pymongo.DESCENDING)]
        return self.query(start=start, rows=rows, sort=sort,**q)
        

    def insert(self, resource):
        """
        Override the basic implementation to do some better handling of
        locations, additional data massaging
        """
        #First emails
        if not resource.get('email'):
            candidate_email = EMAILS_REGEX.search(resource.get("description"))
            if candidate_email:
                resource["email"] = candidate_email.group(0)

        #Next process phone numbers
        if not resource.get("contact", {}).get("phone_number"):
            match = PHONE_NUMBER_REGEX.search(resource.get("title") + resource.get("description"))
            if match:
                if match.group(1) in AREA_CODES:
                    number = "%s%s%s" % (match.group(1), match.group(2), match.group(3))
                    resource["contact"]["phone_number"] = number

        #Finally process location
        globe = Globe(self.db)
        if "lat" not in resource.get("loc", {}) or not "lon" not in resource.get("loc", {}):
            if not "city" in resource.get("contact", {}):
                #If there's no locational information for this listing, just toss it
                return 
            location = globe.query(rows=1, no_nulls=True,
                                   **{
                                       "city": resource["contact"]["city"],
                                       "state": resource["contact"].get("state"),
                                       "country": resource["contact"].get("country")
                                   })
            if not location.count():
                location = globe.generate_location(**{
                    "city": resource["contact"]["city"],
                    "state": resource["contact"].get("state"),
                    "country": resource["contact"].get("country")
                })
                if not location:
                    #No location, so toss the listing
                    return
            else:
                location = location[0]
            resource["loc"] = {
                "lat": location["loc"]["lat"],
                "lon": location["loc"]["lon"]
                }
        else:
            location = globe.query(rows=1, **{
                "loc": {
                    "$near": {
                        [resource["loc"]["lat"], resource["loc"]["lon"]]
                    }
                }
            })[0]

        #Update contact information if necessary
        if not resource["contact"].get("city"):
            resource["contact"]["city"] = location["city"]
        if not resource["contact"].get("state"):
            resource["contact"]["state"] = location["state"]
        if not resource["contact"].get("country"):
            resource["contact"]["country"] = location["country"]
        if not resource["contact"].get("zipcode"):
            resource["contact"]["zipcode"] = location["area_code"]

        #Finally, add a timestamp
        resource["created_on"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        return super(ListingDirectory, self).insert(resource)
