# 🌐 API Testing Guide - Cricbuzz API

Complete guide for testing and understanding the Cricbuzz API integration.

---

## 📋 API Overview

**Provider**: Cricbuzz Cricket API  
**Platform**: RapidAPI  
**Base URL**: `https://cricbuzz-cricket.p.rapidapi.com`  
**Authentication**: API Key (x-rapidapi-key header)

---

## 🔑 Getting Your API Key

### Step 1: Sign Up for RapidAPI
1. Go to: https://rapidapi.com/
2. Click "Sign Up" (free account)
3. Complete registration

### Step 2: Subscribe to Cricbuzz API
1. Visit: https://rapidapi.com/cricketapilive/api/cricbuzz-cricket
2. Click "Subscribe to Test"
3. Choose a plan:
   - **Basic (Free)**: 100 requests/month
   - **Pro**: 10,000 requests/month
   - **Ultra**: 100,000 requests/month

### Step 3: Get Your API Key
1. After subscribing, go to "Endpoints" tab
2. Your API key is shown in the code snippets
3. Copy the key (starts with your unique identifier)

---

## 🧪 Testing API Endpoints

### Method 1: Using Python Script

Create a test file `test_api.py`:

```python
import requests
import json

# Your API credentials
RAPIDAPI_KEY = "your_key_here"
RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

# Test 1: Get Recent Matches
print("Testing Recent Matches...")
url = f"https://{RAPIDAPI_HOST}/matches/v1/recent"
response = requests.get(url, headers=headers)
print(f"Status Code: {response.status_code}")
print(json.dumps(response.json(), indent=2))

# Test 2: Get Live Matches
print("\nTesting Live Matches...")
url = f"https://{RAPIDAPI_HOST}/matches/v1/live"
response = requests.get(url, headers=headers)
print(f"Status Code: {response.status_code}")
print(json.dumps(response.json(), indent=2))
```

Run it:
```bash
python test_api.py
```

### Method 2: Using the Application

1. Run the app: `streamlit run app.py`
2. Go to "Live Matches" page
3. Check if data loads
4. If errors appear, check the error message

### Method 3: Using RapidAPI Dashboard

1. Go to RapidAPI Cricbuzz API page
2. Click "Test Endpoint" button
3. Select endpoint (e.g., `/matches/v1/recent`)
4. Click "Test Endpoint"
5. View response

---

## 📡 Available Endpoints

### 1. Matches Endpoints

#### Recent Matches
```
GET /matches/v1/recent
```
Returns recently completed matches.

**Example Response**:
```json
{
  "typeMatches": [
    {
      "matchType": "International",
      "seriesMatches": [...]
    }
  ]
}
```

#### Live Matches
```
GET /matches/v1/live
```
Returns currently ongoing matches.

#### Upcoming Matches
```
GET /matches/v1/upcoming
```
Returns scheduled upcoming matches.

#### Match Details
```
GET /mcenter/v1/{matchId}
```
Returns detailed information about a specific match.

**Parameters**:
- `matchId`: Match ID (integer)

#### Match Scorecard
```
GET /mcenter/v1/{matchId}/scard
```
Returns scorecard for a specific match.

### 2. Series Endpoints

#### International Series
```
GET /series/v1/international
```
Returns list of international cricket series.

#### Series Details
```
GET /series/v1/{seriesId}
```
Returns details of a specific series.

**Parameters**:
- `seriesId`: Series ID (integer)

### 3. Rankings Endpoints

#### Batsmen Rankings
```
GET /stats/v1/rankings/batsmen?formatType={format}
```
Returns batsmen rankings.

**Parameters**:
- `formatType`: test, odi, or t20

#### Bowlers Rankings
```
GET /stats/v1/rankings/bowlers?formatType={format}
```
Returns bowlers rankings.

#### All-rounders Rankings
```
GET /stats/v1/rankings/allrounders?formatType={format}
```
Returns all-rounders rankings.

### 4. Player Endpoints

#### Player Info
```
GET /stats/v1/player/{playerId}
```
Returns player information and statistics.

**Parameters**:
- `playerId`: Player ID (integer)

### 5. News Endpoints

#### Cricket News
```
GET /news/v1/index
```
Returns latest cricket news.

---

## 🔍 Understanding API Responses

### Match Response Structure

```json
{
  "typeMatches": [
    {
      "matchType": "International",
      "seriesMatches": [
        {
          "seriesAdWrapper": {
            "seriesId": 12345,
            "seriesName": "ICC World Cup 2024",
            "matches": [
              {
                "matchInfo": {
                  "matchId": 67890,
                  "matchDesc": "1st Match",
                  "matchFormat": "ODI",
                  "team1": {
                    "teamId": 1,
                    "teamName": "India"
                  },
                  "team2": {
                    "teamId": 2,
                    "teamName": "Australia"
                  },
                  "venueInfo": {
                    "ground": "Wankhede Stadium",
                    "city": "Mumbai"
                  },
                  "status": "India won by 6 wickets",
                  "matchStarted": true,
                  "matchComplete": true
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

### Key Fields Explained

- **matchId**: Unique identifier for the match
- **seriesId**: Unique identifier for the series
- **matchDesc**: Match description (e.g., "1st Match", "Final")
- **matchFormat**: Format type (Test, ODI, T20I, T20)
- **team1/team2**: Team information
- **venueInfo**: Venue details
- **status**: Match status or result
- **matchStarted**: Boolean - has match started
- **matchComplete**: Boolean - is match completed

---

## ⚠️ Common API Issues

### Issue 1: 401 Unauthorized
**Error**: `{"message": "Invalid API key"}`

**Solutions**:
- Check API key is correct in `.env` file
- Ensure no extra spaces in the key
- Verify subscription is active on RapidAPI

### Issue 2: 429 Too Many Requests
**Error**: `{"message": "Rate limit exceeded"}`

**Solutions**:
- You've exceeded your plan's request limit
- Wait for the limit to reset (usually monthly)
- Upgrade to a higher plan

### Issue 3: 403 Forbidden
**Error**: `{"message": "You are not subscribed to this API"}`

**Solutions**:
- Subscribe to the API on RapidAPI
- Check subscription is active

### Issue 4: 404 Not Found
**Error**: `{"message": "Endpoint not found"}`

**Solutions**:
- Check endpoint URL is correct
- Verify the endpoint exists in API documentation

### Issue 5: Empty Response
**Response**: `{}`

**Possible Reasons**:
- No live matches at the moment (for /live endpoint)
- No data available for the requested resource
- This is normal behavior, not an error

---

## 🧪 Testing Checklist

### Before Testing:
- [ ] RapidAPI account created
- [ ] Subscribed to Cricbuzz API
- [ ] API key copied
- [ ] `.env` file updated with API key
- [ ] Internet connection active

### Test Each Endpoint:
- [ ] Recent Matches (`/matches/v1/recent`)
- [ ] Live Matches (`/matches/v1/live`)
- [ ] Upcoming Matches (`/matches/v1/upcoming`)
- [ ] Rankings - Test (`/stats/v1/rankings/batsmen?formatType=test`)
- [ ] Rankings - ODI (`/stats/v1/rankings/batsmen?formatType=odi`)
- [ ] Rankings - T20 (`/stats/v1/rankings/batsmen?formatType=t20`)

### Verify in Application:
- [ ] Live Matches page loads
- [ ] Top Stats page loads
- [ ] Data displays correctly
- [ ] No error messages

---

## 📊 Rate Limiting

### Free Plan Limits:
- **Requests**: 100/month
- **Rate**: ~3 requests/day
- **Hard Limit**: Yes

### Best Practices:
1. Cache API responses when possible
2. Don't refresh too frequently
3. Use sample data for development
4. Upgrade plan if needed

### Monitoring Usage:
1. Go to RapidAPI Dashboard
2. Click "Analytics"
3. View request count and remaining quota

---

## 🔧 Debugging API Calls

### Enable Debug Mode

Add to your test script:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

response = requests.get(url, headers=headers)
print(f"Request URL: {response.url}")
print(f"Status Code: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Response: {response.text}")
```

### Check Response Status

```python
if response.status_code == 200:
    print("Success!")
    data = response.json()
elif response.status_code == 401:
    print("Authentication failed - check API key")
elif response.status_code == 429:
    print("Rate limit exceeded")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

---

## 💡 Tips for Development

### 1. Use Sample Data
While developing, use the sample data feature to avoid API calls:
- Go to CRUD Operations → Sample Data
- Load sample data
- Practice SQL queries without API

### 2. Cache API Responses
Store API responses locally for testing:

```python
import json

# Save response
with open('matches_cache.json', 'w') as f:
    json.dump(response.json(), f)

# Load cached response
with open('matches_cache.json', 'r') as f:
    data = json.load(f)
```

### 3. Mock API for Testing
Create mock responses for development:

```python
def get_mock_matches():
    return {
        "typeMatches": [
            {
                "matchType": "International",
                "seriesMatches": [...]
            }
        ]
    }
```

---

## 📚 Additional Resources

- **RapidAPI Docs**: https://rapidapi.com/cricketapilive/api/cricbuzz-cricket
- **Cricbuzz Website**: https://www.cricbuzz.com/
- **API Support**: Contact via RapidAPI platform

---

## ✅ Verification Script

Save as `verify_api.py`:

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')

def test_api():
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    
    print("🧪 Testing Cricbuzz API Connection...")
    print(f"API Host: {RAPIDAPI_HOST}")
    print(f"API Key: {RAPIDAPI_KEY[:10]}..." if RAPIDAPI_KEY else "Not set")
    print()
    
    url = f"https://{RAPIDAPI_HOST}/matches/v1/recent"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ SUCCESS! API is working correctly.")
            data = response.json()
            print(f"Response contains {len(str(data))} characters")
        elif response.status_code == 401:
            print("❌ FAILED! Invalid API key.")
        elif response.status_code == 429:
            print("⚠️ WARNING! Rate limit exceeded.")
        else:
            print(f"❌ FAILED! Status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"❌ ERROR! {e}")

if __name__ == "__main__":
    test_api()
```

Run: `python verify_api.py`

---

**Happy API Testing! 🚀**
