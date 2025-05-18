from BackEnd.config import map_api_key

def fetch_pois(region, filter_str):
    return [
        {"name": "Museum A", "lat": 37.1, "long": 127.1},
        {"name": "Park B", "lat": 37.2, "long": 127.2},
    ]