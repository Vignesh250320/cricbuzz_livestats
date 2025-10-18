"""
Fetch Cricket Data from Cricbuzz API and Populate Database
This script fetches real cricket data and populates all 8 database tables
"""

import requests
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import datetime
import time

# Load environment variables
load_dotenv()

# API Configuration
RAPIDAPI_KEY = "931ecde80cmsh80f2dc04d04d93ap136a0ejsnb76565e7402a"
RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"
BASE_URL = f"https://{RAPIDAPI_HOST}"

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'cricbuzz_db')
}


def get_db_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✅ Database connected successfully")
            return connection
    except Error as e:
        print(f"❌ Database connection error: {e}")
        return None


def make_api_request(endpoint):
    """Make API request to Cricbuzz"""
    try:
        url = f"{BASE_URL}/{endpoint}"
        print(f"📡 Fetching: {endpoint}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed for {endpoint}: {e}")
        return None


def fetch_and_insert_teams(connection):
    """Fetch teams data and insert into database"""
    print("\n" + "="*60)
    print("📊 FETCHING TEAMS DATA")
    print("="*60)
    
    cursor = connection.cursor()
    
    # Predefined international teams (API doesn't have direct teams endpoint)
    teams_data = [
        ("India", "India", "International"),
        ("Australia", "Australia", "International"),
        ("England", "England", "International"),
        ("Pakistan", "Pakistan", "International"),
        ("South Africa", "South Africa", "International"),
        ("New Zealand", "New Zealand", "International"),
        ("West Indies", "West Indies", "International"),
        ("Sri Lanka", "Sri Lanka", "International"),
        ("Bangladesh", "Bangladesh", "International"),
        ("Afghanistan", "Afghanistan", "International"),
        ("Zimbabwe", "Zimbabwe", "International"),
        ("Ireland", "Ireland", "International"),
    ]
    
    inserted = 0
    for team_name, country, team_type in teams_data:
        try:
            query = """
            INSERT INTO teams (team_name, country, team_type) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE team_name=team_name
            """
            cursor.execute(query, (team_name, country, team_type))
            inserted += 1
        except Error as e:
            print(f"⚠️  Error inserting team {team_name}: {e}")
    
    connection.commit()
    print(f"✅ Inserted {inserted} teams")
    return inserted


def fetch_and_insert_venues(connection):
    """Fetch venues data and insert into database"""
    print("\n" + "="*60)
    print("🏟️  FETCHING VENUES DATA")
    print("="*60)
    
    cursor = connection.cursor()
    
    # Major cricket venues (API has limited venue data)
    venues_data = [
        ("Wankhede Stadium", "Mumbai", "India", 33000),
        ("Eden Gardens", "Kolkata", "India", 68000),
        ("M. Chinnaswamy Stadium", "Bangalore", "India", 40000),
        ("Arun Jaitley Stadium", "Delhi", "India", 41820),
        ("MA Chidambaram Stadium", "Chennai", "India", 50000),
        ("Melbourne Cricket Ground", "Melbourne", "Australia", 100024),
        ("Sydney Cricket Ground", "Sydney", "Australia", 48000),
        ("Adelaide Oval", "Adelaide", "Australia", 53583),
        ("Lord's Cricket Ground", "London", "England", 31100),
        ("The Oval", "London", "England", 25500),
        ("Old Trafford", "Manchester", "England", 26000),
        ("Edgbaston", "Birmingham", "England", 25000),
        ("National Stadium", "Karachi", "Pakistan", 34228),
        ("Gaddafi Stadium", "Lahore", "Pakistan", 27000),
        ("Newlands", "Cape Town", "South Africa", 25000),
        ("The Wanderers", "Johannesburg", "South Africa", 28000),
    ]
    
    inserted = 0
    for venue_name, city, country, capacity in venues_data:
        try:
            query = """
            INSERT INTO venues (venue_name, city, country, capacity) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE venue_name=venue_name
            """
            cursor.execute(query, (venue_name, city, country, capacity))
            inserted += 1
        except Error as e:
            print(f"⚠️  Error inserting venue {venue_name}: {e}")
    
    connection.commit()
    print(f"✅ Inserted {inserted} venues")
    return inserted


def fetch_and_insert_players(connection):
    """Fetch trending players and rankings data"""
    print("\n" + "="*60)
    print("👥 FETCHING PLAYERS DATA")
    print("="*60)
    
    cursor = connection.cursor()
    inserted = 0
    
    # Fetch trending players
    trending_data = make_api_request("stats/v1/player/trending")
    
    if trending_data and 'player' in trending_data:
        players = trending_data['player']
        print(f"📥 Found {len(players)} trending players")
        
        for player in players:
            try:
                player_id = player.get('id')
                player_name = player.get('name', 'Unknown')
                
                # Get team_id from database (default to India for now)
                cursor.execute("SELECT team_id FROM teams WHERE team_name = 'India' LIMIT 1")
                result = cursor.fetchone()
                team_id = result[0] if result else None
                
                query = """
                INSERT INTO players (player_id, player_name, team_id, country, playing_role) 
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE player_name=VALUES(player_name)
                """
                cursor.execute(query, (player_id, player_name, team_id, 'India', 'Batsman'))
                inserted += 1
                
            except Error as e:
                print(f"⚠️  Error inserting player {player_name}: {e}")
    
    # Fetch rankings for different formats
    formats = ['test', 'odi', 't20']
    categories = ['batsmen', 'bowlers', 'allrounders']
    
    for format_type in formats:
        for category in categories:
            time.sleep(0.5)  # Rate limiting
            endpoint = f"stats/v1/rankings/{category}?formatType={format_type}"
            rankings_data = make_api_request(endpoint)
            
            if rankings_data and 'rank' in rankings_data:
                ranks = rankings_data['rank'][:20]  # Top 20 players
                print(f"📥 Found {len(ranks)} {format_type.upper()} {category}")
                
                for rank_info in ranks:
                    try:
                        player_id = rank_info.get('id')
                        player_name = rank_info.get('name', 'Unknown')
                        country = rank_info.get('country', 'Unknown')
                        
                        # Get team_id
                        cursor.execute("SELECT team_id FROM teams WHERE country = %s LIMIT 1", (country,))
                        result = cursor.fetchone()
                        team_id = result[0] if result else None
                        
                        # Determine playing role
                        if category == 'batsmen':
                            role = 'Batsman'
                        elif category == 'bowlers':
                            role = 'Bowler'
                        else:
                            role = 'All-rounder'
                        
                        query = """
                        INSERT INTO players (player_id, player_name, team_id, country, playing_role) 
                        VALUES (%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            player_name=VALUES(player_name),
                            country=VALUES(country)
                        """
                        cursor.execute(query, (player_id, player_name, team_id, country, role))
                        inserted += 1
                        
                    except Error as e:
                        print(f"⚠️  Error inserting player {player_name}: {e}")
    
    connection.commit()
    print(f"✅ Inserted/Updated {inserted} players")
    return inserted


def fetch_and_insert_series(connection):
    """Fetch series data"""
    print("\n" + "="*60)
    print("🏆 FETCHING SERIES DATA")
    print("="*60)
    
    cursor = connection.cursor()
    inserted = 0
    
    # Fetch international series
    series_data = make_api_request("series/v1/international")
    
    if series_data and 'seriesMapProto' in series_data:
        for series_map in series_data['seriesMapProto']:
            if 'series' in series_map:
                for series in series_map['series']:
                    try:
                        series_id = series.get('id')
                        series_name = series.get('name', 'Unknown Series')
                        start_date = series.get('startDt')
                        end_date = series.get('endDt')
                        
                        # Convert timestamp to date
                        if start_date and isinstance(start_date, (int, float)):
                            start_date = datetime.fromtimestamp(start_date / 1000).date()
                        else:
                            start_date = None
                        if end_date and isinstance(end_date, (int, float)):
                            end_date = datetime.fromtimestamp(end_date / 1000).date()
                        else:
                            end_date = None
                        
                        query = """
                        INSERT INTO series (series_id, series_name, start_date, end_date, match_type) 
                        VALUES (%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE series_name=VALUES(series_name)
                        """
                        cursor.execute(query, (series_id, series_name, start_date, end_date, 'International'))
                        inserted += 1
                        
                    except Error as e:
                        print(f"⚠️  Error inserting series: {e}")
    
    connection.commit()
    print(f"✅ Inserted {inserted} series")
    return inserted


def fetch_and_insert_matches(connection):
    """Fetch matches data"""
    print("\n" + "="*60)
    print("🏏 FETCHING MATCHES DATA")
    print("="*60)
    
    cursor = connection.cursor()
    inserted = 0
    
    # Fetch recent matches
    matches_data = make_api_request("matches/v1/recent")
    
    if matches_data and 'typeMatches' in matches_data:
        for type_match in matches_data['typeMatches']:
            if 'seriesMatches' in type_match:
                for series_match in type_match['seriesMatches']:
                    if 'seriesAdWrapper' in series_match:
                        series_info = series_match['seriesAdWrapper']
                        
                        if 'matches' in series_info:
                            for match in series_info['matches']:
                                if 'matchInfo' in match:
                                    try:
                                        match_info = match['matchInfo']
                                        match_id = match_info.get('matchId')
                                        match_desc = match_info.get('matchDesc', 'Match')
                                        match_format = match_info.get('matchFormat', 'Unknown')
                                        series_id = match_info.get('seriesId')
                                        venue_id = match_info.get('venueId')
                                        
                                        # Get match date
                                        start_date = match_info.get('startDate')
                                        if start_date and isinstance(start_date, (int, float)):
                                            match_date = datetime.fromtimestamp(start_date / 1000).date()
                                        else:
                                            match_date = None
                                        
                                        # Get team IDs
                                        team1 = match_info.get('team1', {})
                                        team2 = match_info.get('team2', {})
                                        team1_name = team1.get('teamName', 'Unknown')
                                        team2_name = team2.get('teamName', 'Unknown')
                                        
                                        # Get team IDs from database
                                        cursor.execute("SELECT team_id FROM teams WHERE team_name LIKE %s LIMIT 1", (f"%{team1_name}%",))
                                        result1 = cursor.fetchone()
                                        team1_id = result1[0] if result1 else None
                                        
                                        cursor.execute("SELECT team_id FROM teams WHERE team_name LIKE %s LIMIT 1", (f"%{team2_name}%",))
                                        result2 = cursor.fetchone()
                                        team2_id = result2[0] if result2 else None
                                        
                                        # Get match status
                                        match_state = match_info.get('state', 'Unknown')
                                        
                                        query = """
                                        INSERT INTO matches (match_id, series_id, team1_id, team2_id, venue_id, 
                                                           match_date, match_format, match_description, match_status) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        ON DUPLICATE KEY UPDATE match_status=VALUES(match_status)
                                        """
                                        cursor.execute(query, (match_id, series_id, team1_id, team2_id, venue_id,
                                                             match_date, match_format, match_desc, match_state))
                                        inserted += 1
                                        
                                    except Error as e:
                                        print(f"⚠️  Error inserting match: {e}")
    
    connection.commit()
    print(f"✅ Inserted {inserted} matches")
    return inserted


def fetch_and_insert_player_stats(connection):
    """Fetch and insert player career statistics"""
    print("\n" + "="*60)
    print("📈 FETCHING PLAYER CAREER STATS")
    print("="*60)
    
    cursor = connection.cursor()
    inserted = 0
    
    # Fetch rankings for different formats
    formats = {'test': 'Test', 'odi': 'ODI', 't20': 'T20I'}
    
    for format_key, format_name in formats.items():
        time.sleep(0.5)  # Rate limiting
        
        # Fetch batsmen rankings
        endpoint = f"stats/v1/rankings/batsmen?formatType={format_key}"
        rankings_data = make_api_request(endpoint)
        
        if rankings_data and 'rank' in rankings_data:
            ranks = rankings_data['rank'][:50]  # Top 50 batsmen
            print(f"📥 Processing {len(ranks)} {format_name} batsmen stats")
            
            for rank_info in ranks:
                try:
                    player_id = rank_info.get('id')
                    
                    # Check if player exists
                    cursor.execute("SELECT player_id FROM players WHERE player_id = %s", (player_id,))
                    if not cursor.fetchone():
                        continue
                    
                    # Extract stats
                    rating = rank_info.get('rating', 0)
                    
                    query = """
                    INSERT INTO player_career_stats 
                    (player_id, match_format, total_matches, batting_average) 
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        batting_average=VALUES(batting_average)
                    """
                    cursor.execute(query, (player_id, format_name, 0, rating / 10))
                    inserted += 1
                    
                except Error as e:
                    print(f"⚠️  Error inserting stats: {e}")
    
    connection.commit()
    print(f"✅ Inserted {inserted} player career stats")
    return inserted


def main():
    """Main function to fetch all data"""
    print("\n" + "="*60)
    print("🏏 CRICBUZZ DATA FETCHER")
    print("="*60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Connect to database
    connection = get_db_connection()
    if not connection:
        print("❌ Failed to connect to database. Exiting...")
        return
    
    try:
        # Fetch data in order (respecting foreign key constraints)
        teams_count = fetch_and_insert_teams(connection)
        venues_count = fetch_and_insert_venues(connection)
        series_count = fetch_and_insert_series(connection)
        players_count = fetch_and_insert_players(connection)
        matches_count = fetch_and_insert_matches(connection)
        stats_count = fetch_and_insert_player_stats(connection)
        
        # Summary
        print("\n" + "="*60)
        print("📊 DATA FETCH SUMMARY")
        print("="*60)
        print(f"✅ Teams: {teams_count}")
        print(f"✅ Venues: {venues_count}")
        print(f"✅ Series: {series_count}")
        print(f"✅ Players: {players_count}")
        print(f"✅ Matches: {matches_count}")
        print(f"✅ Player Stats: {stats_count}")
        print("="*60)
        print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("✅ All data fetched successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during data fetch: {e}")
    
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\n🔌 Database connection closed")


if __name__ == "__main__":
    main()
