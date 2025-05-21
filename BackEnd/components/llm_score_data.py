from typing import TypedDict, List

class Place(TypedDict):
    name: str
    latitude: float
    longitude: float
    score: float
    concept: str