from pydantic import BaseModel, Field
from typing import Dict
import time

class CacheData(BaseModel):
    data: Dict
    expires_at: float = Field(default_factory=lambda: time.time() + 3600)

    def update(self, value: dict):
        for key, val in value.items():
            self.data[key] = val
