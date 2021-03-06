"""Formatters for formatting the json received from the internal API
"""

from cybler_mobile.lib import text

def full_listing(listing):
    """Full listing data for displaying on a single page"""
    listing["created_on"] = text.api_date_convert(listing["created_on"], "%a, %b %d %I:%M%p")
    return listing


def main_listings_json(listing):
    """For use in a batch listings page. Contains a single image, a truncated description,
    and a properly formatted date"""
    return {
        "id": listing["_id"],
        "image": text.extract_image_link(listing["images"][0]) if listing["images"] and len(listing["images"]) else "/static/img/question.png",
        "description": text.smart_truncate(listing["description"]),
        "title": listing["title"],
        "created_on": text.api_date_convert(listing["created_on"], "%a, %b %d %I:%M%p")
    }
