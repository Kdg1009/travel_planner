from modules.common.llm_request import request_to_llm
import csv
import os
from fastapi import HTTPException
from components.user_data import UserData
from components.llm_score_data import Place
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from common.webcrawler import exec_webcrawl

def get_scores_from_llm(poi_list: List[Dict], user_data: UserData) -> List[Place]:
    def chunk_list(lst, chunk_size):
        """Yield successive chunks from list."""
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]

    # Parameters
    batch_size = 10  # You can adjust this as needed
    batches = list(chunk_list(poi_list, batch_size))
    results: List[Place] = []

    with ThreadPoolExecutor() as executor:
        # Submit tasks
        futures = [executor.submit(get_scores_for_batch, batch, user_data) for batch in batches]

        # Collect results
        for future in as_completed(futures):
            batch_result = future.result()
            results.extend(batch_result)

    return results

def get_scores_for_batch(batch: List[Dict], user_data: UserData) -> List[Place]:
    results: List[Place] = []

    for place in batch:
        name = place["name"]
        latitude = place["latitude"]
        longitude = place["longitude"]

        # Step 1: Get reviews (black-box)
        reviews = exec_webcrawl(name)  # Assume this returns a List[str] of review texts

        if not reviews:
            continue  # Skip if no reviews found

        # Step 2: Construct request for LLM
        reviews_text = "\n".join([f"{i+1}. {review}" for i, review in enumerate(reviews)])
        llm_prompt = f"""
You are a travel assistant helping a user select the most fitting places to visit.

The user’s preferences are as follows:
- Companions: {user_data.companions}
- Concepts: {user_data.concepts}
- Extra Requests: {user_data.extra_requests}

You are given reviews for a place called "{name}".  
Read each review and evaluate **how well this place fits the user's preferences**, on a scale of 1 to 10 (10 = perfect match, 1 = very poor fit).

Respond with a **comma-separated list** of integers representing scores **in order** for each review (no text, no explanation, only numbers). Example: `7,6,8,5,...`

Reviews:
{reviews_text}
"""

        # Step 3: Send to LLM
        response_text = request_to_llm(llm_prompt.strip())

        # Step 4: Parse scores
        try:
            score_strings = response_text.strip().split(",")
            scores = [int(s.strip()) for s in score_strings if s.strip().isdigit()]
        except Exception:
            scores = []

        if not scores:
            continue  # Skip if parsing failed

        # Step 5: Calculate average score
        avg_score = sum(scores) / len(scores)

        # Step 6: Create and add Place object
        results.append(Place(name=name, latitude=latitude, longitude=longitude, score=avg_score, concept=""))

    return results

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

'''
def chunk_pois(poi_list, chunk_size=20):
    for i in range(0, len(poi_list), chunk_size):
        yield poi_list[i:i + chunk_size]

# ---- Helper to get scores from llm ----
def parse_llm_response_to_dict_list(llm_response: str)->List[Place]:
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
        if len(parts) != 5:
            # skip malformed lines or handle error
            continue
        name, lat_str, lon_str, score_str, concept = parts
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
            "concept":concept,
        })

    return result

def get_scores_from_llm(poi_list: list, user_data: UserData) -> List[Place]:
    all_responses = []

    for chunk in chunk_pois(poi_list, chunk_size=20):
        poi_info = "\n".join(
            f"- {poi['name']} (lat: {poi['latitude']}, long: {poi['longitude']})"
            for poi in chunk
        )

        query = f"""
You are a travel planner AI.

Based on the user profile below and the list of Points of Interest (POIs), score each POI on a scale from 0 to 100, based on how well it matches the user's preferences.
Respond with one line for **each POI listed above**. If any POI is missing, it will be considered an incomplete response.

## User Profile (in JSON):
{json.dumps(user_data.model_dump(), indent=2)}

## POIs:
{poi_info}

## Expected Output Format (CSV-style, no header):
name,latitude,longitude,score,concept

Please respond only with the list. Respond to *every* POI above.
        """.strip()

        response = request_to_llm(query)
        all_responses.append(response)

    full_csv_output = "\n".join(all_responses)
    return parse_llm_response_to_dict_list(full_csv_output)
'''
