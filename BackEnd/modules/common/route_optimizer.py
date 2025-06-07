from components.plan_data import Location, Visiting, DayPlan, TravelPlan
from components.user_request_data import Duration
from components.llm_score_data import PlaceScore
from datetime import datetime, timedelta
from typing import List, Optional
import requests
import numpy as np
# ---- remove after implementing naver api
import math
from sklearn.cluster import DBSCAN

# ---- optimize_helper ----
# return list of dates within duration.start and duration.end
def get_days(duration: Duration) -> List[str]:
    start_date = datetime.strptime(duration.start, "%Y-%m-%d")
    end_date = datetime.strptime(duration.end, "%Y-%m-%d")
    delta = end_date - start_date

    return [
        (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(delta.days + 1)
    ]

# get actual distance
def get_distance(start_lat, start_lng, end_lat, end_lng, mode="driving"):
    # simple directed distance
    # remove after implementing naver api
    return math.sqrt((start_lat - end_lat)**2 + (start_lng - end_lng)**2)
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVER_CLIENT_SECRET,
    }

    url = f"https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
    params = {
        "start": f"{start_lng},{start_lat}",
        "goal": f"{end_lng},{end_lat}",
        "option": "trafast"  # shortest path with traffic
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        try:
            route = data["route"]["trafast"][0]
            distance_m = route["summary"]["distance"]
            duration_sec = route["summary"]["duration"]
            return {
                "distance_km": distance_m / 1000,
                "duration_min": duration_sec / 60000
            }
        except Exception as e:
            print("Failed to parse route:", e)
            return None
    else:
        print("API Error:", response.status_code, response.text)
        return None

def cluster_pois(pois: List[Visiting], eps=0.05, min_samples=2) -> List[int]:
    """
    Cluster POIs based on geographic proximity using DBSCAN
    
    Args:
        pois: List of Visiting objects
        eps: The maximum distance between two samples for them to be considered as in the same neighborhood
        min_samples: The number of samples in a neighborhood for a point to be considered as a core point
        
    Returns:
        List of cluster labels for each POI
    """
    if not pois:
        return []
        
    # Extract coordinates from POIs
    coordinates = np.array([[float(poi.location.latitude), float(poi.location.longitude)] for poi in pois])
    
    # Apply DBSCAN clustering
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(coordinates)
    
    # Return cluster labels
    return clustering.labels_.tolist()

def softmax(scores: List[float]) -> List[float]:
    """
    Apply softmax function to convert scores to probabilities
    
    Args:
        scores: List of scores
        
    Returns:
        List of probabilities
    """
    # Convert to numpy array and apply softmax
    exp_scores = np.exp(np.array(scores))
    return (exp_scores / exp_scores.sum()).tolist()

def next_visit(scores: List[float], pois: List[Visiting], clusters: List[int], 
               prev_visit: Optional[Visiting] = None, prev_cluster: Optional[int]=None, incentive_factor: float = 1.3) -> Visiting:
    """
    Select the next POI to visit based on scores and clustering
    
    Args:
        scores: List of scores for each POI
        pois: List of Visiting objects
        clusters: List of cluster labels for each POI
        prev_visit: The previously visited POI (optional)- not used in this function, but may used in later extension such as use concepts in weighting
        prev_cluster: The cluster ID of the previous visit (optional)
        incentive_factor: Factor to boost scores for POIs in the same cluster
        
    Returns:
        The next POI to visit
    """
    # Create a copy of scores to modify
    adjusted_scores = scores.copy()
    
    # Apply incentive for POIs in the same cluster as prev_visit
    if prev_cluster is not None and prev_cluster != -1:
        for i, cluster in enumerate(clusters):
            if cluster == prev_cluster:
                adjusted_scores[i] *= incentive_factor
    
    # Apply softmax to get probabilities
    probabilities = softmax(adjusted_scores)
    
    # Select the POI with the highest probability
    selected_idx = np.argmax(probabilities)
    selected_poi = pois[selected_idx]

    return selected_poi

def optimize_route(user_id: str, duration: Duration, pois_data: List[PlaceScore], visits_per_day: int = 3, score_threshold=7.4) -> TravelPlan:
    """
    Create an optimized travel plan based on POIs provided as dictionaries
    
    Args:
        duration: Duration object with start and end dates
        pois_data: List of POI dictionaries with format:
                  {'name': str, 'latitude': str, 'longitude': str, 'score': str, 'concept': str}
        visit_per_day: Maximum number of visits per day
        score_threshold: Minimum score for a POI to be considered
        
    Returns:
        Optimized TravelPlan
    """
    days = get_days(duration)
    # Convert dictionary POIs to Visiting objects and extract scores
    pois = []
    scores = []
    
    for poi_dict in pois_data:
        # Convert dictionary to Visiting object
        poi = Visiting(
            name=poi_dict['name'],
            location=Location(
                latitude=poi_dict['latitude'],
                longitude=poi_dict['longitude']
            ),
            concept=poi_dict['category']
        )
        pois.append(poi)
        
        # Extract score (convert from string to float)
        scores.append(float(poi_dict['score']))

    # Filter POIs based on score threshold
    filtered_indices = [i for i, score in enumerate(scores) if score >= score_threshold]
    filtered_pois = [pois[i] for i in filtered_indices]
    filtered_scores = [scores[i] for i in filtered_indices]

    # Early return if no POIs meet the threshold
    if not filtered_pois:
        return TravelPlan(user_id=user_id, plans=[])
        
    # Cluster POIs (only the filtered ones)
    clusters = cluster_pois(filtered_pois)

    # Create a copy of POIs and scores to modify
    remaining_pois = filtered_pois.copy()
    remaining_scores = filtered_scores.copy()
    remaining_clusters = clusters.copy()

    # Initialize travel plan
    travel_plan = TravelPlan(user_id=user_id, plans=[])

    # Create day plans
    for day_idx in range(len(days)):
        current_date = days[day_idx]

        # Initialize day plan
        day_plan = DayPlan(date=current_date, place_to_visit=[])
        
        # Previous visit, initially None
        prev_visit = None
        prev_cluster = None
        
        # Add visits for the day
        for _ in range(min(visits_per_day, len(remaining_pois))):
            if not remaining_pois:
                break
                
            # Get next POI to visit
            next_poi = next_visit(
                remaining_scores, 
                remaining_pois, 
                remaining_clusters, 
                prev_visit,
                prev_cluster
            )
            
            # Add POI to day plan
            day_plan.place_to_visit.append(next_poi)
            
            # Update previous visit
            prev_visit = next_poi
            
            # Remove selected POI from remaining POIs and scores
            idx = remaining_pois.index(next_poi)
            remaining_pois.pop(idx)
            remaining_scores.pop(idx)
            prev_cluster = remaining_clusters.pop(idx)
        
        # Add day plan to travel plan
        travel_plan.plans.append(day_plan)
    
    return travel_plan