"""
Main entry point for Streamlit app.
Run: streamlit run app.py
"""

import streamlit as st

st.set_page_config(page_title="Cricbuzz LiveStats", layout="wide")

st.title("🏏 Cricbuzz LiveStats — Real-Time Cricket Insights & SQL Analytics")

st.markdown(
    """
Use the left sidebar to navigate between pages:
- 🏠 Home (overview)
- 📡 Load Player Data (fetch real data from Cricbuzz API)
- 🟢 Live Matches (real-time from Cricbuzz API)
- 📊 Top Stats (top batting/bowling)
- 🧮 SQL Queries (25 analytics queries)
- 🧑‍💻 CRUD Operations (manage players in DB)
"""
)

# Sidebar navigation
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Load Player Data",
        "Live Matches",
        "Top Stats",
        "SQL Queries",
        "CRUD Operations",
    ],
)

# Page routing
if page == "Home":
    import pages.home as home
    home.app()
elif page == "Load Player Data":
    import pages.load_api_data as load_api_data
    load_api_data.app()
elif page == "Live Matches":
    import pages.live_matches as live_matches
    live_matches.app()
elif page == "Top Stats":
    import pages.top_stats as top_stats
    top_stats.app()
elif page == "SQL Queries":
    import pages.sql_queries as sql_queries
    sql_queries.app()
elif page == "CRUD Operations":
    import pages.crud_operations as crud
    crud.app()
