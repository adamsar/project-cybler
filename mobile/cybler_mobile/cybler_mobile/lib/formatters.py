"""Formatters for formatting the json received from the internal API
"""

from cybler_mobile.lib import text


def main_listings_json(listing):
    """For use in a batch listings page. Contains a single image, a truncated description,
    and a properly formatted date"""
    return {
        "id": listing["_id"],
        "image": text.extract_image_link(listing["images"][0]) if listing["images"] and len(listing["images"]) else "/static/img/question.png",
        "description": text.smart_truncate(listing["description"]),
        "title": listing["title"],
        "createdOn": text.api_date_convert(listing["createdOn"], "%a, %b %d %I:%M%p")
    }
