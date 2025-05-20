from fastapi import APIRouter
from components.user_data import UserData
from modules.common.route_optimizer import optimize_route
from modules.route_optim_util import load_pois, get_scores_from_llm

router = APIRouter()

# ---- Main API Endpoint ----
@router.post("/route_optim")
async def route_optim(user_data: UserData):
    # 1. Load POIs from CSV
    poi_list = load_pois(user_data.kwargs.poi_file_loc)

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
