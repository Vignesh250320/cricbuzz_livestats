import streamlit as st
import pandas as pd
from utils.query_executor import run_sql_query, execute_sql

st.set_page_config(page_title="🛠️ CRUD Operations", layout="wide")
st.title("🛠️ Player & Team Management")

operation = st.selectbox("Choose Operation", ["View Players", "Add Player", "Update Player", "Delete Player"])

if operation == "View Players":
    data = run_sql_query("SELECT player_id, full_name, country, playing_role, total_runs, total_wickets FROM Players ORDER BY full_name;")
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, width='stretch')
    else:
        st.info("No players found.")

elif operation == "Add Player":
    with st.form("add_form"):
        full_name = st.text_input("Full Name")
        country = st.text_input("Country")
        playing_role = st.selectbox("Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
        runs = st.number_input("Total Runs", 0)
        wickets = st.number_input("Total Wickets", 0)
        submit = st.form_submit_button("Add Player")
        if submit and full_name and country:
            sql = """INSERT INTO Players (full_name, country, playing_role, total_runs, total_wickets)
                     VALUES (%s, %s, %s, %s, %s);"""
            execute_sql(sql, (full_name, country, playing_role, runs, wickets))
            st.success(f"Player '{full_name}' added!")

elif operation == "Update Player":
    players = run_sql_query("SELECT player_id, full_name FROM Players;")
    if players:
        player_map = {p["full_name"]: p["player_id"] for p in players}
        selected = st.selectbox("Select Player", list(player_map.keys()))
        new_runs = st.number_input("Update Runs", 0)
        new_wickets = st.number_input("Update Wickets", 0)
        if st.button("Update"):
            execute_sql("UPDATE Players SET total_runs=%s, total_wickets=%s WHERE player_id=%s;",
                        (new_runs, new_wickets, player_map[selected]))
            st.success(f"Updated '{selected}' successfully!")

elif operation == "Delete Player":
    players = run_sql_query("SELECT player_id, full_name FROM Players;")
    if players:
        player_map = {p["full_name"]: p["player_id"] for p in players}
        selected = st.selectbox("Select Player to Delete", list(player_map.keys()))
        if st.button("Confirm Delete"):
            execute_sql("DELETE FROM Players WHERE player_id=%s;", (player_map[selected],))
            st.error(f"Player '{selected}' deleted successfully!")
