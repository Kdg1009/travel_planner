from dotenv import load_dotenv
import os

# Load .env file from current directory or specify path
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
FOURSQUARE_API_KEY = os.getenv('FOURSQUARE_API_KEY')
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')
OPENROUTESERVICE_API_KEY = os.getenv('OPENROUTESERVICE_API_KEY')