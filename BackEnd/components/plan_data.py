from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    latitude: float
    longitude: float

class Visiting(BaseModel):  # Capitalize class names by convention
    name: str
    location: Location
    concept: List[str]

class DayPlan(BaseModel):
    date: str
    place_to_visit: List[Visiting]  # List of Visiting objects

class TravelPlan(BaseModel):
    user_id: str
    plans: List[DayPlan]  # List of DayPlan objects
