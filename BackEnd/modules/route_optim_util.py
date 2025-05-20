from modules.common.llm_request import request_to_llm
import csv
import os
import json
from fastapi import HTTPException
from components.user_data import UserData

# ---- Helper to get scores from llm ----
def parse_llm_response_to_dict_list(llm_response: str)->list:
    """
    Parses the LLM CSV-style response (no header) into a list of dictionaries.

    Expected input format per line:
    name,latitude,longitude,score

    Returns:
        List[Dict[str, Any]] with keys: 'name', 'latitude', 'longitude', 'score'
    """
    result = []
    lines = llm_response.strip().splitlines()
    for line in lines:
        parts = line.split(',')
        if len(parts) != 4:
            # skip malformed lines or handle error
            continue
        name, lat_str, lon_str, score_str = parts
        try:
            lat = float(lat_str)
            lon = float(lon_str)
            score = float(score_str)
        except ValueError:
            # skip if conversion fails
            continue

        result.append({
            "name": name,
            "latitude": lat,
            "longitude": lon,
            "score": score,
        })

    return result

def get_scores_from_llm(poi_list:list, user_data:UserData)->list:
    # Step 1: Convert user data to readable string (already achived)
    # Step 2: Construct POI information block
    poi_info = "\n".join(
        f"- {poi['name']} (lat: {poi['latitude']}, long: {poi['longitude']})"
        for poi in poi_list
    )

    # Step 3: Build the prompt/query
    query = f"""
You are a travel planner AI.

Based on the user profile below and the list of Points of Interest (POIs), score each POI on a scale from 0 to 100, based on how well it matches the user's preferences.

## User Profile (in JSON):
{json.dumps(user_data.model_dump(), indent=2)}

## POIs:
{poi_info}

## Expected Output Format (CSV-style, no header):
name,latitude,longitude,score

Please respond only with the list.
    """.strip()

    # Step 4: Call the LLM
    response = request_to_llm(query)

    # Optional: Parse or return raw depending on downstream usage

    return parse_llm_response_to_dict_list(response)

# ---- Helper to read CSV POI list ----
def load_pois_from_csv(filename: str)->list:
    path = os.path.join("BackEnd","routes", "temp", filename)
    pois = []
    try:
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pois.append(row)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="POI CSV file not found")
    return pois

# ---- Helper to load pois ----
def load_pois(pois_loc):
    if not pois_loc:
        raise HTTPException(status_code=400, detail="Missing 'poi_csv' in kwargs")
    poi_list = load_pois_from_csv(pois_loc)
    return poi_list
    """
        < redis version>
        from modules import get_pois_from_redis

        poi_list = get_pois_from_redis(pois_loc)
        if not poi_list:
            raise HTTPException(status_code=404, detail="POIs not found in Redis")
        return poi_list
    """