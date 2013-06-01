"""
Tools for manipulating text and extracting information from text
"""

import re
PHONE_NUMBER_REGEX = "(\d{3}).*(\d{3}).*(\d{4})"
EMAILS_REGEX = "([a-zA-Z0-9]+@[a-zA-Z0-9]+\.(com|net|org))"
TAG_RE = re.compile(r'<[^>]+>')
AREA_CODES = ["201","202","203","204","205","206","207","208","209","210","212","213","214","215","216","217","218","219","225","228","229","231","234","240","242","246","248","250","252","253","254","256","262","264","267","268","270","281","284","301","302","303","304","305","306","307","308","309","310","312","313","314","315","316","317","318","319","320","321","323","330","334","336","337","340","345","347","352","360","361","385","401","402","403","404","405","406","407","408","409","410","412","413","414","415","416","417","418","419","423","425","435","440","441","443","450","456","469","473","478","480","484","500","501","502","503","504","505","506","507","508","509","510","512","513","514","515","516","517","518","519","520","530","540","541","559","561","562","570","571","573","580","600","601","602","603","604","605","606","607","608","609","610","612","613","614","615","616","617","618","619","623","626","630","631","636","641","646","647","649","650","651","660","661","662","664","670","671","678","682","700","701","702","703","704","705","706","707","708","709","710","712","713","714","715","716","717","718","719","720","724","727","732","734","740","757","758","760","763","765","767","770","773","775","780","781","784","785","786","787","800","801","802","803","804","805","806","807","808","809","810","812","813","814","815","816","817","818","819","828","830","831","832","843","845","847","850","856","858","859","860","863","864","865","866","867","867","867","868","869","870","876","877","880","881","882","888","900","901","902","902","903","904","905","906","907","908","909","910","912","913","914","915","916","917","918","919","920","925","931","936","937","940","941","949","952","954","956","970","971","972","973","978","979"]

def extract_email(txt):
    """
    Extract any email addresses that may be contained within the text
    """
    match = re.search(EMAILS_REGEX, txt)
    if match:
        return match(0)

    
def extract_phone_number(txt):
    """
    Extract any phone numbers that may be in the text
    """
    match = re.search(PHONE_NUMBER_REGEX, txt)
    if match:
        if match.group(1) in AREA_CODES:
            return match.group(1) + match.group(2) + match.group(3)


def url_to_id(url):
    """
    Since ids for rss feeds will be the ids, strip out bad characters to
    return a useable id
    """
    return re.sub("[/|:| |?]", "", url)


def format_contents(contents):
    """Formats the contents of a beautiful soup entry to be able to be returned
    """
    if not contents:
        return None
    return "".join([str(x).encode("utf-8", "replace") for x in contents.contents])


def strip_tags(string):
    """Removes all the tags (html/xml) from a string """
    return TAG_RE.sub('', string)


def image_format(string):
    """Removes trailing muck on http string for images"""
    return string.strip("[]' ")

def body_format(soup_bits):
    """
    Removes tags from HTML, and joins them with nicely formatted paragraph tags
    if there is content
    """
    result = ""
    for content in soup_bits.contents:
        candidate_str = strip_tags(unicode(content)).strip()
        if len(candidate_str):
            result += "%s\n" % candidate_str
            
    #If the string was modified, then we'll close the paragraph tag and return it
    return result
