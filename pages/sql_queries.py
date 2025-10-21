# pages/sql_queries.py
import streamlit as st
from utils.db_connection import run_query
from utils.api_handler import load_players_into_db

# 25 SQL queries grouped
QUERIES = {
    "Beginner": [
        ("Find all players from India with roles and styles",
         "SELECT player_id, name, playing_role, batting_style, bowling_style FROM Players WHERE country = 'India';"),
        ("Show matches played in last 7 days (sorted by date)",
         "SELECT * FROM Matches WHERE match_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) ORDER BY match_date DESC;"),
        ("Top 10 ODI run scorers with averages and centuries",
         "SELECT player_id, name, total_runs, batting_average FROM Players WHERE batting_average IS NOT NULL ORDER BY total_runs DESC LIMIT 10;"),
        ("Venues with capacity > 30000",
         "SELECT * FROM Venues WHERE capacity > 30000;"),
        ("Matches won by each team",
         "SELECT winning_team, COUNT(*) AS wins FROM Matches WHERE winning_team IS NOT NULL GROUP BY winning_team ORDER BY wins DESC;"),
        ("Count players by playing role",
         "SELECT playing_role, COUNT(*) AS count FROM Players GROUP BY playing_role;"),
        ("Highest batting score in each format",
         # Assuming Batting_Performance includes format in Matches.format join
         "SELECT m.format, bp.player_id, p.name, MAX(bp.runs) AS highest_score FROM Batting_Performance bp JOIN Matches m ON bp.match_id = m.match_id JOIN Players p ON bp.player_id = p.player_id GROUP BY m.format, bp.player_id, p.name ORDER BY m.format, highest_score DESC;"),
        ("Series started in 2024 (matches grouped by series/description)",
         "SELECT DISTINCT description, MIN(match_date) AS series_start FROM Matches WHERE YEAR(match_date) = 2024 GROUP BY description;")
    ],
    "Intermediate": [
        ("All-rounders with 1000+ runs AND 50+ wickets",
         "SELECT player_id, name, total_runs, total_wickets FROM Players WHERE total_runs >= 1000 AND total_wickets >= 50;"),
        ("Last 20 completed matches with details",
         "SELECT * FROM Matches WHERE winning_team IS NOT NULL ORDER BY match_date DESC LIMIT 20;"),
        ("Player performance comparison across formats (sample)",
         "SELECT p.player_id, p.name, m.format, SUM(bp.runs) AS runs, SUM(bw.wickets) AS wickets FROM Players p LEFT JOIN Batting_Performance bp ON p.player_id = bp.player_id LEFT JOIN Bowling_Performance bw ON p.player_id = bw.player_id LEFT JOIN Matches m ON bp.match_id = m.match_id OR bw.match_id = m.match_id GROUP BY p.player_id, m.format ORDER BY p.player_id;"),
        ("Team performance: home vs away",
         # Assumes Matches has venue/city info and Teams table
         "SELECT m.team1 AS team, SUM(CASE WHEN m.winning_team = m.team1 THEN 1 ELSE 0 END) AS home_wins FROM Matches m GROUP BY m.team1;"),
        ("Batting partnerships with 100+ combined runs",
         # Requires partnership table - best-effort: look for two-player same-innings combined runs
         "SELECT match_id, innings, SUM(runs) AS partnership_runs FROM Batting_Performance GROUP BY match_id, innings HAVING SUM(runs) >= 100;"),
        ("Bowling performance at venues (3+ matches)",
         "SELECT b.player_id, p.name, v.venue_id, v.name AS venue_name, AVG(b.economy_rate) AS avg_econ, COUNT(DISTINCT b.match_id) AS matches FROM Bowling_Performance b JOIN Players p ON b.player_id = p.player_id JOIN Matches m ON b.match_id = m.match_id JOIN Venues v ON m.venue_id = v.venue_id GROUP BY b.player_id, v.venue_id HAVING matches >= 3 ORDER BY avg_econ ASC;"),
        ("Player performance in close matches (margin < 10 runs/wickets)",
         "SELECT p.player_id, p.name, bp.match_id, bp.runs FROM Players p JOIN Batting_Performance bp ON p.player_id = bp.player_id JOIN Matches m ON bp.match_id = m.match_id WHERE (m.victory_margin IS NOT NULL AND CAST(m.victory_margin AS SIGNED) < 10) ORDER BY m.match_date DESC;"),
        ("Batting trends year-over-year (since 2020)",
         "SELECT YEAR(m.match_date) AS year, p.player_id, p.name, SUM(bp.runs) AS runs FROM Batting_Performance bp JOIN Matches m ON bp.match_id = m.match_id JOIN Players p ON bp.player_id = p.player_id WHERE YEAR(m.match_date) >= 2020 GROUP BY YEAR(m.match_date), p.player_id ORDER BY year, runs DESC;")
    ],
    "Advanced": [
        ("Toss advantage analysis (who wins more after winning toss)",
         "SELECT toss_winner, toss_decision, SUM(CASE WHEN winning_team = toss_winner THEN 1 ELSE 0 END) AS wins_after_toss, COUNT(*) AS matches FROM Matches GROUP BY toss_winner, toss_decision ORDER BY wins_after_toss DESC;"),
        ("Most economical bowlers in limited-overs (min 20 matches)",
         "SELECT bp.player_id, p.name, AVG(bp.economy_rate) AS avg_econ, COUNT(DISTINCT bp.match_id) AS matches FROM Bowling_Performance bp JOIN Players p ON bp.player_id = p.player_id JOIN Matches m ON bp.match_id = m.match_id WHERE m.format IN ('ODI','T20') GROUP BY bp.player_id HAVING matches >= 20 ORDER BY avg_econ ASC LIMIT 50;"),
        ("Most consistent batsmen (stddev of runs)",
         "SELECT bp.player_id, p.name, AVG(bp.runs) AS avg_runs, STDDEV_POP(bp.runs) AS sd_runs, COUNT(*) AS matches FROM Batting_Performance bp JOIN Players p ON bp.player_id = p.player_id GROUP BY bp.player_id HAVING matches >= 20 ORDER BY sd_runs ASC LIMIT 50;"),
        ("Player format-wise analysis (20+ total matches)",
         "SELECT p.player_id, p.name, m.format, COUNT(DISTINCT bp.match_id) AS matches, SUM(bp.runs) AS runs, SUM(bw.wickets) AS wickets FROM Players p LEFT JOIN Batting_Performance bp ON p.player_id = bp.player_id LEFT JOIN Bowling_Performance bw ON p.player_id = bw.player_id LEFT JOIN Matches m ON (bp.match_id = m.match_id OR bw.match_id = m.match_id) GROUP BY p.player_id, m.format HAVING SUM(COALESCE(bp.runs,0)) + SUM(COALESCE(bw.wickets,0)) IS NOT NULL;"),
        ("Comprehensive performance ranking system (sample using weighted score)",
         "SELECT p.player_id, p.name, (COALESCE(p.total_runs,0)*0.6 + COALESCE(p.total_wickets,0)*0.4) AS performance_score FROM Players p ORDER BY performance_score DESC LIMIT 100;"),
        ("Head-to-head match prediction analysis (historical wins)",
         "SELECT team1 AS team_a, team2 AS team_b, SUM(CASE WHEN winning_team = team1 THEN 1 ELSE 0 END) AS team1_wins, SUM(CASE WHEN winning_team = team2 THEN 1 ELSE 0 END) AS team2_wins FROM Matches GROUP BY team1, team2;"),
        ("Recent player form and momentum analysis (last 10 matches)",
         "SELECT bp.player_id, p.name, SUM(bp.runs) AS runs_last10, SUM(bw.wickets) AS wkts_last10 FROM Batting_Performance bp LEFT JOIN Bowling_Performance bw ON bp.player_id = bw.player_id LEFT JOIN Players p ON p.player_id = bp.player_id WHERE bp.match_id IN (SELECT match_id FROM Matches ORDER BY match_date DESC LIMIT 10) GROUP BY bp.player_id;"),
        ("Best batting partnerships study (top combined runs)",
         "SELECT match_id, innings, GROUP_CONCAT(CONCAT(player_id,':',runs) SEPARATOR ';') AS players_runs, SUM(runs) AS combined FROM Batting_Performance GROUP BY match_id, innings ORDER BY combined DESC LIMIT 50;"),
        ("Time-series performance evolution analysis (player level)",
         "SELECT YEAR(m.match_date) AS year, p.player_id, p.name, SUM(bp.runs) AS runs FROM Batting_Performance bp JOIN Matches m ON bp.match_id = m.match_id JOIN Players p ON bp.player_id = p.player_id GROUP BY YEAR(m.match_date), p.player_id ORDER BY p.player_id, year;")
    ]
}

def app():
    st.header("SQL Queries — Built-in Analytics (25 queries)")
    st.markdown("Choose a group and query, then execute against the connected DB.")

    group = st.selectbox("Group", ["Beginner", "Intermediate", "Advanced"])
    queries = QUERIES[group]

    q_label = [q[0] for q in queries]
    choice = st.selectbox("Query", q_label)
    idx = q_label.index(choice)
    sql = queries[idx][1]

    st.subheader("SQL")
    st.code(sql, language="sql")

    if st.button("Run Query"):
        rows = run_query(sql)
        if rows is None:
            st.error("Query failed or DB error. Check logs and connection.")
        elif len(rows) == 0:
            st.info("No results returned.")
        else:
            st.write(f"Returned {len(rows)} rows.")
            st.dataframe(rows)
