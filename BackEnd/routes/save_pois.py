# 파일 위치 예시: routes/save.py

from fastapi import APIRouter, Request
from modules.common.save_util import save_as  # <- 너가 만든 save_as 함수 import

router = APIRouter()

@router.post("/api/save_pois")
async def save_pois(request: Request):
    data = await request.json()
    poi_list = data.get("poi_list", [])
    filename = data.get("filename", "saved_pois.csv")

    if not poi_list:
        return {"error": "No POIs provided"}

    try:
        save_as(poi_list, filename)
        return {"message": f"{filename} 저장 완료"}
    except Exception as e:
        return {"error": str(e)}