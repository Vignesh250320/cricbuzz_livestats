"""
Test each SQL query to find the one causing GROUP BY error
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
cursor = conn.cursor()

# Import queries from sql_queries.py
import sys
sys.path.append('pages')

# Test queries that might have GROUP BY issues
test_queries = {
    "13": """SELECT bp1.innings_id, p1.full_name AS Batsman1, p2.full_name AS Batsman2, (bp1.runs + bp2.runs) AS Partnership_Runs FROM Batting_Performance bp1 JOIN Batting_Performance bp2 ON bp1.innings_id=bp2.innings_id AND ABS(bp1.batting_position - bp2.batting_position)=1 JOIN Players p1 ON bp1.player_id=p1.player_id JOIN Players p2 ON bp2.player_id=p2.player_id WHERE (bp1.runs + bp2.runs)>=100;""",
    "16": """SELECT p.full_name, YEAR(m.match_date) AS Year, AVG(bp.runs) AS Avg_Runs, AVG(bp.strike_rate) AS Avg_SR FROM Batting_Performance bp JOIN Matches m ON bp.match_id=m.match_id JOIN Players p ON bp.player_id=p.player_id WHERE YEAR(m.match_date)>=2020 GROUP BY p.player_id, p.full_name, YEAR(m.match_date);""",
    "19": """SELECT p.full_name, COUNT(bp.match_id) AS Innings, AVG(bp.runs) AS Avg_Runs, ROUND(STDDEV(bp.runs),2) AS StdDev_Runs, ROUND(STDDEV(bp.runs)/AVG(bp.runs),3) AS Consistency_Index FROM Batting_Performance bp JOIN Players p ON bp.player_id=p.player_id JOIN Matches m ON bp.match_id=m.match_id WHERE bp.balls_faced>=10 AND YEAR(m.match_date)>=2020 GROUP BY p.player_id, p.full_name HAVING COUNT(bp.match_id)>=2 ORDER BY Consistency_Index ASC;""",
    "23": """SELECT p.full_name, AVG(CASE WHEN m.match_date>=DATE_SUB(CURDATE(),INTERVAL 30 DAY) THEN bp.runs END) AS LastMonthAvg, AVG(bp.runs) AS OverallAvg FROM Batting_Performance bp JOIN Players p ON bp.player_id=p.player_id JOIN Matches m ON bp.match_id=m.match_id GROUP BY p.player_id, p.full_name;""",
    "25": """SELECT p.full_name, YEAR(m.match_date) AS Year, QUARTER(m.match_date) AS Quarter, ROUND(AVG(bp.runs),2) AS Avg_Runs, ROUND(AVG(bp.strike_rate),2) AS Avg_SR FROM Batting_Performance bp JOIN Matches m ON bp.match_id=m.match_id JOIN Players p ON bp.player_id=p.player_id GROUP BY p.player_id, p.full_name, YEAR(m.match_date), QUARTER(m.match_date) HAVING COUNT(bp.match_id)>=1;"""
}

print("Testing queries for GROUP BY errors...\n")

for query_num, query_sql in test_queries.items():
    try:
        cursor.execute(query_sql)
        results = cursor.fetchall()
        print(f"✅ Query {query_num}: OK ({len(results)} rows)")
    except Exception as e:
        if "1055" in str(e):
            print(f"❌ Query {query_num}: GROUP BY ERROR")
            print(f"   Error: {str(e)[:200]}")
            print(f"   Query: {query_sql[:100]}...")
        else:
            print(f"⚠️ Query {query_num}: {str(e)[:100]}")

conn.close()
print("\nDone!")
