from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    latitude: str
    longitude: str

class Visiting(BaseModel):  # Capitalize class names by convention
    name: str
    location: Location

class DayPlan(BaseModel):
    date: str
    place_to_visit: List[Visiting]  # List of Visiting objects

class TravelPlan(BaseModel):
    dayplan: List[DayPlan]  # List of DayPlan objects
