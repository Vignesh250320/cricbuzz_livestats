import streamlit as st
import pandas as pd
from utils.api_handler import get_live_matches, get_recent_matches, get_upcoming_matches
from datetime import datetime

st.set_page_config(page_title="📺 Live Matches", layout="wide")

st.title("🏏 Cricket Matches Dashboard")

# Match type selector
match_type = st.radio("Select Match Type", ["🔴 Live", "📅 Upcoming", "📜 Recent"], horizontal=True)

def extract_matches(data):
    """Extract match information from API response."""
    matches = []
    if "error" in data:
        error_msg = data['error']
        status_code = data.get('status_code', 'Unknown')
        
        if status_code == 404:
            st.warning(f"⚠️ No data found (404). This could mean no matches are available right now.")
        elif status_code == 403:
            st.error(f"❌ Access Denied (403): Check your API key in .env file")
        elif status_code == 429:
            st.error(f"❌ Rate Limit Exceeded (429): Too many requests. Please wait and try again.")
        else:
            st.error(f"❌ API Error ({status_code}): {error_msg}")
        return matches
    
    for t in data.get("typeMatches", []):
        for s in t.get("seriesMatches", []):
            series_wrapper = s.get("seriesAdWrapper", {})
            series_info = series_wrapper.get("seriesName", "") if series_wrapper else ""
            
            match_list = s.get("seriesMatches", [])
            if not match_list and series_wrapper:
                match_list = series_wrapper.get("matches", [])
            
            for m in match_list:
                info = m.get("matchInfo", {})
                if not info:
                    continue
                
                team1 = info.get("team1", {}).get("teamName", "TBD")
                team2 = info.get("team2", {}).get("teamName", "TBD")
                desc = info.get("matchDesc", "")
                status = info.get("status", "")
                match_format = info.get("matchFormat", "")
                venue = info.get("venueInfo", {}).get("ground", "")
                
                date_str = ""
                if start_date := info.get("startDate"):
                    try:
                        date_str = datetime.fromtimestamp(int(start_date)//1000).strftime('%b %d, %H:%M')
                    except:
                        pass
                
                matches.append({
                    "Match": f"{team1} vs {team2}",
                    "Description": desc,
                    "Format": match_format,
                    "Status": status,
                    "Venue": venue,
                    "Date": date_str,
                    "Series": series_info
                })
    return matches

# Fetch and display based on selection
if st.button("🔄 Refresh Matches", type="primary"):
    with st.spinner("Fetching data from Cricbuzz API..."):
        if match_type == "🔴 Live":
            data = get_live_matches()
            matches = extract_matches(data)
            if matches:
                df = pd.DataFrame(matches)
                st.success(f"✅ Found {len(matches)} live match(es)")
                st.dataframe(df, width='stretch')
            else:
                st.info("No live matches at the moment.")
        
        elif match_type == "📅 Upcoming":
            data = get_upcoming_matches()
            matches = extract_matches(data)
            if matches:
                df = pd.DataFrame(matches)
                st.success(f"✅ Found {len(matches)} upcoming match(es)")
                st.dataframe(df, width='stretch')
            else:
                st.info("No upcoming matches found.")
        
        else:  # Recent
            data = get_recent_matches()
            matches = extract_matches(data)
            if matches:
                df = pd.DataFrame(matches)
                st.success(f"✅ Found {len(matches)} recent match(es)")
                st.dataframe(df, width='stretch')
            else:
                st.info("No recent matches found.")
else:
    st.info("👆 Click **Refresh Matches** to load data from Cricbuzz API")
    
st.markdown("---")
st.caption("💡 Data refreshes every 60 seconds for live matches, 5 minutes for others")
