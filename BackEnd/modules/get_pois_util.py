from modules.common.llm_request import request_to_llm
from modules.common.save_as import save_as
from uuid import uuid4
import json

# ---- Helper to get filter from llm ----

def get_filter_from_llm(user_data: dict) -> dict:
    # this will be tested after get_pois_from_map completed

    """
    Generates a Foursquare-compatible filter using LLM based on user preferences.

    :param user_data: Dictionary of user input preferences.
    :return: Dictionary containing filter parameters for Foursquare API.
    """

    # Construct readable user profile
    user_profile = (
        f"User is planning a trip to {user_data.get('location')}.\n"
        f"Travel dates: {user_data.get('duration', {}).get('start')} to {user_data.get('duration', {}).get('end')}.\n"
        f"Companions: {user_data.get('companions')}.\n"
        f"Travel concept or theme: {user_data.get('concept')}.\n"
        f"Additional requests: {user_data.get('extra_request')}\n"
    )

    # Instruction to GPT to create a filter
    instruction = (
        "Based on the user's travel profile below, generate a JSON object for querying the Foursquare API.\n"
        "The filter should help extract 50–70 Points of Interest (POIs) that align with the user's interests.\n"
        "Return only a JSON object with keys like 'categories', 'radius', 'keywords', 'limit' and any relevant filters.\n"
        "Make sure the format is valid JSON and contains only filter information—no explanation.\n"
    )

    query = instruction + "\nUser Profile:\n" + user_profile

    # Send to GPT
    response = request_to_llm(query)

    # Parse response to dict
    try:
        result = json.loads(response)
        return result
    except json.JSONDecodeError:
        raise ValueError("GPT returned an invalid JSON response for filters.")


# ---- Helper to save pois ----
def save_pois(poi_list):
    filename = f"pois_{uuid4().hex}.csv"
    save_as(poi_list, filename, format="csv")
    return filename