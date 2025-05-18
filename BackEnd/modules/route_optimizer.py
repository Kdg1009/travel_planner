def optimize(pois):
    return sorted(pois, key=lambda p: -float(p["score"]))