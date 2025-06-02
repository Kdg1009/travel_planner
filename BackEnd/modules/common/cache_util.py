from uuid import uuid4
import requests
from components.cache_data import CacheData

def save_data(payload, backend_url="http://localhost:3000/api/cache/save") -> str:
    key = uuid4().hex

    response = requests.post(
        backend_url,
        params={"key":key},
        json=payload
    )

    if response.status_code != 200:
        raise Exception(f"Failed to save POIs to cache: {response.text}")
    return key

def load_data(key:str, backend_url="http://localhost:3000/api/cache/get") -> CacheData:
    response = requests.get(
        backend_url,
        params={"key":key}
    )

    if response.status_code != 200:
        raise Exception(f"Failed to load POIs: {response.text}")
    data = response.json()
    return data["value"]