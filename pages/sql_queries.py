import streamlit as st
import pandas as pd
from utils.query_executor import run_sql_query

st.set_page_config(page_title="🧮 SQL Analytics", layout="wide")
st.title("🧮 SQL Practice Queries (25)")

st.markdown("Explore cricket analytics through 25 real SQL queries powered by your MySQL database.")
st.info("💡 Make sure your database has loaded player and match data before running queries.")

# =====================================================
# 25 Practice Queries (Structured by Difficulty)
# =====================================================

@st.cache_data(ttl=300)
def get_queries():
    return {
        # Beginner Level
        "1️⃣ Players from India": """SELECT full_name, playing_role, batting_style, bowling_style FROM Players WHERE country='India';""",
        "2️⃣ Recent Matches": """SELECT match_description, match_date, match_format, victory_type FROM Matches ORDER BY match_date DESC LIMIT 10;""",
        "3️⃣ Top 10 Run Scorers": """SELECT full_name, total_runs, batting_average FROM Players ORDER BY total_runs DESC LIMIT 10;""",
        "4️⃣ Venues with Capacity > 30,000": """SELECT venue_name, city, country, capacity FROM Venues WHERE capacity > 30000 ORDER BY capacity DESC;""",
        "5️⃣ Wins per Team": """SELECT team_name, total_wins FROM Teams ORDER BY total_wins DESC;""",
        "6️⃣ Player Count by Role": """SELECT playing_role, COUNT(*) AS Player_Count FROM Players GROUP BY playing_role;""",
        "7️⃣ Highest Score by Format": """SELECT match_format, MAX(bp.runs) AS Highest_Score FROM Batting_Performance bp JOIN Matches m ON bp.match_id=m.match_id GROUP BY match_format;""",
        "8️⃣ Series Started in 2024": """SELECT series_name, host_country, match_type, start_date FROM Series WHERE YEAR(start_date)=2024;""",

        # Intermediate Level
        "9️⃣ All-rounders with 1000+ Runs & 50+ Wickets": """SELECT full_name, total_runs, total_wickets FROM Players WHERE total_runs>1000 AND total_wickets>50;""",
        "🔟 Last 20 Completed Matches": """SELECT match_description, match_date, victory_type, victory_margin FROM Matches WHERE match_status='Completed' ORDER BY match_date DESC LIMIT 20;""",
        "11️⃣ Player Format Comparison": """SELECT p.full_name, SUM(CASE WHEN m.match_format='Test' THEN bp.runs ELSE 0 END) AS Test_Runs, SUM(CASE WHEN m.match_format='ODI' THEN bp.runs ELSE 0 END) AS ODI_Runs, SUM(CASE WHEN m.match_format='T20I' THEN bp.runs ELSE 0 END) AS T20_Runs FROM Batting_Performance bp JOIN Matches m ON bp.match_id=m.match_id JOIN Players p ON bp.player_id=p.player_id GROUP BY p.player_id, p.full_name HAVING COUNT(DISTINCT m.match_format)>=1;""",
        "12️⃣ Home vs Away Team Wins": """SELECT t.team_name, SUM(CASE WHEN v.country=t.country THEN 1 ELSE 0 END) AS Home_Wins, SUM(CASE WHEN v.country!=t.country THEN 1 ELSE 0 END) AS Away_Wins FROM Matches m JOIN Venues v ON m.venue_id=v.venue_id JOIN Teams t ON m.winning_team_id=t.team_id GROUP BY t.team_id, t.team_name;""",
        "13️⃣ 100+ Run Partnerships": """SELECT bp1.innings_id, p1.full_name AS Batsman1, p2.full_name AS Batsman2, (bp1.runs + bp2.runs) AS Partnership_Runs FROM Batting_Performance bp1 JOIN Batting_Performance bp2 ON bp1.innings_id=bp2.innings_id AND bp1.batting_position + 1 = bp2.batting_position JOIN Players p1 ON bp1.player_id=p1.player_id JOIN Players p2 ON bp2.player_id=p2.player_id WHERE (bp1.runs + bp2.runs)>=100 ORDER BY Partnership_Runs DESC;""",
        "14️⃣ Bowling Performance by Venue": """SELECT p.full_name, v.venue_name, AVG(bp.economy_rate) AS Avg_Economy, SUM(bp.wickets) AS Total_Wickets FROM Bowling_Performance bp JOIN Matches m ON bp.match_id=m.match_id JOIN Venues v ON m.venue_id=v.venue_id JOIN Players p ON bp.player_id=p.player_id GROUP BY p.player_id, p.full_name, v.venue_id, v.venue_name HAVING COUNT(DISTINCT m.match_id)>=1;""",
        "15️⃣ Player Performance in Close Matches": """SELECT p.full_name, AVG(bp.runs) AS Avg_Runs, COUNT(DISTINCT m.match_id) AS Close_Matches FROM Batting_Performance bp JOIN Matches m ON bp.match_id=m.match_id JOIN Players p ON bp.player_id=p.player_id WHERE (m.victory_type='runs' AND CAST(SUBSTRING_INDEX(m.victory_margin,' ',1) AS UNSIGNED)<50) OR (m.victory_type='wickets' AND CAST(SUBSTRING_INDEX(m.victory_margin,' ',1) AS UNSIGNED)<5) GROUP BY p.player_id, p.full_name HAVING Close_Matches>=1 ORDER BY Avg_Runs DESC;""",
        "16️⃣ Yearly Player Averages (Since 2020)": """SELECT p.full_name, YEAR(m.match_date) AS Year, AVG(bp.runs) AS Avg_Runs, AVG(bp.strike_rate) AS Avg_SR FROM Batting_Performance bp JOIN Matches m ON bp.match_id=m.match_id JOIN Players p ON bp.player_id=p.player_id WHERE YEAR(m.match_date)>=2020 GROUP BY p.player_id, p.full_name, YEAR(m.match_date);""",

        # Advanced Level
        "17️⃣ Toss Advantage Analysis": """SELECT toss_decision, COUNT(*) AS Total_Tosses, SUM(CASE WHEN toss_winner_id=winning_team_id THEN 1 ELSE 0 END) AS Toss_Winners_Won, ROUND(SUM(CASE WHEN toss_winner_id=winning_team_id THEN 1 ELSE 0 END)*100/COUNT(*),2) AS Win_Percentage FROM Matches GROUP BY toss_decision;""",
        "18️⃣ Most Economical Bowlers": """SELECT p.full_name, AVG(bp.economy_rate) AS Avg_Economy, SUM(bp.wickets) AS Total_Wickets FROM Bowling_Performance bp JOIN Players p ON bp.player_id=p.player_id JOIN Matches m ON bp.match_id=m.match_id WHERE m.match_format IN ('ODI','T20I') GROUP BY p.player_id, p.full_name HAVING COUNT(DISTINCT bp.match_id)>=1 ORDER BY Avg_Economy ASC LIMIT 15;""",
        "19️⃣ Consistent Batsmen (Low Std Dev)": """SELECT p.full_name, COUNT(bp.match_id) AS Innings, AVG(bp.runs) AS Avg_Runs, ROUND(STDDEV(bp.runs),2) AS StdDev_Runs, ROUND(STDDEV(bp.runs)/AVG(bp.runs),3) AS Consistency_Index FROM Batting_Performance bp JOIN Players p ON bp.player_id=p.player_id JOIN Matches m ON bp.match_id=m.match_id WHERE bp.balls_faced>=10 AND YEAR(m.match_date)>=2020 GROUP BY p.player_id, p.full_name HAVING COUNT(bp.match_id)>=2 ORDER BY Consistency_Index ASC;""",
        "20️⃣ Matches Played by Format": """SELECT p.full_name, SUM(CASE WHEN m.match_format='Test' THEN 1 ELSE 0 END) AS Test_Matches, SUM(CASE WHEN m.match_format='ODI' THEN 1 ELSE 0 END) AS ODI_Matches, SUM(CASE WHEN m.match_format='T20I' THEN 1 ELSE 0 END) AS T20_Matches FROM Batting_Performance bp JOIN Matches m ON bp.match_id=m.match_id JOIN Players p ON bp.player_id=p.player_id GROUP BY p.player_id, p.full_name HAVING (Test_Matches+ODI_Matches+T20_Matches)>=1;""",
        "21️⃣ Player Performance Ranking": """SELECT full_name, ROUND((COALESCE(total_runs,0)*0.01 + COALESCE(batting_average,0)*0.5 + COALESCE(strike_rate,0)*0.3 + COALESCE(total_wickets,0)*2 + (50-COALESCE(bowling_average,0))*0.5 + ((6-COALESCE(economy_rate,0))*2)),2) AS Performance_Score FROM Players ORDER BY Performance_Score DESC LIMIT 10;""",
        "22️⃣ Head-to-Head Team Stats": """SELECT t1.team_name AS Team1, t2.team_name AS Team2, COUNT(*) AS Total_Matches, SUM(CASE WHEN m.winning_team_id=t1.team_id THEN 1 ELSE 0 END) AS Team1_Wins, SUM(CASE WHEN m.winning_team_id=t2.team_id THEN 1 ELSE 0 END) AS Team2_Wins FROM Matches m JOIN Teams t1 ON m.team1_id=t1.team_id JOIN Teams t2 ON m.team2_id=t2.team_id GROUP BY t1.team_id, t1.team_name, t2.team_id, t2.team_name HAVING Total_Matches>=1;""",
        "23️⃣ Recent Player Form": """SELECT p.full_name, AVG(CASE WHEN m.match_date>=DATE_SUB(CURDATE(),INTERVAL 30 DAY) THEN bp.runs END) AS LastMonthAvg, AVG(bp.runs) AS OverallAvg FROM Batting_Performance bp JOIN Players p ON bp.player_id=p.player_id JOIN Matches m ON bp.match_id=m.match_id GROUP BY p.player_id, p.full_name;""",
        "24️⃣ Successful Batting Partnerships": """SELECT p1.full_name AS Player1, p2.full_name AS Player2, ROUND(AVG(bp1.runs+bp2.runs),2) AS Avg_Partnership, COUNT(*) AS Partnerships FROM Batting_Performance bp1 JOIN Batting_Performance bp2 ON bp1.innings_id=bp2.innings_id AND bp1.batting_position + 1 = bp2.batting_position JOIN Players p1 ON bp1.player_id=p1.player_id JOIN Players p2 ON bp2.player_id=p2.player_id GROUP BY p1.player_id, p1.full_name, p2.player_id, p2.full_name HAVING Partnerships>=1 ORDER BY Avg_Partnership DESC;""",
        "25️⃣ Quarterly Player Performance": """SELECT p.full_name, YEAR(m.match_date) AS Year, QUARTER(m.match_date) AS Quarter, ROUND(AVG(bp.runs),2) AS Avg_Runs, ROUND(AVG(bp.strike_rate),2) AS Avg_SR FROM Batting_Performance bp JOIN Matches m ON bp.match_id=m.match_id JOIN Players p ON bp.player_id=p.player_id GROUP BY p.player_id, p.full_name, YEAR(m.match_date), QUARTER(m.match_date) HAVING COUNT(bp.match_id)>=1;"""
    }

queries = get_queries()
selected = st.selectbox("Choose a Query", list(queries.keys()))
st.code(queries[selected], language="sql")

if st.button("▶️ Run Query"):
    with st.spinner("Executing SQL query..."):
        result = run_sql_query(queries[selected])
        if result:
            df = pd.DataFrame(result)
            st.dataframe(df, width='stretch')
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", data=csv, file_name=f"{selected}.csv", mime="text/csv")
        else:
            st.warning("No results or data mismatch. Ensure your database has proper data loaded.")
