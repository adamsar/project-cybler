"""
Tools for manipulating text and extracting information from text
"""

import re

def extract_emails(text):
    """
    Extract any email addresses that may be contained within the text
    """

    pass

    
def extract_phone_number(text):
    """
    Extract any phone numbers that may be in the text
    """
    match = re.search(".*(\d{3}).*(\d{3}).*(\d{4}).*", text)
    if match:
        return int(match.group(1) + match.group(2) + match.group(3))


def url_to_id(url):
    """
    Since ids for rss feeds will be the ids, strip out bad characters to
    return a useable id
    """
    return url.replace("/", "").replace(":", "").replace("#", "").replace("?", "")
