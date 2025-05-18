from dotenv import load_dotenv
import os

# Load .env file from current directory or specify path
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
NAVERMAP_API_KEY = os.getenv('NAVERMAP_API_KEY')
FOURSQUARE_API_KEY = os.getenv('FOURSQUARE_API_KEY')