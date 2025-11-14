"""Utility script to run selected SQL queries for debugging."""
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "cb_user",
    "password": "vicky@123",
    "database": "cricbuzz_livestats",
}

QUERIES = {
    "14": """
        SELECT p.full_name,
               v.venue_name,
               AVG(bp.economy_rate) AS Avg_Economy,
               SUM(bp.wickets) AS Total_Wickets,
               COUNT(DISTINCT m.match_id) AS Matches_At_Venue
        FROM Bowling_Performance bp
        JOIN Matches m ON bp.match_id = m.match_id
        JOIN Venues v ON m.venue_id = v.venue_id
        JOIN Players p ON bp.player_id = p.player_id
        WHERE bp.overs >= 4
        GROUP BY p.player_id, p.full_name, v.venue_id, v.venue_name
        HAVING COUNT(DISTINCT m.match_id) >= 3;
    """,
    "16": """
        SELECT p.full_name,
               YEAR(m.match_date) AS Year,
               ROUND(AVG(bp.runs), 2) AS Avg_Runs_Per_Match,
               ROUND(AVG(bp.strike_rate), 2) AS Avg_Strike_Rate
        FROM Batting_Performance bp
        JOIN Matches m ON bp.match_id = m.match_id
        JOIN Players p ON bp.player_id = p.player_id
        WHERE YEAR(m.match_date) >= 2020
        GROUP BY p.player_id, p.full_name, YEAR(m.match_date)
        HAVING COUNT(DISTINCT m.match_id) >= 5;
    """,
    "20": """
        SELECT p.full_name,
               SUM(CASE WHEN m.match_format = 'Test' THEN 1 ELSE 0 END) AS Test_Matches,
               SUM(CASE WHEN m.match_format = 'ODI' THEN 1 ELSE 0 END) AS ODI_Matches,
               SUM(CASE WHEN m.match_format = 'T20I' THEN 1 ELSE 0 END) AS T20_Matches,
               ROUND(AVG(CASE WHEN m.match_format = 'Test' THEN bp.runs END), 2) AS Test_Avg,
               ROUND(AVG(CASE WHEN m.match_format = 'ODI' THEN bp.runs END), 2) AS ODI_Avg,
               ROUND(AVG(CASE WHEN m.match_format = 'T20I' THEN bp.runs END), 2) AS T20_Avg
        FROM Batting_Performance bp
        JOIN Matches m ON bp.match_id = m.match_id
        JOIN Players p ON bp.player_id = p.player_id
        GROUP BY p.player_id, p.full_name
        HAVING (Test_Matches + ODI_Matches + T20_Matches) >= 20;
    """,
    "22": """
        SELECT t1.team_name AS Team1,
               t2.team_name AS Team2,
               COUNT(*) AS Total_Matches,
               SUM(CASE WHEN m.winning_team_id = t1.team_id THEN 1 ELSE 0 END) AS Team1_Wins,
               SUM(CASE WHEN m.winning_team_id = t2.team_id THEN 1 ELSE 0 END) AS Team2_Wins,
               ROUND(SUM(CASE WHEN m.winning_team_id = t1.team_id THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Team1_Win_Pct
        FROM Matches m
        JOIN Teams t1 ON m.team1_id = t1.team_id
        JOIN Teams t2 ON m.team2_id = t2.team_id
        WHERE m.match_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
        GROUP BY t1.team_id, t1.team_name, t2.team_id, t2.team_name
        HAVING Total_Matches >= 5;
    """,
    "25": """
        SELECT p.full_name,
               YEAR(m.match_date) AS Year,
               QUARTER(m.match_date) AS Quarter,
               ROUND(AVG(bp.runs), 2) AS Avg_Runs,
               ROUND(AVG(bp.strike_rate), 2) AS Avg_Strike_Rate,
               COUNT(DISTINCT m.match_id) AS Matches_In_Quarter
        FROM Batting_Performance bp
        JOIN Matches m ON bp.match_id = m.match_id
        JOIN Players p ON bp.player_id = p.player_id
        GROUP BY p.player_id, p.full_name, YEAR(m.match_date), QUARTER(m.match_date)
        HAVING COUNT(DISTINCT m.match_id) >= 3
           AND p.player_id IN (
                SELECT player_id
                FROM (
                    SELECT bp2.player_id,
                           COUNT(DISTINCT CONCAT(YEAR(m2.match_date), '-', QUARTER(m2.match_date))) AS Quarters_Count
                    FROM Batting_Performance bp2
                    JOIN Matches m2 ON bp2.match_id = m2.match_id
                    GROUP BY bp2.player_id
                    HAVING Quarters_Count >= 6
                ) q
           )
        ORDER BY p.full_name, Year, Quarter;
    """,
}


def run_queries():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    for number, sql in QUERIES.items():
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(f"Query {number}: {len(rows)} rows")
        for row in rows:
            print(row)
        print('-' * 60)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    run_queries()
