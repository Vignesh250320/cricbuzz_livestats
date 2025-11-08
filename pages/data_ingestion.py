"""
Data Ingestion Page - Fetch from Cricbuzz API and insert into your existing schema
Adapted to work with your current database structure (Players, Matches, Teams, Venues, etc.)
"""
import os
import requests
import pandas as pd
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

# ---------- Config ----------
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY") or os.getenv("X_RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST") or "cricbuzz-cricket.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY or "",
    "x-rapidapi-host": RAPIDAPI_HOST
}

# ---------- Database Connection ----------
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "cb_user"),
        password=os.getenv("DB_PASSWORD", "vicky@123"),
        database=os.getenv("DB_NAME", "cricbuzz_livestats")
    )

# ---------- API Helper ----------
def api_get(path: str, params: dict = None, timeout: int = 10):
    """Fetch data from Cricbuzz API"""
    url = f"https://{RAPIDAPI_HOST}/{path.lstrip('/')}"
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"API error for {path}: {e}")
        return None

# ---------- API Fetch Functions ----------
def fetch_matches_live():
    return api_get("matches/v1/live")

def fetch_matches_recent():
    return api_get("matches/v1/recent")

def fetch_matches_upcoming():
    return api_get("matches/v1/upcoming")

def fetch_stats_top(statsType="mostRuns"):
    return api_get("stats/v1/topstats/0", params={"statsType": statsType})

def fetch_teams_list():
    return api_get("teams/v1/international")

def fetch_series_list():
    return api_get("series/v1/international")

# ---------- Data Extraction ----------
def extract_matches_from_api(data):
    """Extract matches and return structured list"""
    if not data:
        return []
    matches = []
    for type_match in data.get("typeMatches", []):
        for series_match in type_match.get("seriesMatches", []):
            series_data = series_match.get("seriesAdWrapper") or series_match.get("series", {})
            series_id = series_data.get("seriesId") or series_data.get("id")
            series_name = series_data.get("seriesName") or series_data.get("name")
            
            for m in series_data.get("matches", []):
                info = m.get("matchInfo") or m.get("match", {})
                match_id = info.get("matchId") or info.get("id")
                match_desc = info.get("matchDesc") or info.get("description")
                match_format = info.get("matchFormat") or info.get("format", "T20I")
                start_date = info.get("startDate")
                
                # Parse date
                try:
                    if start_date and len(str(start_date)) > 10:
                        start_ts = int(start_date) / 1000
                        start_dt = datetime.fromtimestamp(start_ts)
                    elif start_date:
                        start_dt = datetime.fromtimestamp(int(start_date))
                    else:
                        start_dt = datetime.now()
                except Exception:
                    start_dt = datetime.now()
                
                status = info.get("status") or info.get("state", "Upcoming")
                team1 = (info.get("team1") or {}).get("teamName") or info.get("team1Name", "TBD")
                team2 = (info.get("team2") or {}).get("teamName") or info.get("team2Name", "TBD")
                venue_info = info.get("venueInfo") or info.get("venue", {})
                venue = venue_info.get("ground") or venue_info.get("name", "Unknown")
                venue_city = venue_info.get("city") or "Unknown"
                
                matches.append({
                    "series_id": series_id,
                    "series_name": series_name,
                    "match_id": match_id,
                    "match_desc": match_desc,
                    "match_format": match_format,
                    "team1": team1,
                    "team2": team2,
                    "venue": venue,
                    "city": venue_city,
                    "start_date": start_dt,
                    "status": status
                })
    return matches

def extract_players_from_stats(data):
    """Extract player stats from topstats endpoint"""
    out = []
    if not data:
        return out
    
    for rec in data.get("values", []):
        values = rec.get("values", [])
        try:
            pid = values[0] if len(values) > 0 else None
            name = values[1] if len(values) > 1 else "Unknown"
            matches = int(values[2]) if len(values) > 2 and str(values[2]).replace('.','').isdigit() else 0
            innings = int(values[3]) if len(values) > 3 and str(values[3]).replace('.','').isdigit() else 0
            runs = int(values[4]) if len(values) > 4 and str(values[4]).replace('.','').isdigit() else 0
            avg = float(values[5]) if len(values) > 5 else 0.0
            sr = float(values[6]) if len(values) > 6 else 0.0
            
            out.append({
                "player_id": pid,
                "full_name": name,
                "total_runs": runs,
                "batting_average": avg,
                "strike_rate": sr,
                "matches": matches
            })
        except Exception:
            continue
    return out

# ---------- Database Insertion (Your Schema) ----------
def insert_teams(db, teams_data):
    """Insert teams into Teams table"""
    cursor = db.cursor()
    inserted = 0
    
    for team in teams_data:
        try:
            # Check if exists
            cursor.execute("SELECT team_id FROM Teams WHERE team_name = %s", (team['name'],))
            if cursor.fetchone():
                continue
                
            sql = """INSERT INTO Teams (team_name, country, total_wins, total_losses)
                     VALUES (%s, %s, 0, 0)"""
            cursor.execute(sql, (team['name'], team.get('country', team['name'])))
            db.commit()
            inserted += 1
        except Exception as e:
            st.warning(f"Error inserting team {team.get('name')}: {e}")
            continue
    
    cursor.close()
    return inserted

def insert_venues_from_matches(db, matches_df):
    """Extract and insert unique venues from matches"""
    cursor = db.cursor()
    inserted = 0
    
    unique_venues = matches_df[['venue', 'city']].drop_duplicates()
    
    for _, row in unique_venues.iterrows():
        try:
            cursor.execute("SELECT venue_id FROM Venues WHERE venue_name = %s", (row['venue'],))
            if cursor.fetchone():
                continue
            
            sql = """INSERT INTO Venues (venue_name, city, country, capacity)
                     VALUES (%s, %s, %s, 50000)"""
            cursor.execute(sql, (row['venue'], row['city'], 'India'))
            db.commit()
            inserted += 1
        except Exception as e:
            continue
    
    cursor.close()
    return inserted

def insert_series_from_matches(db, matches_df):
    """Extract and insert series"""
    cursor = db.cursor()
    inserted = 0
    
    unique_series = matches_df[['series_id', 'series_name']].drop_duplicates()
    
    for _, row in unique_series.iterrows():
        if not row['series_id']:
            continue
        try:
            cursor.execute("SELECT series_id FROM Series WHERE series_id = %s", (row['series_id'],))
            if cursor.fetchone():
                continue
            
            sql = """INSERT INTO Series (series_id, series_name, host_country, match_type, start_date, end_date, total_matches)
                     VALUES (%s, %s, %s, %s, %s, %s, 0)"""
            cursor.execute(sql, (row['series_id'], row['series_name'], 'Multiple', 'International', 
                                datetime.now(), datetime.now()))
            db.commit()
            inserted += 1
        except Exception as e:
            continue
    
    cursor.close()
    return inserted

def insert_matches(db, matches_df):
    """Insert matches into Matches table"""
    cursor = db.cursor()
    inserted = 0
    
    for _, row in matches_df.iterrows():
        try:
            # Get team IDs
            cursor.execute("SELECT team_id FROM Teams WHERE team_name = %s", (row['team1'],))
            team1_result = cursor.fetchone()
            team1_id = team1_result[0] if team1_result else None
            
            cursor.execute("SELECT team_id FROM Teams WHERE team_name = %s", (row['team2'],))
            team2_result = cursor.fetchone()
            team2_id = team2_result[0] if team2_result else None
            
            # Get venue ID
            cursor.execute("SELECT venue_id FROM Venues WHERE venue_name = %s", (row['venue'],))
            venue_result = cursor.fetchone()
            venue_id = venue_result[0] if venue_result else None
            
            # Check if match exists
            if row['match_id']:
                cursor.execute("SELECT match_id FROM Matches WHERE match_id = %s", (row['match_id'],))
                if cursor.fetchone():
                    continue
            
            sql = """INSERT INTO Matches 
                     (match_id, series_id, team1_id, team2_id, venue_id, match_date, 
                      match_format, match_status, match_description)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(sql, (
                row['match_id'],
                row['series_id'],
                team1_id,
                team2_id,
                venue_id,
                row['start_date'],
                row['match_format'],
                row['status'],
                row['match_desc']
            ))
            db.commit()
            inserted += 1
        except Exception as e:
            continue
    
    cursor.close()
    return inserted

def insert_players(db, players_df):
    """Insert players into Players table"""
    cursor = db.cursor()
    inserted = 0
    
    for _, row in players_df.iterrows():
        try:
            if not row['player_id']:
                continue
                
            cursor.execute("SELECT player_id FROM Players WHERE player_id = %s", (row['player_id'],))
            if cursor.fetchone():
                # Update existing
                sql = """UPDATE Players SET 
                         total_runs = %s, batting_average = %s, strike_rate = %s
                         WHERE player_id = %s"""
                cursor.execute(sql, (row['total_runs'], row['batting_average'], 
                                    row['strike_rate'], row['player_id']))
            else:
                # Insert new
                sql = """INSERT INTO Players 
                         (player_id, full_name, country, playing_role, batting_style, 
                          total_runs, batting_average, strike_rate)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (
                    row['player_id'],
                    row['full_name'],
                    'India',  # Default
                    'Batsman',  # Default
                    'Right-hand bat',  # Default
                    row['total_runs'],
                    row['batting_average'],
                    row['strike_rate']
                ))
                inserted += 1
            
            db.commit()
        except Exception as e:
            continue
    
    cursor.close()
    return inserted

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Data Ingestion", layout="wide", page_icon="📥")
st.title("📥 Data Ingestion - Populate Database from Cricbuzz API")

st.info("💡 **Tip**: Fetch data from API first, preview it, then insert into your database to populate more records.")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("🌐 1. Fetch from API")
    
    endpoint = st.selectbox("Select Data Source", [
        "Matches - Live",
        "Matches - Recent", 
        "Matches - Upcoming",
        "Players - Top Run Scorers",
        "Players - Top Wicket Takers",
        "Teams - International"
    ])
    
    if st.button("🔄 Fetch Data", type="primary"):
        with st.spinner("Fetching from Cricbuzz API..."):
            if "Matches - Live" in endpoint:
                data = fetch_matches_live()
                df = pd.DataFrame(extract_matches_from_api(data))
            elif "Matches - Recent" in endpoint:
                data = fetch_matches_recent()
                df = pd.DataFrame(extract_matches_from_api(data))
            elif "Matches - Upcoming" in endpoint:
                data = fetch_matches_upcoming()
                df = pd.DataFrame(extract_matches_from_api(data))
            elif "Top Run Scorers" in endpoint:
                data = fetch_stats_top("mostRuns")
                df = pd.DataFrame(extract_players_from_stats(data))
            elif "Top Wicket Takers" in endpoint:
                data = fetch_stats_top("mostWickets")
                df = pd.DataFrame(extract_players_from_stats(data))
            elif "Teams" in endpoint:
                data = fetch_teams_list()
                st.json(data)
                df = pd.DataFrame()
            else:
                df = pd.DataFrame()
            
            if not df.empty:
                st.session_state['fetched_df'] = df
                st.session_state['data_type'] = endpoint
                st.success(f"✅ Fetched {len(df)} records")
                st.dataframe(df, use_container_width=True)
            elif df.empty and "Teams" not in endpoint:
                st.warning("⚠️ No data returned from API")

with col2:
    st.header("💾 2. Insert to Database")
    
    if 'fetched_df' in st.session_state:
        df = st.session_state['fetched_df']
        data_type = st.session_state.get('data_type', '')
        
        st.info(f"**Ready to insert**: {len(df)} {data_type} records")
        st.dataframe(df.head(10), use_container_width=True)
        
        if st.button("💾 Insert into Database", type="primary"):
            db = get_db()
            
            try:
                if "Matches" in data_type:
                    with st.spinner("Inserting teams, venues, series, and matches..."):
                        # Step 1: Insert teams
                        teams_data = []
                        for team in pd.concat([df['team1'], df['team2']]).unique():
                            if team and team != 'TBD':
                                teams_data.append({'name': team, 'country': team})
                        teams_inserted = insert_teams(db, teams_data)
                        st.success(f"✅ Teams: {teams_inserted} inserted")
                        
                        # Step 2: Insert venues
                        venues_inserted = insert_venues_from_matches(db, df)
                        st.success(f"✅ Venues: {venues_inserted} inserted")
                        
                        # Step 3: Insert series
                        series_inserted = insert_series_from_matches(db, df)
                        st.success(f"✅ Series: {series_inserted} inserted")
                        
                        # Step 4: Insert matches
                        matches_inserted = insert_matches(db, df)
                        st.success(f"✅ Matches: {matches_inserted} inserted")
                        
                        st.balloons()
                        
                elif "Players" in data_type:
                    with st.spinner("Inserting players..."):
                        players_inserted = insert_players(db, df)
                        st.success(f"✅ Players: {players_inserted} inserted/updated")
                        st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                db.close()
                
    else:
        st.warning("👈 Fetch data first from the left panel")

st.markdown("---")
st.subheader("📊 Current Database Stats")

try:
    db = get_db()
    cursor = db.cursor()
    
    col1, col2, col3, col4 = st.columns(4)
    
    cursor.execute("SELECT COUNT(*) FROM Players")
    with col1:
        st.metric("Players", cursor.fetchone()[0])
    
    cursor.execute("SELECT COUNT(*) FROM Teams")
    with col2:
        st.metric("Teams", cursor.fetchone()[0])
    
    cursor.execute("SELECT COUNT(*) FROM Matches")
    with col3:
        st.metric("Matches", cursor.fetchone()[0])
    
    cursor.execute("SELECT COUNT(*) FROM Venues")
    with col4:
        st.metric("Venues", cursor.fetchone()[0])
    
    cursor.close()
    db.close()
except Exception as e:
    st.error(f"Could not fetch stats: {e}")
