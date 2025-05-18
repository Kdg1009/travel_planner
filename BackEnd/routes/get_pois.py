from fastapi import APIRouter, Request
from services import llm_request, get_pois_from_map, save_to
import uuid
import os

router = APIRouter()

@router.post("/get_pois")
async def get_pois_handler(request: Request):
    data = await request.json()
    region = data["region"]
    user_info = data["kwargs"]

    if user_info.get("filter") is None:
        user_info["filter"] = llm_request.get_filter(region, user_info)

    pois = get_pois_from_map.fetch_pois(region, user_info["filter"])

    session_id = str(uuid.uuid4())
    file_path = f"temp_data_{session_id}.csv"
    save_to.save_to_csv(pois, file_path)

    return {"session_id": session_id, "pois": pois}