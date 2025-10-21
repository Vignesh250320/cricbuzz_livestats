# pages/live_matches.py
import streamlit as st
from utils.api_handler import get_live_matches, get_match_scorecard

def app():
    st.title("🏏 Live Matches — Cricbuzz API")
    st.markdown("View currently live cricket matches and fetch detailed scorecards in real time (via RapidAPI).")

    # Fetch live matches
    with st.spinner("Fetching live matches..."):
        matches = get_live_matches()

    if not matches:
        st.warning("No live matches found or API limit reached.")
        return

    # Display list of live matches
    st.subheader("🌍 Currently Live Matches")
    for m in matches:
        with st.expander(f"{m['team1']} vs {m['team2']} — {m['series']}"):
            st.write(f"**Match ID:** {m['id']}")
            st.write(f"**Status:** {m['status']}")

            if st.button(f"View Scorecard — {m['id']}", key=m['id']):
                with st.spinner("Fetching scorecard..."):
                    data = get_match_scorecard(m["id"])
                if not data:
                    st.error("No scorecard data found for this match.")
                    continue

                # Try to display summary info
                match_info = data.get("matchInfo", {})
                st.write("### Match Summary")
                col1, col2, col3 = st.columns(3)
                col1.metric("Team 1", match_info.get("team1", {}).get("teamName", "N/A"))
                col2.metric("Team 2", match_info.get("team2", {}).get("teamName", "N/A"))
                col3.metric("Status", match_info.get("status", "Unavailable"))

                # Display innings data if available
                innings = data.get("innings", [])
                if innings:
                    st.write("### 🏏 Innings Details")
                    for inn in innings:
                        st.markdown(f"**{inn.get('batTeamName','')}** — {inn.get('scoreDetails','')}")
                        if 'batsmen' in inn:
                            st.markdown("#### Batting")
                            st.table(inn['batsmen'])
                        if 'bowlers' in inn:
                            st.markdown("#### Bowling")
                            st.table(inn['bowlers'])
                else:
                    st.info("No innings data found yet.")
