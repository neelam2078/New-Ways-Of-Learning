from urllib.parse import quote_plus


PLATFORMS = {

    "Amazon":
        "https://www.amazon.in/s?k={q}",

    "Flipkart":
        "https://www.flipkart.com/search?q={q}",

    "IKEA":
        "https://www.ikea.com/in/en/search/?q={q}",

    "Swiggy":
        "https://www.swiggy.com/search?query={q}",

    "Zomato":
        "https://www.zomato.com/search?query={q}",

    "OYO":
        "https://www.oyorooms.com/search?q={q}",
}


def search_url(
    platform: str,
    query: str,
) -> str:

    template = PLATFORMS.get(
        platform,
        "https://www.google.com/search?q={q}",
    )

    return template.format(
        q=quote_plus(query)
    )


def choose_platform(
    category: str,
    planner_type: str,
) -> str:

    category_lower = category.lower()

    if planner_type == "party":

        if category_lower in {
            "food",
            "catering",
            "restaurant",
        }:
            return "Zomato"

        if category_lower in {
            "venue",
            "stay",
            "accommodation",
        }:
            return "OYO"

        return "Amazon"

    if planner_type == "home":

        if category_lower in {
            "furniture",
            "decor",
            "lighting",
        }:
            return "IKEA"

        return "Amazon"

    if category_lower in {
        "earrings",
        "necklace",
        "jewelry",
        "jewellery",
    }:
        return "Flipkart"

    return "Amazon"