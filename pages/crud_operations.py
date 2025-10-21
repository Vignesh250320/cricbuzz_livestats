# pages/crud_operations.py

import streamlit as st
from utils.db_connection import run_query, execute_statement
from utils.api_handler import load_players_into_db

def app():
    st.header("⚙️ CRUD — Players Table")

    st.write("Use this page to Create, Read, Update, and Delete players in the database.")

    # --- READ ---
    st.subheader("📋 Player List")
    players = run_query("SELECT * FROM Players")
    if players:
        st.dataframe(players)
    else:
        st.warning("No players found in the database.")

    st.divider()

    # --- CREATE ---
    st.subheader("➕ Add New Player")
    with st.form("add_player_form"):
        name = st.text_input("Player Name", "")
        country = st.text_input("Country", "")
        playing_role = st.selectbox("Playing Role", ["Batsman", "Bowler", "All-Rounder", "Wicket-Keeper"])
        batting_style = st.text_input("Batting Style (e.g. Right-hand bat)")
        bowling_style = st.text_input("Bowling Style (e.g. Right-arm offbreak)")

        submitted = st.form_submit_button("Add Player")
        if submitted:
            if name.strip():
                success = execute_statement("""
                    INSERT INTO Players (name, country, playing_role, batting_style, bowling_style)
                    VALUES (:name, :country, :playing_role, :batting_style, :bowling_style)
                """, {
                    "name": name,
                    "country": country,
                    "playing_role": playing_role,
                    "batting_style": batting_style,
                    "bowling_style": bowling_style
                })
                if success:
                    st.success(f"✅ Player '{name}' added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add player.")
            else:
                st.warning("Player name is required.")

    st.divider()

    # --- UPDATE ---
    st.subheader("✏️ Update Player Stats")
    player_list = run_query("SELECT player_id, name FROM Players")
    if player_list:
        player_dict = {f"{row[1]} (ID: {row[0]})": row[0] for row in player_list}
        selected_player = st.selectbox("Select Player to Update", list(player_dict.keys()))

        new_runs = st.number_input("Total Runs", min_value=0, step=1)
        new_wickets = st.number_input("Total Wickets", min_value=0, step=1)
        new_strike_rate = st.number_input("Strike Rate", min_value=0.0, step=0.1)
        new_bowling_avg = st.number_input("Bowling Average", min_value=0.0, step=0.1)

        if st.button("Update Player"):
            player_id = player_dict[selected_player]
            success = execute_statement("""
                UPDATE Players
                SET total_runs = :runs,
                    total_wickets = :wickets,
                    strike_rate = :sr,
                    bowling_average = :ba
                WHERE player_id = :pid
            """, {
                "runs": new_runs,
                "wickets": new_wickets,
                "sr": new_strike_rate,
                "ba": new_bowling_avg,
                "pid": player_id
            })
            if success:
                st.success(f"✅ Updated stats for {selected_player}")
                st.rerun()
            else:
                st.error("❌ Update failed.")
    else:
        st.info("No players available to update.")

    st.divider()

    # --- DELETE ---
    st.subheader("🗑️ Delete Player")
    if player_list:
        player_dict = {f"{row[1]} (ID: {row[0]})": row[0] for row in player_list}
        del_player = st.selectbox("Select Player to Delete", list(player_dict.keys()))

        if st.button("Delete Player"):
            player_id = player_dict[del_player]
            success = execute_statement("DELETE FROM Players WHERE player_id = :pid", {"pid": player_id})
            if success:
                st.success(f"🗑️ Player '{del_player}' deleted successfully.")
                st.rerun()
            else:
                st.error("❌ Failed to delete player.")
