from pydantic import BaseModel
from typing import Optional, Dict, Any

# Pydantic models for validation (user_data defined)
class Duration(BaseModel):
    start: str
    end: str

class Kwargs(BaseModel):
    filter: Optional[Dict[str, Any]] = None
    prev_map_data: Optional[Any] = None
    poi_file_loc: str = None

class UserData(BaseModel):
    location: str
    duration: Duration
    companions: str
    concept: str
    extra_request: str
    kwargs: Kwargs