from fastapi import APIRouter, HTTPException
from typing import Optional, Dict
import time
from components.cache_data import CacheData

router = APIRouter()

# In-memory cache: { key: { value: any, expires_at: timestamp } }
cache = {}

# Save a data to in-memory cache with optional expiration
@router.post("/cache/save")
def cache_save(key: str, value: Dict, expire: Optional[int] = None) -> None:
    expires_at = time.time() + expire if expire else time.time() + 3600

    if key not in cache:
        cache[key] = CacheData(expires_at=expires_at)

    cache[key].update(value)

# Retrieve a data by key, checking expiration
@router.get("/cache/get")
def cache_get(key: str) -> Dict[str,CacheData]:
    item = cache.get(key)
    if not item:
        raise HTTPException(status_code=404, detail="Key not found")

    # Check expiration
    if item.expires_at and time.time() > item.expires_at:
        del cache[key]
        raise HTTPException(status_code=404, detail="Key expired")

    return {"value": cache[key]}


# Delete a data by key
@router.get("cache/delete")
def cache_del(key:str) -> None:
    item = cache.get(key)
    if item:
        del cache[key]