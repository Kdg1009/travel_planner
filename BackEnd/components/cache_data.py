from pydantic import BaseModel, Field
from typing import List
import time

class CacheData(BaseModel):
    poi_list: List = Field(default_factory=list)
    accomodation: List = Field(default_factory=list)
    expires_at: float = Field(default_factory=lambda: time.time() + 3600)

    def update(self, value: dict):
        if "poi_list" in value:
            self.poi_list = value["poi_list"]
        if "accomodation" in value:
            self.accomodation = value["accomodation"]
