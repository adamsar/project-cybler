"""
Tools for manipulating text and extracting information from text
"""

import re
PHONE_NUMBER_REGEX = "(\d{3}).*(\d{3}).*(\d{4})"
EMAILS_REGEX = "([a-zA-Z0-9]+@[a-zA-Z0-9]+\.(com|net|org))"
TAG_RE = re.compile(r'<[^>]+>')
def extract_email(txt):
    """
    Extract any email addresses that may be contained within the text
    """
    match = re.search(EMAILS_REGEX, txt)
    if match:
        return match.group(0)

    
def extract_phone_number(txt):
    """
    Extract any phone numbers that may be in the text
    """
    match = re.search(PHONE_NUMBER_REGEX, txt)
    if match:
        return int(match.group(1) + match.group(2) + match.group(3))


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
