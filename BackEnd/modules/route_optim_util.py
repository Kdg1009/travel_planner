from modules.common.llm_request import request_to_llm
from components.user_request_data import UserRequest
from components.llm_score_data import Place
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from modules.common.poi_metadata import get_reviews
from modules.common.cache_util import load_data
import requests
import traceback

def get_scores_from_llm(poi_list: List[Dict], user_data: UserRequest) -> List[Place]:
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
            try:
                batch_result = future.result()
                print('batch result in upper func:\n', batch_result)
                results.extend(batch_result)
                print('results extension:\n', results)
            except Exception as e:
                print("⚠️ Exception in future:")
                traceback.print_exc()

    return results

def get_scores_for_batch(batch: List[Dict], user_data: UserRequest) -> List[Place]:
    results: List[Place] = []

    for place in batch:
        name = place["name"]
        latitude = place["lat"]
        longitude = place["lon"]
        id = place["fsq_id"]
        category = place["categories"]

        # Step 1: Get reviews (black-box)
        reviews = get_reviews(name, id)  # Assume this returns a List[str] of review texts

        if not isinstance(reviews, list):
            print(f"⚠️ Invalid review data for {name}: {reviews}")
            return []

        # Step 2: Construct request for LLM
        try:
            reviews_text = "\n".join([f"{i+1}. {review['text']}" for i, review in enumerate(reviews)])
        except Exception as e:
            print(f"⚠️ Failed to format reviews for {name}: {e}, raw reviews: {reviews}")
            return []

        llm_prompt = f"""
You are a travel assistant helping a user select the most fitting places to visit.

The user’s preferences are as follows:
- Companions: {user_data.companions}
- Concepts: {user_data.concept}
- Extra Requests: {user_data.extra_request}

You are given reviews for a place called "{name}".  
Read each review and evaluate **how well this place fits the user's preferences**, on a scale of 1 to 10 (10 = perfect match, 1 = very poor fit).

Respond with a **comma-separated list** of integers representing scores **in order** for each review (no text, no explanation, only numbers). Example: `7,6,8,5,...`

place categories:
{category}

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
        results.append(Place(name=name, latitude=latitude, longitude=longitude, score=avg_score, category=category))
    print('batch result:\n', results)
    return results

# ---- Helper to load pois ----
def load_pois(key):
    data = load_data(key)
    return data["poi_list"]

def get_nearby_accommodations(lat, lon, radius=2000, limit=10):
    headers = {
        "Accept": "application/json",
        "Authorization": "YOUR_FOURSQUARE_API_KEY"
    }

    params = {
        "ll": f"{lat},{lon}",
        "radius": radius,  # in meters
        "limit": limit,
        "categories": "19014,19015,19016,19017"  # Foursquare category ID for 'Hotel','Hostle','Vacation Rental','Resort'
    }

    response = requests.get("https://api.foursquare.com/v3/places/search", headers=headers, params=params)
    return response.json()