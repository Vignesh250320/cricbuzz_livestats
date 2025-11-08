import streamlit as st

# ✅ Global App Configuration
st.set_page_config(
    page_title="🏏 Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
)

# ===============================
# 🧭 Sidebar Navigation
# ===============================
st.sidebar.title("🏏 Cricbuzz LiveStats")
st.sidebar.markdown("Your one-stop Cricket Analytics Dashboard")
st.sidebar.markdown("---")

st.sidebar.page_link("pages/home.py", label="🏠 Home")
st.sidebar.page_link("pages/live_matches.py", label="📺 Live Matches")
st.sidebar.page_link("pages/top_stats.py", label="📊 Top Player Stats")
st.sidebar.page_link("pages/data_ingestion.py", label="📥 Data Ingestion")
st.sidebar.page_link("pages/sql_queries.py", label="🧮 SQL Practice Queries")
st.sidebar.page_link("pages/crud_operations.py", label="🛠️ CRUD Operations")

st.sidebar.markdown("---")
st.sidebar.caption("Made with ❤️ using Streamlit, MySQL & Cricbuzz API")

# ===============================
# 🏠 Main Home Section
# ===============================
st.title("🏏 Welcome to Cricbuzz LiveStats Dashboard")

st.markdown("""
### 🚀 Explore Real-Time Cricket Insights  
**Cricbuzz LiveStats** brings you live data, player rankings, analytics, and direct database interaction.

#### 💡 Features
- 📺 **Live Matches** — Real-time data from Cricbuzz API  
- 📊 **Top Stats** — Most Runs, Wickets, Hundreds, etc.  
- 📥 **Data Ingestion** — Populate database with API data
- 🧮 **SQL Analytics** — 25 practice queries with visual results  
- 🛠️ **CRUD** — Manage your cricket data easily

---

Navigate using the sidebar to explore different sections.
""")
