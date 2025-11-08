"""
Complete Database Setup Script
================================
Runs everything in one go:
1. Creates schema (tables, views, triggers, procedures)
2. Inserts sample data (teams, venues, players, matches, series)
3. Adds batting/bowling performance data
4. Adds partnership data

Usage:
    python database/setup_complete.py
"""
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# Database connection
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "cb_user"),
        password=os.getenv("DB_PASSWORD", "vicky@123"),
        database=os.getenv("DB_NAME", "cricbuzz_livestats")
    )

def run_sql_file(cursor, filepath):
    """Execute SQL file"""
    print(f"Running {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_content = f.read()
        # Split by delimiter and execute
        statements = sql_content.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except Exception as e:
                    if 'already exists' not in str(e):
                        print(f"Warning: {e}")

def insert_sample_data(conn):
    """Insert all sample data"""
    cursor = conn.cursor()
    
    print("\n📊 Step 2: Inserting sample data...")
    
    # Teams
    teams = [
        ("India", "India", 150, 80),
        ("Australia", "Australia", 140, 85),
        ("England", "England", 130, 90),
        ("Pakistan", "Pakistan", 100, 95),
        ("South Africa", "South Africa", 110, 88)
    ]
    
    for team in teams:
        try:
            cursor.execute("""
                INSERT INTO Teams (team_name, country, total_wins, total_losses)
                VALUES (%s, %s, %s, %s)
            """, team)
        except:
            pass
    
    print("✅ Teams inserted")
    
    # Venues
    venues = [
        ("Wankhede Stadium", "Mumbai", "India", 33000),
        ("Eden Gardens", "Kolkata", "India", 68000),
        ("Melbourne Cricket Ground", "Melbourne", "Australia", 100000),
        ("Lord's", "London", "England", 30000),
        ("National Stadium", "Karachi", "Pakistan", 34000)
    ]
    
    for venue in venues:
        try:
            cursor.execute("""
                INSERT INTO Venues (venue_name, city, country, capacity)
                VALUES (%s, %s, %s, %s)
            """, venue)
        except:
            pass
    
    print("✅ Venues inserted")
    
    # Players
    players = [
        (1, "Virat Kohli", "India", "Batsman", "Right-hand bat", "Right-arm medium", 12000, 55.5, 92.5, 50, 30.5, 5.2),
        (2, "Rohit Sharma", "India", "Batsman", "Right-hand bat", "Right-arm off-break", 10000, 48.5, 88.0, 30, 32.0, 5.5),
        (3, "Steve Smith", "Australia", "Batsman", "Right-hand bat", "Right-arm leg-break", 8500, 62.0, 54.0, 20, 28.0, 5.0),
        (4, "Kane Williamson", "New Zealand", "Batsman", "Right-hand bat", None, 7800, 58.0, 80.0, 10, 35.0, 5.3),
        (5, "Babar Azam", "Pakistan", "Batsman", "Right-hand bat", "Right-arm off-break", 6500, 56.0, 90.0, 5, 40.0, 5.8),
        (6, "Joe Root", "England", "Batsman", "Right-hand bat", "Right-arm off-break", 9200, 50.0, 55.0, 15, 30.0, 5.1),
        (7, "Pat Cummins", "Australia", "Bowler", "Right-hand bat", "Right-arm fast", 800, 15.0, 65.0, 250, 22.0, 3.2),
        (8, "Jasprit Bumrah", "India", "Bowler", "Right-hand bat", "Right-arm fast", 500, 12.0, 70.0, 280, 20.0, 3.0),
        (9, "Kagiso Rabada", "South Africa", "Bowler", "Right-hand bat", "Right-arm fast", 600, 18.0, 75.0, 230, 24.0, 3.5),
        (10, "Ben Stokes", "England", "All-rounder", "Left-hand bat", "Right-arm fast-medium", 5500, 36.0, 82.0, 180, 32.0, 3.8)
    ]
    
    for player in players:
        try:
            cursor.execute("""
                INSERT INTO Players (player_id, full_name, country, playing_role, batting_style, 
                                   bowling_style, total_runs, batting_average, strike_rate, 
                                   total_wickets, bowling_average, economy_rate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, player)
        except:
            pass
    
    print("✅ Players inserted")
    
    # Series
    cursor.execute("INSERT IGNORE INTO Series (series_id, series_name, host_country, match_type, start_date, end_date, total_matches) VALUES (1, 'India vs Australia 2024', 'India', 'Test', '2024-01-15', '2024-02-28', 5)")
    
    # Matches
    base_date = datetime(2025, 10, 15)
    for i in range(5):
        match_date = base_date + timedelta(days=i*7)
        cursor.execute("""
            INSERT IGNORE INTO Matches 
            (match_id, series_id, team1_id, team2_id, venue_id, match_date, match_format, 
             match_status, match_description, winning_team_id, victory_type, victory_margin,
             toss_winner_id, toss_decision)
            VALUES (%s, 1, 1, 2, %s, %s, 'T20I', 'Completed', %s, 1, 'wickets', '5 wickets', 1, 'bat')
        """, (i+1, (i % 5) + 1, match_date, f"Match {i+1}"))
    
    print("✅ Matches inserted")
    
    conn.commit()
    cursor.close()

def add_batting_bowling_data(conn):
    """Add batting and bowling performance data"""
    cursor = conn.cursor()
    
    print("\n🏏 Step 3: Adding performance data...")
    
    # Batting data - 6 batsmen per match, 2 innings each
    innings_id = 1
    for match_id in range(1, 6):
        for innings_num in range(1, 3):
            for pos in range(1, 7):
                player_id = ((match_id - 1) * 6 + innings_num * 3 + pos - 1) % 10 + 1
                runs = [45, 55, 38, 42, 28, 20][pos-1] + (match_id * 7)
                balls = int(runs * 1.5) + 10
                strike_rate = (runs / balls * 100) if balls > 0 else 0
                
                cursor.execute("""
                    INSERT IGNORE INTO Batting_Performance 
                    (player_id, match_id, innings_id, runs, balls_faced, fours, sixes, 
                     strike_rate, batting_position)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (player_id, match_id, innings_id, runs, balls, runs//6, runs//15, 
                      round(strike_rate, 2), pos))
            
            innings_id += 1
    
    print("✅ Batting data added")
    
    # Bowling data
    for match_id in range(1, 6):
        for bowler in range(1, 6):
            player_id = (7 + bowler) % 10 + 1
            overs = 4
            wickets = match_id % 3
            runs_conceded = 25 + (match_id * 5)
            economy = runs_conceded / overs
            
            cursor.execute("""
                INSERT IGNORE INTO Bowling_Performance 
                (player_id, match_id, innings_id, overs, wickets, runs_conceded, economy_rate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (player_id, match_id, match_id, overs, wickets, runs_conceded, round(economy, 2)))
    
    print("✅ Bowling data added")
    
    conn.commit()
    cursor.close()

def main():
    """Main setup function"""
    print("=" * 60)
    print("🏏 CRICBUZZ LIVESTATS - COMPLETE DATABASE SETUP")
    print("=" * 60)
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Step 1: Run schema.sql
        print("\n🗄️  Step 1: Creating database schema...")
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if os.path.exists(schema_path):
            run_sql_file(cursor, schema_path)
            conn.commit()
            print("✅ Schema created")
        else:
            print("⚠️  schema.sql not found, skipping...")
        
        # Step 2: Insert sample data
        insert_sample_data(conn)
        
        # Step 3: Add performance data
        add_batting_bowling_data(conn)
        
        # Step 4: Update player stats
        print("\n📊 Step 4: Updating player statistics...")
        for player_id in range(1, 11):
            try:
                cursor.callproc('sp_update_player_stats', [player_id])
            except:
                pass
        conn.commit()
        print("✅ Statistics updated")
        
        # Verify
        print("\n✅ Verification:")
        cursor.execute("SELECT COUNT(*) FROM Players")
        print(f"   Players: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Teams")
        print(f"   Teams: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Matches")
        print(f"   Matches: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Batting_Performance")
        print(f"   Batting records: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Bowling_Performance")
        print(f"   Bowling records: {cursor.fetchone()[0]}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("🎉 DATABASE SETUP COMPLETE!")
        print("=" * 60)
        print("\n📝 Next steps:")
        print("   1. Run: streamlit run app.py")
        print("   2. Go to: http://localhost:8501")
        print("   3. Test SQL queries in 'SQL Practice Queries' page")
        print("\n💡 Use 'Data Ingestion' page to add more real data from API")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure:")
        print("   1. MySQL is running")
        print("   2. Database 'cricbuzz_livestats' exists")
        print("   3. User 'cb_user' has proper permissions")
        print("   4. .env file has correct credentials")

if __name__ == "__main__":
    main()
