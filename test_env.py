from dotenv import load_dotenv
import os

load_dotenv()

print("DB Host:", os.getenv("DB_HOST"))
print("API Base:", os.getenv("CRICBUZZ_API_BASE"))
print("API Key:", os.getenv("RAPIDAPI_KEY")[:6] + "********")  # partially hide
