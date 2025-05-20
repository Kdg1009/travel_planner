from config import FOURSQUARE_API_KEY
from modules.common.llm_request import request_to_llm

# dummy function
def get_pois_from_map(filter_data:str, location:str)->list:
    pois = [
    {"name": "Gyeongbokgung", "latitude": "37.5796", "longitude": "126.9770"},
    {"name": "N Seoul Tower", "latitude": "37.5512", "longitude": "126.9882"}
    ]
    return pois