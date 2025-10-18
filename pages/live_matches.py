"""
Live Matches Page - Real-time match updates from Cricbuzz API
"""

import streamlit as st
import pandas as pd
from src.utils.api_helper import get_api_client
from datetime import datetime


def show():
    """Display live matches page"""
    
    st.title("📱 Live Cricket Matches")
    st.markdown("Real-time match updates from Cricbuzz API")
    
    # Initialize API client
    api_client = get_api_client()
    
    # Tabs for different match types
    tab1, tab2, tab3 = st.tabs(["🔴 Live Matches", "📅 Recent Matches", "🔜 Upcoming Matches"])
    
    with tab1:
        st.subheader("Live Matches")
        display_live_matches(api_client)
    
    with tab2:
        st.subheader("Recent Matches")
        display_recent_matches(api_client)
    
    with tab3:
        st.subheader("Upcoming Matches")
        display_upcoming_matches(api_client)


def display_live_matches(api_client):
    """Display live matches"""
    
    with st.spinner("Fetching live matches..."):
        data = api_client.get_live_matches()
    
    if not data:
        st.warning("Unable to fetch live matches. Please check your API connection.")
        return
    
    # Parse and display matches
    matches = parse_matches(data)
    
    if not matches:
        st.info("No live matches at the moment.")
        return
    
    # Remove duplicates based on match_id
    seen_ids = set()
    unique_matches = []
    for match in matches:
        if match['match_id'] not in seen_ids:
            seen_ids.add(match['match_id'])
            unique_matches.append(match)
    
    for idx, match in enumerate(unique_matches):
        display_match_card(match, is_live=True, index=idx, prefix="live")


def display_recent_matches(api_client):
    """Display recent matches"""
    
    with st.spinner("Fetching recent matches..."):
        data = api_client.get_recent_matches()
    
    if not data:
        st.warning("Unable to fetch recent matches. Please check your API connection.")
        return
    
    # Parse and display matches
    matches = parse_matches(data)
    
    if not matches:
        st.info("No recent matches found.")
        return
    
    # Remove duplicates based on match_id
    seen_ids = set()
    unique_matches = []
    for match in matches:
        if match['match_id'] not in seen_ids:
            seen_ids.add(match['match_id'])
            unique_matches.append(match)
    
    for idx, match in enumerate(unique_matches):
        display_match_card(match, is_live=False, index=idx, prefix="recent")


def display_upcoming_matches(api_client):
    """Display upcoming matches"""
    
    with st.spinner("Fetching upcoming matches..."):
        data = api_client.get_upcoming_matches()
    
    if not data:
        st.warning("Unable to fetch upcoming matches. Please check your API connection.")
        return
    
    # Parse and display matches
    matches = parse_matches(data)
    
    if not matches:
        st.info("No upcoming matches found.")
        return
    
    # Remove duplicates based on match_id
    seen_ids = set()
    unique_matches = []
    for match in matches:
        if match['match_id'] not in seen_ids:
            seen_ids.add(match['match_id'])
            unique_matches.append(match)
    
    for idx, match in enumerate(unique_matches):
        display_match_card(match, is_live=False, index=idx, prefix="upcoming")


def parse_matches(data):
    """
    Parse match data from API response
    
    Args:
        data: API response JSON
    
    Returns:
        List of match dictionaries
    """
    matches = []
    
    try:
        if isinstance(data, dict):
            # Handle typeMatches structure
            if 'typeMatches' in data:
                for type_match in data['typeMatches']:
                    if 'seriesMatches' in type_match:
                        for series in type_match['seriesMatches']:
                            if 'seriesAdWrapper' in series:
                                series_info = series['seriesAdWrapper']
                                if 'matches' in series_info:
                                    for match_wrapper in series_info['matches']:
                                        if 'matchInfo' in match_wrapper:
                                            match_info = match_wrapper['matchInfo']
                                            matches.append(parse_match_info(match_info))
            
            # Handle direct matches array
            elif 'matches' in data:
                for match in data['matches']:
                    if 'matchInfo' in match:
                        matches.append(parse_match_info(match['matchInfo']))
    except Exception as e:
        st.error(f"Error parsing matches: {e}")
    
    return matches


def parse_match_info(match_info):
    """
    Parse individual match information
    
    Args:
        match_info: Match info dictionary
    
    Returns:
        Parsed match dictionary
    """
    return {
        'match_id': match_info.get('matchId', 'N/A'),
        'series_name': match_info.get('seriesName', 'N/A'),
        'match_desc': match_info.get('matchDesc', 'N/A'),
        'match_format': match_info.get('matchFormat', 'N/A'),
        'team1': match_info.get('team1', {}).get('teamName', 'TBD'),
        'team2': match_info.get('team2', {}).get('teamName', 'TBD'),
        'venue': match_info.get('venueInfo', {}).get('ground', 'N/A'),
        'city': match_info.get('venueInfo', {}).get('city', 'N/A'),
        'status': match_info.get('status', 'N/A'),
        'match_started': match_info.get('matchStarted', False),
        'match_complete': match_info.get('matchComplete', False),
        'start_date': match_info.get('startDate', 'N/A'),
        'state': match_info.get('state', 'N/A')
    }


def display_match_card(match, is_live=False, index=0, prefix="match"):
    """
    Display match information card
    
    Args:
        match: Match dictionary
        is_live: Whether match is live
        index: Unique index for this match
        prefix: Prefix for unique key generation
    """
    
    # Create card container
    with st.container():
        # Header with live indicator
        if is_live and match['match_started'] and not match['match_complete']:
            st.markdown(f"### 🔴 {match['series_name']}")
        else:
            st.markdown(f"### {match['series_name']}")
        
        # Match details
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**{match['match_desc']}** • {match['match_format']}")
            st.markdown(f"**{match['team1']}** vs **{match['team2']}**")
            st.markdown(f"📍 {match['venue']}, {match['city']}")
        
        with col2:
            # Status badge
            if match['match_complete']:
                st.success("✅ Completed")
            elif match['match_started']:
                st.warning("🔴 Live")
            else:
                st.info("🔜 Upcoming")
            
            # Date
            if match['start_date'] != 'N/A':
                try:
                    timestamp = int(match['start_date']) / 1000
                    date = datetime.fromtimestamp(timestamp)
                    st.markdown(f"📅 {date.strftime('%d %b %Y')}")
                except:
                    st.markdown(f"📅 {match['start_date']}")
        
        # Match status
        if match['status'] != 'N/A':
            st.info(match['status'])
        
        # View details button with unique key
        if st.button(f"View Details", key=f"{prefix}_match_{match['match_id']}_{index}"):
            display_match_details(match['match_id'])
        
        st.markdown("---")


def display_match_details(match_id):
    """
    Display detailed match information
    
    Args:
        match_id: Match ID
    """
    
    api_client = get_api_client()
    
    with st.spinner("Loading match details..."):
        details = api_client.get_match_details(match_id)
    
    if not details:
        st.error("Unable to fetch match details.")
        return
    
    # Display match details in expander
    with st.expander("📊 Match Details", expanded=True):
        st.json(details)
    
    # Try to get scorecard
    with st.spinner("Loading scorecard..."):
        scorecard = api_client.get_match_scorecard(match_id)
    
    if scorecard:
        with st.expander("📋 Scorecard", expanded=True):
            st.json(scorecard)


if __name__ == "__main__":
    show()
