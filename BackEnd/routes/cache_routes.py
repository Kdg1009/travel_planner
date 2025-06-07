from fastapi import APIRouter, Body
from typing import Optional, Dict
import time
from components.cache_data import CacheData

router = APIRouter()

# In-memory cache: { key: { value: any, expires_at: timestamp } }
cache = {}

# Save a data to in-memory cache with optional expiration
@router.post("/cache/save")
def cache_save(key: str, value: Dict = Body(...), expire: Optional[int] = None) -> None:
    expires_at = time.time() + expire if expire else time.time() + 3600
    value = value["value"]

    if key not in cache:
        cache[key] = CacheData(data=value,expires_at=expires_at)

    cache[key].update(value)
    print_status()

# Retrieve a data by key, checking expiration
@router.get("/cache/get")
def cache_get(key: str, extend_minutes: int = 30) -> Dict[str, CacheData]:
    item = cache.get(key)
    if not item:
        print("key not found")
        return {"value": None}  # Added return for consistency

    # Check expiration
    if item.expires_at and time.time() > item.expires_at:
        del cache[key]
        print("key expired")
        return {"value": None}  # Added return for consistency
    
    # Update expiration time to extend the cache lifetime
    if item.expires_at:  # Only update if there was an expiration time originally
        item.expires_at = time.time() + (extend_minutes * 60)
        print(f"Cache extended for key '{key}' by {extend_minutes} minutes")
    
    return {"value": item}


# Delete a data by key
@router.get("cache/delete")
def cache_del(key:str) -> None:
    item = cache.get(key)
    if item:
        del cache[key]

def print_status():
    print("< cache status >")
    print(cache)