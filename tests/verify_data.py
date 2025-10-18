"""
Verify the data in the database
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'cricbuzz_db')
}

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

print("\n" + "="*70)
print("📊 DATABASE DATA VERIFICATION")
print("="*70)

# Check each table
tables = [
    'teams',
    'venues', 
    'players',
    'series',
    'matches',
    'batting_stats',
    'bowling_stats',
    'player_career_stats'
]

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"✅ {table.upper()}: {count} records")

print("\n" + "="*70)
print("📋 SAMPLE DATA FROM EACH TABLE")
print("="*70)

# Sample teams
print("\n🏏 TEAMS (First 5):")
cursor.execute("SELECT team_name, country FROM teams LIMIT 5")
for row in cursor.fetchall():
    print(f"  • {row[0]} ({row[1]})")

# Sample players
print("\n👥 PLAYERS (First 10):")
cursor.execute("SELECT player_name, country, playing_role FROM players LIMIT 10")
for row in cursor.fetchall():
    print(f"  • {row[0]} - {row[1]} ({row[2]})")

# Sample series
print("\n🏆 SERIES (First 5):")
cursor.execute("SELECT series_name FROM series LIMIT 5")
for row in cursor.fetchall():
    print(f"  • {row[0]}")

# Sample matches
print("\n🏏 MATCHES (First 5):")
cursor.execute("""
    SELECT m.match_description, t1.team_name, t2.team_name 
    FROM matches m
    LEFT JOIN teams t1 ON m.team1_id = t1.team_id
    LEFT JOIN teams t2 ON m.team2_id = t2.team_id
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"  • {row[0]}: {row[1]} vs {row[2]}")

print("\n" + "="*70)
print("✅ DATA VERIFICATION COMPLETE!")
print("💡 You can now run your 25 SQL queries!")
print("="*70)

cursor.close()
conn.close()
