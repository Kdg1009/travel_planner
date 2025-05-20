# This part is for later extension to implement poi_list in-memory saving
# This enables to save poi without disk I/O

import redis
import json

# Connect to Redis (adjust host/port as needed)
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# After 1 hour, delete pois automatically
def save_pois_to_redis(session_id: str, pois: list, ttl_seconds: int=3600):
    r.set(session_id, json.dumps(pois), ex=ttl_seconds)

def get_pois_from_redis(session_id: str):
    data = r.get(session_id)
    if data is None:
        raise ValueError("Session expired or not found")
    return json.loads(data)
