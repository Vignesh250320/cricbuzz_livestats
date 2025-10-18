import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

# Page config
st.set_page_config(page_title="Cricbuzz Stats", layout="wide")

def get_db_connection():
    """Create and return a database connection with detailed error handling"""
    try:
        # Force fresh connection each time
        conn = mysql.connector.connect(
            host='localhost',
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'vicky@123'),
            database=os.getenv('DB_NAME', 'cricbuzz_db'),
            port=int(os.getenv('DB_PORT', 3306)),
            connection_timeout=10,
            autocommit=True,
            charset='utf8mb4',
            use_unicode=True,
            pool_name=None,  # Disable connection pooling
            pool_size=1
        )
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"❌ Database connection failed: {e}")
        st.warning("⚠️ **Browser showing old error?** Press **Ctrl+Shift+R** to hard refresh!")
        st.info("💡 **Troubleshooting:**\n"
                "1. Hard refresh browser: **Ctrl+Shift+R** (Chrome) or **Ctrl+F5**\n"
                "2. Check MySQL: `sc query MySQL80`\n"
                "3. Test works in PowerShell but not browser? → Browser cache issue!")
        return None

# Title and connection test
st.title("🏏 Cricbuzz Live Stats Dashboard")

# Test connection on page load
with st.spinner("Checking database connection..."):
    test_conn = get_db_connection()
    if test_conn and test_conn.is_connected():
        st.success("✅ Database connected successfully!")
        test_conn.close()
    else:
        st.stop()  # Stop execution if connection fails

def get_recent_matches(limit=5):
    """Fetch recent matches from database"""
    conn = get_db_connection()
    if not conn:
        return None
        
    try:
        query = """
            SELECT 
                m.match_id, 
                t1.team_name as team1, 
                t2.team_name as team2, 
                m.match_date, 
                v.venue_name,
                m.winner_id,
                tw.team_name as winner_name
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            LEFT JOIN venues v ON m.venue_id = v.venue_id
            LEFT JOIN teams tw ON m.winner_id = tw.team_id
            ORDER BY m.match_date DESC
            LIMIT %s
        """
        df = pd.read_sql(query, conn, params=(limit,))
        return df
    except Error as e:
        st.error(f"Database error: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()

def get_players(search_query=None):
    """Fetch players from database with optional search"""
    conn = get_db_connection()
    if not conn:
        return None
        
    try:
        query = """
            SELECT 
                p.player_id, 
                p.player_name, 
                t.team_name, 
                p.batting_style, 
                p.bowling_style,
                p.date_of_birth,
                p.country
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.team_id
        """
        
        params = ()
        if search_query:
            query += " WHERE p.player_name LIKE %s OR t.team_name LIKE %s"
            search_term = f"%{search_query}%"
            params = (search_term, search_term)
            
        query += " ORDER BY p.player_name"
        
        df = pd.read_sql(query, conn, params=params)
        return df
    except Error as e:
        st.error(f"Error loading players: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()

# Sidebar for navigation
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Overview", "Players", "Matches", "Team Stats"]
)

# Page routing
if page == "Overview":
    st.header("📊 Overview")
    st.write("Welcome to Cricbuzz Live Stats Dashboard!")
    
    # Show recent matches
    st.subheader("Recent Matches")
    df_matches = get_recent_matches(5)
    
    if df_matches is not None and not df_matches.empty:
        for _, match in df_matches.iterrows():
            with st.container():
                cols = st.columns([1, 2, 1])
                with cols[0]:
                    st.markdown(f"**{match['team1']}**")
                with cols[1]:
                    st.markdown("<div style='text-align: center;'>vs</div>", unsafe_allow_html=True)
                with cols[2]:
                    st.markdown(f"**{match['team2']}**")
                
                venue = match.get('venue_name', 'Venue not specified')
                date_str = match['match_date'].strftime('%d %b %Y') if pd.notna(match['match_date']) else 'Date not available'
                st.caption(f"🏟️ {venue} | 📅 {date_str}")
                
                if pd.notna(match.get('winner_name')) and match.get('winner_name') != 'None':
                    st.success(f"🏆 Winner: {match['winner_name']}")
                else:
                    st.info("🤝 Match Drawn/No Result")
                
                st.markdown("---")

elif page == "Players":
    st.header("👥 Players")
    
    # Search box
    search_query = st.text_input("Search players by name or team:")
    
    # Get players data
    players_df = get_players(search_query if search_query else None)
    
    if players_df is not None:
        if not players_df.empty:
            st.write(f"Found {len(players_df)} players:")
            
            # Show as cards
            cols = st.columns(3)  # 3 columns for the cards
            
            for idx, player in players_df.iterrows():
                with cols[idx % 3]:
                    with st.container():
                        st.markdown(f"### {player['player_name']}")
                        st.markdown(f"**Team:** {player['team_name'] or 'N/A'}")
                        st.markdown(f"**Batting:** {player['batting_style'] or 'N/A'}")
                        st.markdown(f"**Bowling:** {player['bowling_style'] or 'N/A'}")
                        if pd.notna(player.get('date_of_birth')):
                            st.markdown(f"**Age:** {pd.Timestamp.now().year - pd.to_datetime(player['date_of_birth']).year}")
                        st.markdown("---")
        else:
            st.info("No players found matching your search.")