import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("CRICBUZZ_API_BASE", "https://cricbuzz-cricket.p.rapidapi.com")
API_KEY = os.getenv("RAPIDAPI_KEY")

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

url = f"{BASE_URL}/teams/v1/4/players"   # 4 = India
res = requests.get(url, headers=headers)
print(res.status_code)
print(res.text[:500])
