from fastapi import APIRouter, HTTPException
from components.user_data import UserData
from modules.common.route_optimizer import optimize_route
from modules.route_optim_util import load_pois, get_scores_from_llm
from modules.common.components_util import printUserData, printTravelPlan

router = APIRouter()

# ---- Main API Endpoint ----
@router.post("/route_optim")
def route_optim(user_data: UserData):
    try:
        # 1. Load POIs from CSV (or later redis)
        poi_list = load_pois(user_data.kwargs.poi_file_loc)
    
        # 2. Get scores from LLM
        scored_pois = get_scores_from_llm(poi_list, user_data)
    
        # 3. Optimize route
        # travel_plan follows form of plan_data.TravelPlan
        travel_plan = optimize_route(user_data.duration, scored_pois)

        # 4. Return updated user_data + travel plan
        user_data.kwargs.prev_map_data = travel_plan
        return {
            "user_data": user_data,
            "travel_plan": travel_plan
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))