# pages/top_stats.py
import streamlit as st
from utils.db_connection import run_query
from utils.api_handler import load_players_into_db

def app():
    st.header("Top Stats")
    st.markdown("Top batting and bowling stats extracted from the DB.")

    # Example top queries (these rely on the Players table)
    top_bats_sql = """
    SELECT player_id, name, country, total_runs, batting_average
    FROM Players
    ORDER BY total_runs DESC
    LIMIT 10;
    """
    top_bowl_sql = """
    SELECT player_id, name, country, total_wickets, bowling_average, economy_rate
    FROM Players
    ORDER BY total_wickets DESC
    LIMIT 10;
    """

    st.subheader("Top 10 Run Scorers")
    rows = run_query(top_bats_sql) or []
    if rows:
        st.table(rows)
    else:
        st.info("No data — ensure DB and sample data loaded.")

    st.subheader("Top 10 Wicket Takers")
    rows2 = run_query(top_bowl_sql) or []
    if rows2:
        st.table(rows2)
    else:
        st.info("No data available.")
