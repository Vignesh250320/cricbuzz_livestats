import streamlit as st

st.set_page_config(page_title="🏠 Home - Cricbuzz LiveStats", layout="wide")

# Header
st.title("🏏 Cricbuzz LiveStats")
st.markdown("### Cricket Analytics Dashboard with Live Match Data & SQL Query Interface")

st.divider()

# Project Overview
st.header("📋 Project Overview")

st.markdown("""
**Cricbuzz LiveStats** is a comprehensive cricket analytics platform built with Streamlit and MySQL. 
This application provides real-time cricket match data, player statistics, team analysis, and 
interactive SQL query capabilities.

### 🎯 Key Features

- **🔴 Live Match Data** - Real-time cricket match updates from Cricbuzz API
- **📊 Player Statistics** - Top batting and bowling records across formats
- **🏆 ICC Rankings** - Latest ICC rankings for players and teams
- **🧮 SQL Analytics** - 25 pre-built SQL queries for cricket data analysis
- **✏️ CRUD Operations** - Manage player and team data in the database
- **📈 Data Visualization** - Interactive charts and tables for insights
""")

st.divider()

# Technology Stack
st.header("🛠️ Technology Stack")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Frontend & Framework:**
    - 🎨 Streamlit - Interactive web framework
    - 📊 Pandas - Data manipulation
    - 📈 Plotly/Charts - Visualizations
    """)

with col2:
    st.markdown("""
    **Backend & Database:**
    - 🗄️ MySQL 8.0+ - Relational database
    - 🔌 MySQL Connector - DB connectivity
    - 🌐 Cricbuzz API (RapidAPI) - Live data
    """)

st.divider()

# Database Schema
st.header("🗄️ Database Schema")

st.markdown("""
The application uses a normalized MySQL database with the following tables:

- **Teams** - International cricket teams information
- **Venues** - Cricket stadiums and grounds
- **Players** - Player profiles with career statistics
- **Matches** - Match details and results
- **Batting_Performance** - Player batting stats per match
- **Bowling_Performance** - Player bowling stats per match  
- **Series** - Tournament and series information

All queries are optimized with proper indexing and follow MySQL best practices.
""")

st.divider()

# How to Use
st.header("📖 How to Use This Application")

st.markdown("""
1. **🏠 Home** - You are here! Project overview and information
2. **🏏 Live Matches** - View live, recent, and upcoming cricket matches
3. **📊 Top Stats** - Explore top batting/bowling records and ICC rankings
4. **🧮 SQL Queries** - Run 25 pre-built analytical queries on cricket data
5. **✏️ CRUD Operations** - Add, update, delete player and team records
""")

st.divider()

# About the Project
st.header("ℹ️ About This Project")

st.markdown("""
This project was developed as a comprehensive cricket analytics solution, combining:
- **Real-time API integration** for live match data
- **Robust database design** with proper normalization
- **SQL query interface** for data analysis
- **Modern UI/UX** with Streamlit

### 🎓 Learning Outcomes
- API integration and data fetching
- MySQL database design and optimization
- SQL query optimization with GROUP BY handling
- Streamlit app development
- Data visualization and analytics

### 📂 Project Structure
```
cricbuzz_livestats/
├── app.py                  # Main entry point
├── pages/                  # Individual Streamlit pages
├── utils/                  # Database and API utilities
├── database/              # Schema and setup files
└── notebooks/             # Jupyter notebooks for testing
```
""")

st.divider()

# Footer
st.info("💡 **Tip:** Use the sidebar to navigate between different sections of the application.")
st.caption("🏏 Cricbuzz LiveStats - Your Complete Cricket Analytics Platform")
