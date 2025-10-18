"""
Cricbuzz API Integration Helper
Handles all API calls to Cricbuzz via RapidAPI
"""

import requests
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


class CricbuzzAPI:
    """Wrapper for Cricbuzz API calls"""
    
    def __init__(self):
        self.api_key = os.getenv('RAPIDAPI_KEY')
        self.api_host = os.getenv('RAPIDAPI_HOST', 'cricbuzz-cricket.p.rapidapi.com')
        self.base_url = f"https://{self.api_host}"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.api_host
        }
    
    def _make_request(self, endpoint):
        """
        Make API request
        
        Args:
            endpoint: API endpoint path
        
        Returns:
            JSON response or None
        """
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
            return None
    
    def get_recent_matches(self):
        """Get recent cricket matches"""
        return self._make_request("matches/v1/recent")
    
    def get_live_matches(self):
        """Get live cricket matches"""
        return self._make_request("matches/v1/live")
    
    def get_upcoming_matches(self):
        """Get upcoming cricket matches"""
        return self._make_request("matches/v1/upcoming")
    
    def get_match_details(self, match_id):
        """
        Get detailed match information
        
        Args:
            match_id: Match ID
        
        Returns:
            Match details JSON
        """
        return self._make_request(f"mcenter/v1/{match_id}")
    
    def get_match_scorecard(self, match_id):
        """
        Get match scorecard
        
        Args:
            match_id: Match ID
        
        Returns:
            Scorecard JSON
        """
        return self._make_request(f"mcenter/v1/{match_id}/scard")
    
    def get_series_list(self):
        """Get list of cricket series"""
        return self._make_request("series/v1/international")
    
    def get_series_matches(self, series_id):
        """
        Get matches in a series
        
        Args:
            series_id: Series ID
        
        Returns:
            Series matches JSON
        """
        return self._make_request(f"series/v1/{series_id}")
    
    def get_player_info(self, player_id):
        """
        Get player information
        
        Args:
            player_id: Player ID
        
        Returns:
            Player info JSON
        """
        return self._make_request(f"stats/v1/player/{player_id}")
    
    def get_rankings_batsmen(self, format_type="test"):
        """
        Get batsmen rankings
        
        Args:
            format_type: Cricket format (test, odi, t20)
        
        Returns:
            Rankings JSON
        """
        return self._make_request(f"stats/v1/rankings/batsmen?formatType={format_type}")
    
    def get_rankings_bowlers(self, format_type="test"):
        """
        Get bowlers rankings
        
        Args:
            format_type: Cricket format (test, odi, t20)
        
        Returns:
            Rankings JSON
        """
        return self._make_request(f"stats/v1/rankings/bowlers?formatType={format_type}")
    
    def get_rankings_allrounders(self, format_type="test"):
        """
        Get all-rounders rankings
        
        Args:
            format_type: Cricket format (test, odi, t20)
        
        Returns:
            Rankings JSON
        """
        return self._make_request(f"stats/v1/rankings/allrounders?formatType={format_type}")
    
    def get_news(self):
        """Get cricket news"""
        return self._make_request("news/v1/index")


def get_api_client():
    """Helper function to get API client instance"""
    return CricbuzzAPI()
