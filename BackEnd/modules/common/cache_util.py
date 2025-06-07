from uuid import uuid4
import requests
from components.cache_data import CacheData
from fastapi.encoders import jsonable_encoder

def save_data(key=None, payload=None, backend_url="http://localhost:3000/api/cache/save") -> str:
    if not key:
        key = uuid4().hex

    serialized_payload = jsonable_encoder(payload)

    response = requests.post(
        backend_url,
        params={"key":key},
        json={"value":serialized_payload}
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
        raise Exception(f"Failed to load data: {response.text}")
    data = response.json()
    return data["value"]["data"]