"""
Text based editing features
"""

import datetime

API_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def extract_image_link(image_link):
    """
    Strips out unnecessary characters in an image link until ingestion is fixed
    """
    return image_link.strip("'[]")


def smart_truncate(content, length=100, suffix='...'):
    """Truncates a list of text by the length of characters and a trailing suffix suffix"""
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix


def api_date_convert(date, new_format):
    """Takes a date string from the API and converts it to the specified format"""
    converted_date = datetime.datetime.strptime(date, API_DATE_FORMAT)
    return converted_date.strftime(new_format)
