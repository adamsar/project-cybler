"""
Files dealing with the ultimate mendokusai topic - dates
"""
import datetime

API_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
def api_str_to_date(str_date):
    """
    Take a string in the api date format, returns a python
    date object
    """
    return datetime.datetime.strptime(str_date, API_DATE_FORMAT)

    
def api_date_to_str(date):
    """
    Takes a python date, returns a proper API date formatted string
    """
    return date.strftime(API_DATE_FORMAT)
