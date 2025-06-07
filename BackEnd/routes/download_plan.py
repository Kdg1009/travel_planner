# Later will be deleted

from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from components.plan_data import TravelPlan
from modules.common.export_to import export_to_pdf

class DownloadRequest(BaseModel):
    user_cache_key: str
    travel_plan: TravelPlan

router = APIRouter()

@router.post("/download_plan")
def download_pdf(req:DownloadRequest):
    # Create and get PDF path
    pdf_path = export_to_pdf(req.travel_plan, user_id=req.user_cache_key)
    
    # Return it as downloadable file
    return FileResponse(path=pdf_path, filename=f"schedule_{req.user_id}.pdf", media_type="application/pdf")
