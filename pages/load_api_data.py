# pages/load_api_data.py
import streamlit as st
from utils.api_handler import load_players_into_db

def app():
    st.header("📡 Load Player Data from Cricbuzz API")
    st.markdown("This will fetch player stats from live Cricbuzz matches via RapidAPI and store them into your database.")

    if st.button("🚀 Load Data Now"):
        with st.spinner("Fetching and loading player data..."):
            count = load_players_into_db()
        if count:
            st.success(f"✅ Successfully loaded {count} player records!")
        else:
            st.warning("⚠️ No data loaded. Possibly no live matches available.")
