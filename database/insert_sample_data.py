"""
Insert sample cricket data into the database
"""

import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

print("=" * 60)
print("🏏 INSERTING SAMPLE CRICKET DATA")
print("=" * 60)

# Database credentials
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "cb_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "cricbuzz_livestats")

try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    print("✅ Connected to database")
    
    # Insert Teams
    print("\n📋 Inserting Teams...")
    teams = [
        ('India', 'India'),
        ('Australia', 'Australia'),
        ('England', 'England'),
        ('Pakistan', 'Pakistan'),
        ('South Africa', 'South Africa'),
        ('New Zealand', 'New Zealand'),
        ('Sri Lanka', 'Sri Lanka'),
        ('West Indies', 'West Indies'),
        ('Bangladesh', 'Bangladesh'),
        ('Afghanistan', 'Afghanistan')
    ]
    cursor.executemany(
        "INSERT IGNORE INTO Teams (team_name, country) VALUES (%s, %s)",
        teams
    )
    print(f"   ✅ Inserted {cursor.rowcount} teams")
    
    # Insert Venues
    print("\n🏟️ Inserting Venues...")
    venues = [
        ('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
        ('Eden Gardens', 'Kolkata', 'India', 66000),
        ('Lords Cricket Ground', 'London', 'England', 31100),
        ('Wankhede Stadium', 'Mumbai', 'India', 33108),
        ('Wanderers Stadium', 'Johannesburg', 'South Africa', 34000),
        ('Sydney Cricket Ground', 'Sydney', 'Australia', 48000),
        ('MA Chidambaram Stadium', 'Chennai', 'India', 50000),
        ('The Oval', 'London', 'England', 25500),
        ('National Stadium', 'Karachi', 'Pakistan', 34228),
        ('Hagley Oval', 'Christchurch', 'New Zealand', 18000)
    ]
    cursor.executemany(
        "INSERT IGNORE INTO Venues (venue_name, city, country, capacity) VALUES (%s, %s, %s, %s)",
        venues
    )
    print(f"   ✅ Inserted {cursor.rowcount} venues")
    
    # Insert Players
    print("\n👤 Inserting Players...")
    players = [
        ('Virat Kohli', 'India', 'Batsman', 'Right-hand bat', None, 12000, 0, 50.5, 0, 90.5, 0),
        ('Rohit Sharma', 'India', 'Batsman', 'Right-hand bat', None, 11500, 0, 48.8, 0, 88.2, 0),
        ('Jasprit Bumrah', 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast', 500, 300, 22.0, 24.5, 70.0, 4.2),
        ('Steve Smith', 'Australia', 'Batsman', 'Right-hand bat', None, 9500, 0, 52.3, 0, 85.5, 0),
        ('Pat Cummins', 'Australia', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1200, 280, 28.5, 26.8, 75.0, 3.9),
        ('Joe Root', 'England', 'Batsman', 'Right-hand bat', None, 10500, 58, 49.8, 45.0, 82.0, 5.5),
        ('Ben Stokes', 'England', 'All-rounder', 'Left-hand bat', 'Right-arm medium', 5500, 185, 38.5, 32.5, 88.0, 4.8),
        ('Babar Azam', 'Pakistan', 'Batsman', 'Right-hand bat', None, 8500, 0, 54.2, 0, 87.5, 0),
        ('Kane Williamson', 'New Zealand', 'Batsman', 'Right-hand bat', None, 8200, 45, 51.8, 42.0, 80.5, 5.2),
        ('Kagiso Rabada', 'South Africa', 'Bowler', 'Right-hand bat', 'Right-arm fast', 800, 265, 30.5, 27.2, 72.0, 4.5),
        ('Quinton de Kock', 'South Africa', 'Wicket-keeper', 'Left-hand bat', None, 7500, 0, 44.5, 0, 92.0, 0),
        ('Ravindra Jadeja', 'India', 'All-rounder', 'Left-hand bat', 'Left-arm orthodox', 4800, 240, 36.8, 29.5, 85.5, 3.8),
        ('Trent Boult', 'New Zealand', 'Bowler', 'Left-hand bat', 'Left-arm fast', 650, 320, 28.0, 27.5, 68.0, 4.3),
        ('David Warner', 'Australia', 'Batsman', 'Left-hand bat', None, 8800, 0, 46.2, 0, 95.5, 0),
        ('Rashid Khan', 'Afghanistan', 'Bowler', 'Right-hand bat', 'Right-arm leg-spin', 1500, 380, 32.0, 18.5, 88.0, 4.0)
    ]
    cursor.executemany(
        """INSERT IGNORE INTO Players 
        (full_name, country, playing_role, batting_style, bowling_style, 
         total_runs, total_wickets, batting_average, bowling_average, strike_rate, economy_rate)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        players
    )
    print(f"   ✅ Inserted {cursor.rowcount} players")
    
    # Insert Series
    print("\n🏆 Inserting Series...")
    series = [
        ('ICC World Cup 2023', 'India', 'ODI', '2023-10-05', '2023-11-19'),
        ('ICC T20 World Cup 2024', 'West Indies', 'T20I', '2024-06-01', '2024-06-29'),
        ('The Ashes 2023', 'England', 'Test', '2023-06-16', '2023-07-31'),
        ('Border-Gavaskar Trophy 2023', 'India', 'Test', '2023-02-09', '2023-03-13'),
        ('Asia Cup 2023', 'Pakistan', 'ODI', '2023-08-30', '2023-09-17')
    ]
    cursor.executemany(
        "INSERT IGNORE INTO Series (series_name, host_country, match_type, start_date, end_date) VALUES (%s, %s, %s, %s, %s)",
        series
    )
    print(f"   ✅ Inserted {cursor.rowcount} series")
    
    # Get IDs for foreign keys
    cursor.execute("SELECT team_id, team_name FROM Teams")
    teams_dict = {name: id for id, name in cursor.fetchall()}
    
    cursor.execute("SELECT venue_id, venue_name FROM Venues")
    venues_dict = {name: id for id, name in cursor.fetchall()}
    
    cursor.execute("SELECT player_id, full_name FROM Players")
    players_dict = {name: id for id, name in cursor.fetchall()}
    
    # Insert Matches
    print("\n🏏 Inserting Matches...")
    base_date = datetime.now() - timedelta(days=30)
    matches = []
    
    # Sample matches
    match_data = [
        ('India vs Australia - Final', 'India', 'Australia', 'Wankhede Stadium', 'ODI', 'India', '6 wickets', 'wickets', 'India'),
        ('England vs Pakistan - Semi Final', 'England', 'Pakistan', 'Eden Gardens', 'ODI', 'England', '8 wickets', 'wickets', 'England'),
        ('Australia vs South Africa - Group Stage', 'Australia', 'South Africa', 'Sydney Cricket Ground', 'ODI', 'Australia', '5 wickets', 'wickets', 'South Africa'),
        ('India vs New Zealand - Group Stage', 'India', 'New Zealand', 'Melbourne Cricket Ground', 'ODI', 'India', '70 runs', 'runs', 'India'),
        ('England vs Australia - The Ashes Test 1', 'England', 'Australia', 'Lords Cricket Ground', 'Test', 'Australia', '2 wickets', 'wickets', 'Australia'),
    ]
    
    for i, (desc, t1, t2, venue, format, winner, margin, vtype, toss) in enumerate(match_data):
        match_date = base_date + timedelta(days=i*5)
        matches.append((
            desc,
            teams_dict.get(t1, 1),
            teams_dict.get(t2, 2),
            venues_dict.get(venue, 1),
            match_date.strftime('%Y-%m-%d'),
            format,
            teams_dict.get(winner, 1),
            margin,
            vtype,
            teams_dict.get(toss, 1),
            'bat',
            'Completed'
        ))
    
    cursor.executemany(
        """INSERT IGNORE INTO Matches 
        (match_description, team1_id, team2_id, venue_id, match_date, match_format,
         winning_team_id, victory_margin, victory_type, toss_winner_id, toss_decision, match_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        matches
    )
    print(f"   ✅ Inserted {cursor.rowcount} matches")
    
    # Get match IDs
    cursor.execute("SELECT match_id FROM Matches LIMIT 5")
    match_ids = [row[0] for row in cursor.fetchall()]
    
    # Insert Batting Performance
    print("\n🏏 Inserting Batting Performance...")
    batting_data = []
    for match_id in match_ids:
        # Add some batting performances
        batting_data.extend([
            (players_dict.get('Virat Kohli', 1), match_id, 1, 89, 75, 8, 2, 118.67, 3),
            (players_dict.get('Rohit Sharma', 2), match_id, 1, 45, 38, 6, 1, 118.42, 1),
            (players_dict.get('Steve Smith', 4), match_id, 2, 62, 85, 5, 0, 72.94, 4),
        ])
    
    cursor.executemany(
        """INSERT IGNORE INTO Batting_Performance 
        (player_id, match_id, innings_id, runs, balls_faced, fours, sixes, strike_rate, batting_position)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        batting_data
    )
    print(f"   ✅ Inserted {cursor.rowcount} batting records")
    
    # Insert Bowling Performance
    print("\n⚾ Inserting Bowling Performance...")
    bowling_data = []
    for match_id in match_ids:
        bowling_data.extend([
            (players_dict.get('Jasprit Bumrah', 3), match_id, 1, 10.0, 3, 45, 4.50, 2),
            (players_dict.get('Pat Cummins', 5), match_id, 2, 9.5, 2, 52, 5.47, 1),
        ])
    
    cursor.executemany(
        """INSERT IGNORE INTO Bowling_Performance 
        (player_id, match_id, innings_id, overs, wickets, runs_conceded, economy_rate, maidens)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        bowling_data
    )
    print(f"   ✅ Inserted {cursor.rowcount} bowling records")
    
    conn.commit()
    
    print("\n" + "=" * 60)
    print("✅ SAMPLE DATA INSERTED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📊 Summary:")
    cursor.execute("SELECT COUNT(*) FROM Teams")
    print(f"   Teams: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM Venues")
    print(f"   Venues: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM Players")
    print(f"   Players: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM Matches")
    print(f"   Matches: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM Batting_Performance")
    print(f"   Batting Records: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM Bowling_Performance")
    print(f"   Bowling Records: {cursor.fetchone()[0]}")
    
    print("\n✅ Your SQL queries will now return results!")
    print("=" * 60)

except mysql.connector.Error as e:
    print(f"\n❌ Database Error: {e}")
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
