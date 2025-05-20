from fastapi import APIRouter, HTTPException
from ..components.user_data import UserData
import csv
import os
from modules.llm_request import request_to_llm
from modules.route_optimizer import optimize_route

router = APIRouter()

# ---- Helper to get scores from llm ----
def get_scores_from_llm(poi_list, user_data):
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
{user_data.json(indent=2)}

## POIs:
{poi_info}

## Expected Output Format (CSV-style, no header):
name,latitude,longitude,score

Please respond only with the list.
    """.strip()

    # Step 4: Call the LLM
    response = request_to_llm(query)

    # Optional: Parse or return raw depending on downstream usage
    return response

# ---- Helper to read CSV POI list ----
def load_pois_from_csv(filename: str):
    path = os.path.join("temp", filename)
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
def load_pois(pois_loc:str):
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

# ---- Main API Endpoint ----
@router.post("/api/route_optim")
async def route_optimization(user_data: UserData):
    # 1. Load POIs from CSV
    poi_list = load_pois(user_data.kwargs.get("poi_file_loc"))

    # 2. Get scores from LLM
    scored_pois = get_scores_from_llm(poi_list, user_data)

    # 3. Optimize route
    # travel_plan follows form of plan_data.TravelPlan
    travel_plan = optimize_route(scored_pois)

    # 4. Return updated user_data + travel plan (i think that returining user_data won't be necessary)
    return {
        "user_data": user_data,
        "travel_plan": travel_plan
    }
