from dotenv import load_dotenv
import os

load_dotenv()
GET_GYM_URL="https://games.crossfit.com/competitions/api/v1/competitions/open/{}/leaderboards/"
GET_GYM_LEADERBOARD_URL="https://games.crossfit.com/competitions/api/v1/competitions/open/{}/affiliates"
COUNTRIES_WITH_STATE=["United States", "Australia", "Canada"]
GET_GYM_ID_SEARCH_URL="https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
GET_DETAILS_API_KEY=os.environ.get("GCP_API_KEY")
GET_GYM_DETAILS_SEARCH_URL="https://maps.googleapis.com/maps/api/place/details/json"
GET_GYM_PHOTO_SEARCH_URL="https://maps.googleapis.com/maps/api/place/photo"
