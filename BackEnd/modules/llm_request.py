from BackEnd.config import gpt_api_key

# dummy placeholder for LLM interaction

def get_filter(region, user_info):
    return f"attractions in {region} for {user_info['people']}"

def score_pois(pois, user_info):
    for i, poi in enumerate(pois):
        poi["score"] = 1.0 / (i + 1)  # dummy scores
    return pois