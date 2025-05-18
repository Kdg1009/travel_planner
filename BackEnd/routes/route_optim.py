from fastapi import APIRouter, Request
from services import save_to, llm_request, route_optimizer

router = APIRouter()

@router.post("/route_optim")
async def route_optimization_handler(request: Request):
    data = await request.json()
    session_id = data["session_id"]
    file_path = f"temp_data_{session_id}.csv"

    pois = save_to.load_from_csv(file_path)
    scored_pois = llm_request.score_pois(pois, data["kwargs"])
    route = route_optimizer.optimize(scored_pois)

    return {"route": route}