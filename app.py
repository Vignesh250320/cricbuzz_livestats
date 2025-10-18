"""
Cricbuzz LiveStats - Data Science Project
Cricket Data Analytics using Python, SQL, and Pandas
Technologies: Python, MySQL, Streamlit, Pandas, Data Analysis
"""

import streamlit as st
from src.utils.db_connection import initialize_database
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Cricket Data Analytics - Data Science Project",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main application function"""
    
    # Initialize database on first run
    if 'db_initialized' not in st.session_state:
        with st.spinner("Initializing database..."):
            if initialize_database():
                st.session_state.db_initialized = True
            else:
                st.error("Failed to initialize database. Please check your configuration.")
                st.stop()
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🏏 Cricket Data Analytics")
        st.markdown("**Data Science Project**")
        st.markdown("Python | SQL | Pandas | MySQL")
        st.markdown("---")
        
        # Navigation menu
        page = st.radio(
            "Navigation",
            ["🏠 Home", "📱 Live Matches", "📊 Top Stats", "🔍 SQL Queries", "🛠️ CRUD Operations"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Database status
        st.markdown("### 📊 Database Status")
        if check_database_connection():
            st.success("✅ Connected")
        else:
            st.error("❌ Disconnected")
        
        # API status
        st.markdown("### 🌐 API Status")
        if check_api_key():
            st.success("✅ Configured")
        else:
            st.warning("⚠️ Not configured")
        
        st.markdown("---")
        
        # Quick stats
        display_quick_stats()
        
        st.markdown("---")
        st.caption("**Data Science Technologies:**")
        st.caption("• Python Programming")
        st.caption("• SQL Database (MySQL)")
        st.caption("• Pandas for Data Analysis")
        st.caption("• Streamlit for Visualization")
        st.caption("• API Integration")
    
    # Main content area
    if page == "🏠 Home":
        from pages import home
        home.show()
    elif page == "📱 Live Matches":
        from pages import live_matches
        live_matches.show()
    elif page == "📊 Top Stats":
        from pages import top_stats
        top_stats.show()
    elif page == "🔍 SQL Queries":
        from pages import sql_queries
        sql_queries.show()
    elif page == "🛠️ CRUD Operations":
        from pages import crud_operations
        crud_operations.show()


def check_database_connection():
    """Check if database connection is working"""
    try:
        from utils.db_connection import get_db_connection
        db = get_db_connection()
        result = db.execute_query("SELECT 1", fetch=True)
        return result is not None
    except:
        return False


def check_api_key():
    """Check if API key is configured"""
    api_key = os.getenv('RAPIDAPI_KEY')
    return api_key is not None and api_key != ""


def display_quick_stats():
    """Display quick statistics in sidebar"""
    
    st.markdown("### 📈 Quick Stats")
    
    try:
        from utils.db_connection import get_db_connection
        db = get_db_connection()
        
        # Count players
        players = db.execute_query("SELECT COUNT(*) as count FROM players")
        player_count = players[0]['count'] if players else 0
        
        # Count teams
        teams = db.execute_query("SELECT COUNT(*) as count FROM teams")
        team_count = teams[0]['count'] if teams else 0
        
        # Count matches
        matches = db.execute_query("SELECT COUNT(*) as count FROM matches")
        match_count = matches[0]['count'] if matches else 0
        
        # Display metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Players", player_count)
            st.metric("Teams", team_count)
        with col2:
            st.metric("Matches", match_count)
            st.metric("Venues", "—")
    
    except Exception as e:
        st.caption("Stats unavailable")


if __name__ == "__main__":
    main()
