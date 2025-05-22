import json
from multiprocessing import Manager
from threading import Thread
import time

class Cache:
    def __init__(self, ttl_seconds=600):
        self.manager = Manager()
        self.store = self.manager.dict()  # shared dict: key -> (value_json, expire_time)
        self.ttl = ttl_seconds

        # Background thread to clean expired keys
        def cleanup():
            while True:
                now = time.time()
                keys_to_delete = [k for k, (_, exp) in self.store.items() if exp <= now]
                for k in keys_to_delete:
                    del self.store[k]
                time.sleep(10)  # check every 10 sec

        Thread(target=cleanup, daemon=True).start()

    def save(self, key: str, data):
        value_json = json.dumps(data)
        expire_time = time.time() + self.ttl
        self.store[key] = (value_json, expire_time)

    def load(self, key: str):
        if key not in self.store:
            raise ValueError(f"Key {key} not found or expired")
        value_json, expire_time = self.store[key]
        if expire_time <= time.time():
            del self.store[key]
            raise ValueError(f"Key {key} expired")
        return json.loads(value_json)
