from config import FOURSQUARE_API_KEY
from typing import List, Optional
import requests
from components.user_request_data import UserRequest

FOURSQUARE_API_URL = "https://api.foursquare.com/v3/places/search"

HEADERS = {
    "Authorization": FOURSQUARE_API_KEY,
    "Accept": "application/json"
}

def get_pois_from_map(user_request: Optional[UserRequest] = None, filter_data: Optional[str] = None, limit: int=50) -> List[dict]:
    """
    Fetches POIs using Foursquare Places API based on location and optional filter.
    
    :param filter_data: Optional category keyword (e.g. "cafe", "museum")
    :param location: Optional location string (e.g. "Seoul")
    :return: List of POIs (each as a dictionary)
    """
    if not user_request.location:
        raise ValueError("Location must be provided.")

    # 1. convert location to corresponding to latitude/longitude
    geo_resp = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": user_request.location, "format": "json"},
        headers={'User-Agent': 'TravelPlannerApp/1.0 ehrms1009@hanmail.net'}
    )
    # Check if the response is OK and contains JSON
    if geo_resp.status_code == 200 and geo_resp.text.strip():
        try:
            geo_data = geo_resp.json()
        except ValueError as e:
            print("JSON decode error:", e)
            print("Response content:", geo_resp.text)
    else:
        print(f"Request failed: status {geo_resp.status_code}")
        print("Response content:", geo_resp.text)
    
    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]

    # 2. request to foursquare api to get filter satisfying pois
    params = {
    "ll": f"{lat},{lon}",
    "categories": filter_data or "",     # Category IDs like "10027,10028"
    "query": user_request.concept,       # e.g., "art museum" or "family friendly"
    "limit": limit,
    "sort": "RELEVANCE",                 # Important: tells Foursquare to rank by query relevance
    "radius":50000
    }

    response = requests.get(FOURSQUARE_API_URL, headers=HEADERS, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch POIs: {response.text}")
    
    results = response.json().get("results", [])
    pois = []

    # https://api.foursquare.com/v3/places/{fsq_id} => more detailed information about poi 
    # returns full info: phone, website, categories, hours, photos, etc. (https://api.foursquare.com/v3/places/{fsq_id}/photos)
    # gets tips, reviews
    # store fsq_id in a DB and let users "favorite" or "review" those place
    # Store previously seen fsq_ids to prevent recommending the same spot again.
    for place in results:
        pois.append({
            "name": place.get("name"),
            "lat": place["geocodes"]["main"]["latitude"],
            "lon": place["geocodes"]["main"]["longitude"],
            "categories": [cat["name"] for cat in place.get("categories", [])],
            "fsq_id": place.get("fsq_id")
        })

    return pois

def extract_pois(user_request:UserRequest, filters:List[str], limit=30)->List[dict]:
    result = []
    for f in filters:
        pois = get_pois_from_map(user_request, f, limit=limit)
        result.extend(pois)

        if len(result) >= limit:
            return result
    return result