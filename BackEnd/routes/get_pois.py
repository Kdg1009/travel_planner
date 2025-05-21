from fastapi import APIRouter, HTTPException
from components.user_data import UserData
from modules.common.get_pois_from_map import get_pois_from_map
from modules.get_pois_util import get_filter_from_llm, save_pois

router = APIRouter()

@router.post("/get_pois")
async def get_pois(user_data: UserData):
    try:
        filter_data = user_data.kwargs.filter

        # Step 1: If no filter, call LLM to generate it
        if not filter_data:
            filter_data = get_filter_from_llm(user_data.model_dump())
            user_data.kwargs.filter = filter_data

        # Step 2: Fetch POIs based on filter
        poi_list = get_pois_from_map(filter_data, user_data.location)

        # Step 3: Save to CSV
        user_data.kwargs.poi_file_loc = save_pois(poi_list)

        # Step 4: Return result
        return {
            "user_data": user_data.model_dump()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))