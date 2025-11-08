"""
Quick API Test Script
Run this to verify your Cricbuzz API is working correctly
"""

import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")

print("=" * 60)
print("🏏 CRICBUZZ API CONFIGURATION TEST")
print("=" * 60)

# 1. Check API credentials
print("\n1️⃣ Checking API credentials...")
if RAPIDAPI_KEY:
    print(f"   ✅ API Key: {RAPIDAPI_KEY[:10]}...{RAPIDAPI_KEY[-5:]}")
else:
    print("   ❌ API Key not found in .env file!")
    exit(1)

if RAPIDAPI_HOST:
    print(f"   ✅ API Host: {RAPIDAPI_HOST}")
else:
    print("   ❌ API Host not found!")
    exit(1)

# 2. Test API connection
print("\n2️⃣ Testing API connection...")

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

# Test endpoints
test_endpoints = [
    ("Live Matches", "/matches/v1/live"),
    ("Top Stats", "/stats/v1/topstats/0?statsType=mostRuns"),
    ("ICC Rankings", "/stats/v1/rankings/batsmen?formatType=test"),
]

successful_tests = 0
total_tests = len(test_endpoints)

for name, endpoint in test_endpoints:
    url = f"https://{RAPIDAPI_HOST}{endpoint}"
    print(f"\n   Testing: {name}")
    print(f"   URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        status_code = response.status_code
        
        if status_code == 200:
            print(f"   ✅ Status: {status_code} - SUCCESS")
            data = response.json()
            
            # Show sample of response
            if isinstance(data, dict):
                keys = list(data.keys())[:3]
                print(f"   📊 Response keys: {keys}")
            
            successful_tests += 1
        elif status_code == 403:
            print(f"   ❌ Status: {status_code} - FORBIDDEN (Check API key)")
        elif status_code == 429:
            print(f"   ⚠️  Status: {status_code} - RATE LIMIT EXCEEDED")
        else:
            print(f"   ❌ Status: {status_code}")
            
    except requests.exceptions.Timeout:
        print(f"   ❌ Request timeout after 10 seconds")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

# 3. Summary
print("\n" + "=" * 60)
print("📊 TEST SUMMARY")
print("=" * 60)
print(f"Successful: {successful_tests}/{total_tests}")

if successful_tests == total_tests:
    print("\n🎉 ALL TESTS PASSED! Your API is working correctly.")
    print("\n✅ Next steps:")
    print("   1. Run: streamlit run app.py")
    print("   2. Navigate to '🔧 API Testing' page")
    print("   3. Test individual endpoints")
elif successful_tests > 0:
    print("\n⚠️  PARTIAL SUCCESS - Some endpoints are working")
    print("   Check your API subscription and rate limits")
else:
    print("\n❌ ALL TESTS FAILED")
    print("\n🔍 Troubleshooting:")
    print("   1. Verify your API key in .env file")
    print("   2. Check your RapidAPI subscription status")
    print("   3. Ensure you have active subscription for Cricbuzz API")
    print("   4. Check rate limits on your plan")

print("\n" + "=" * 60)
