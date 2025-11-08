"""
Quick verification script for database
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "cb_user"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "cricbuzz_livestats")
)
cursor = conn.cursor(dictionary=True)

print("=" * 60)
print("🔍 DATABASE VERIFICATION")
print("=" * 60)

# Check tables and row counts
tables = ['Teams', 'Venues', 'Players', 'Matches', 'Batting_Performance', 'Bowling_Performance']

print("\n📊 Table Row Counts:")
for table in tables:
    cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
    count = cursor.fetchone()['count']
    print(f"   {table}: {count} rows")

# Check team wins
print("\n🏆 Team Statistics:")
cursor.execute("SELECT team_name, total_wins, total_losses, total_matches FROM Teams WHERE total_matches > 0")
teams = cursor.fetchall()
for team in teams:
    print(f"   {team['team_name']}: {team['total_wins']}W-{team['total_losses']}L ({team['total_matches']} matches)")

# Test a simple query
print("\n🏏 Top 3 Run Scorers:")
cursor.execute("SELECT full_name, total_runs FROM Players ORDER BY total_runs DESC LIMIT 3")
players = cursor.fetchall()
for p in players:
    print(f"   {p['full_name']}: {p['total_runs']} runs")

# Test view
print("\n👁️ Testing vw_match_summary view...")
try:
    cursor.execute("SELECT COUNT(*) as count FROM vw_match_summary")
    count = cursor.fetchone()['count']
    print(f"   ✅ View works! {count} matches found")
except Exception as e:
    print(f"   ❌ View error: {e}")

print("\n" + "=" * 60)
print("✅ VERIFICATION COMPLETE!")
print("=" * 60)

conn.close()
