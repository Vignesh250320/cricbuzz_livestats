import os
import requests
from dotenv import load_dotenv
import streamlit as st
from typing import Optional, Dict, Any

# Load API credentials
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")
BASE_URL = f"https://{RAPIDAPI_HOST}"

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

def _make_request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Internal function to make API requests."""
    url = f"{BASE_URL}{endpoint if endpoint.startswith('/') else '/' + endpoint}"
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned {response.status_code}", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}

# ==================== MATCHES ====================

@st.cache_data(ttl=60)
def get_live_matches() -> Dict[str, Any]:
    """Get all live matches."""
    return _make_request("/matches/v1/live")

@st.cache_data(ttl=300)
def get_upcoming_matches() -> Dict[str, Any]:
    """Get upcoming matches."""
    return _make_request("/matches/v1/upcoming")

@st.cache_data(ttl=300)
def get_recent_matches() -> Dict[str, Any]:
    """Get recent matches."""
    return _make_request("/matches/v1/recent")

@st.cache_data(ttl=300)
def get_match_info(match_id: int) -> Dict[str, Any]:
    """Get detailed match information."""
    return _make_request(f"/mcenter/v1/{match_id}")

@st.cache_data(ttl=60)
def get_match_scorecard(match_id: int) -> Dict[str, Any]:
    """Get match scorecard."""
    return _make_request(f"/mcenter/v1/{match_id}/hscard")

# ==================== PLAYERS ====================

@st.cache_data(ttl=3600)
def get_player_info(player_id: int) -> Dict[str, Any]:
    """Get player information."""
    return _make_request(f"/stats/v1/player/{player_id}")

@st.cache_data(ttl=3600)
def get_player_batting_stats(player_id: int) -> Dict[str, Any]:
    """Get player batting statistics."""
    return _make_request(f"/stats/v1/player/{player_id}/batting")

@st.cache_data(ttl=3600)
def get_player_bowling_stats(player_id: int) -> Dict[str, Any]:
    """Get player bowling statistics."""
    return _make_request(f"/stats/v1/player/{player_id}/bowling")

@st.cache_data(ttl=3600)
def get_player_career_stats(player_id: int) -> Dict[str, Any]:
    """Get player career statistics."""
    return _make_request(f"/stats/v1/player/{player_id}/career")

@st.cache_data(ttl=300)
def search_player(player_name: str) -> Dict[str, Any]:
    """Search for a player by name."""
    return _make_request("/stats/v1/player/search", params={"plrN": player_name})

# ==================== VENUES ====================

@st.cache_data(ttl=3600)
def get_venue_info(venue_id: int) -> Dict[str, Any]:
    """Get venue information."""
    return _make_request(f"/venues/v1/{venue_id}")

@st.cache_data(ttl=3600)
def get_venue_stats(venue_id: int) -> Dict[str, Any]:
    """Get venue statistics."""
    return _make_request(f"/stats/v1/venue/{venue_id}")

# ==================== TEAMS ====================

@st.cache_data(ttl=3600)
def get_international_teams() -> Dict[str, Any]:
    """Get list of international teams."""
    return _make_request("/teams/v1/international")

@st.cache_data(ttl=300)
def get_team_results(team_id: int) -> Dict[str, Any]:
    """Get team recent results."""
    return _make_request(f"/teams/v1/{team_id}/results")

@st.cache_data(ttl=3600)
def get_team_players(team_id: int) -> Dict[str, Any]:
    """Get team squad/players."""
    return _make_request(f"/teams/v1/{team_id}/players")

@st.cache_data(ttl=3600)
def get_team_stats(team_id: int, stats_type: str = "mostRuns") -> Dict[str, Any]:
    """Get team statistics by type (mostRuns, mostWickets, etc.)."""
    return _make_request(f"/stats/v1/team/{team_id}", params={"statsType": stats_type})

# ==================== SERIES ====================

@st.cache_data(ttl=3600)
def get_international_series() -> Dict[str, Any]:
    """Get list of international series."""
    return _make_request("/series/v1/international")

@st.cache_data(ttl=300)
def get_series_matches(series_id: int) -> Dict[str, Any]:
    """Get matches in a series."""
    return _make_request(f"/series/v1/{series_id}")

@st.cache_data(ttl=3600)
def get_series_stats(series_id: int, stats_type: str = "mostRuns") -> Dict[str, Any]:
    """Get series statistics by type."""
    return _make_request(f"/stats/v1/series/{series_id}", params={"statsType": stats_type})

@st.cache_data(ttl=3600)
def get_series_squad(series_id: int, team_id: int) -> Dict[str, Any]:
    """Get series squad for a team."""
    return _make_request(f"/series/v1/{series_id}/squads/{team_id}")

@st.cache_data(ttl=3600)
def get_series_venues(series_id: int) -> Dict[str, Any]:
    """Get venues for a series."""
    return _make_request(f"/series/v1/{series_id}/venues")

# ==================== STATS & RANKINGS ====================

@st.cache_data(ttl=3600)
def get_icc_rankings(category: str = "batsmen", format_type: str = "test") -> Dict[str, Any]:
    """
    Get ICC rankings.
    category: batsmen, bowlers, allrounders, teams
    format_type: test, odi, t20
    """
    return _make_request(f"/stats/v1/rankings/{category}", params={"formatType": format_type})

@st.cache_data(ttl=3600)
def get_top_stats(category: int = 0, stats_type: str = "mostRuns") -> Dict[str, Any]:
    """
    Get top statistics/records.
    category: 0=all formats, 1=test, 2=odi, 3=t20
    stats_type: mostRuns, mostWickets, highestScore, bestBowling, etc.
    """
    return _make_request(f"/stats/v1/topstats/{category}", params={"statsType": stats_type})

# ==================== LEGACY FUNCTION ====================

@st.cache_data(ttl=60)
def fetch_from_cricbuzz(endpoint: str) -> Dict[str, Any]:
    """Legacy function for backward compatibility."""
    return _make_request(endpoint)
