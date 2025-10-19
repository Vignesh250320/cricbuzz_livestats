"""
CRUD Operations Page - Create, Read, Update, Delete operations for database management
"""

import streamlit as st
import pandas as pd
from src.utils.db_connection import get_db_connection
from datetime import datetime, date
import subprocess
import sys
import os


def show():
    """Display CRUD operations page"""
    
    st.title("🛠️ Database Management")
    
    # API-only mode notice
    st.info("📡 **API Data Mode**: This database uses real cricket data from Cricbuzz API. "
            "Manual CRUD operations are available for testing, but data is primarily managed via API.")
    
    # Tabs for different operations
    tab1, tab2, tab3 = st.tabs([
        "📖 View Data", 
        "🔄 Refresh from API",
        "🛠️ Manual Operations"
    ])
    
    with tab1:
        display_read_operations()  # View data
    
    with tab2:
        display_api_refresh()  # Refresh from API
    
    with tab3:
        st.subheader("🛠️ Manual Database Operations")
        st.warning("⚠️ Manual operations are for testing only. Use 'Refresh from API' tab to update data.")
        
        manual_tab1, manual_tab2, manual_tab3, manual_tab4 = st.tabs([
            "➕ Create", "✏️ Update", "🗑️ Delete", "📊 Sample Data"
        ])
        
        with manual_tab1:
            display_create_operations()
        with manual_tab2:
            display_update_operations()
        with manual_tab3:
            display_delete_operations()
        with manual_tab4:
            display_sample_data_loader()


def display_api_refresh():
    """Display API refresh interface"""
    st.subheader("🔄 Refresh Data from Cricbuzz API")
    
    st.markdown("""
    ### Fetch Latest Cricket Data
    
    This will fetch fresh data from the Cricbuzz API:
    - ✅ Latest teams and players
    - ✅ Recent matches
    - ✅ Current series
    - ✅ Player rankings and stats
    
    **Note:** Existing data will be updated, not replaced.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Fetch Latest Data", type="primary"):
            with st.spinner("Fetching data from Cricbuzz API..."):
                try:
                    # Run the API fetch script
                    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                    script_path = os.path.join(project_root, 'src', 'data', 'fetch_api_data.py')
                    
                    result = subprocess.run(
                        [sys.executable, script_path],
                        cwd=project_root,
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        st.success("✅ Data fetched successfully from API!")
                        st.info("Refresh the page to see updated data.")
                        
                        # Show summary from output
                        if "DATA FETCH SUMMARY" in result.stdout:
                            summary_start = result.stdout.find("DATA FETCH SUMMARY")
                            summary = result.stdout[summary_start:summary_start+500]
                            st.code(summary)
                    else:
                        st.error("❌ Error fetching data from API")
                        with st.expander("Show error details"):
                            st.code(result.stderr)
                            
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    with col2:
        if st.button("🗑️ Clear All & Fetch Fresh"):
            st.warning("⚠️ This will delete ALL existing data and fetch fresh from API!")
            if st.button("⚠️ Confirm Delete All"):
                with st.spinner("Clearing database and fetching fresh data..."):
                    try:
                        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                        script_path = os.path.join(project_root, 'clear_and_fetch_api.py')
                        
                        result = subprocess.run(
                            [sys.executable, script_path],
                            cwd=project_root,
                            capture_output=True,
                            text=True,
                            input="yes\n"
                        )
                        
                        if result.returncode == 0:
                            st.success("✅ Database cleared and fresh data fetched!")
                            st.info("Refresh the page to see new data.")
                        else:
                            st.error("❌ Error during operation")
                            with st.expander("Show details"):
                                st.code(result.stderr)
                    except Exception as e:
                        st.error(f"❌ Error: {e}")


def display_create_operations():
    """Display create operations"""
    
    st.subheader("➕ Create New Records")
    
    # Select entity type
    entity_type = st.selectbox(
        "Select entity to create:",
        ["Player", "Team", "Venue", "Series", "Match"]
    )
    
    if entity_type == "Player":
        create_player_form()
    elif entity_type == "Team":
        create_team_form()
    elif entity_type == "Venue":
        create_venue_form()
    elif entity_type == "Series":
        create_series_form()
    elif entity_type == "Match":
        create_match_form()


def create_player_form():
    """Form to create new player"""
    
    st.markdown("### Add New Player")
    
    with st.form("create_player_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            player_name = st.text_input("Player Name*", placeholder="e.g., Virat Kohli")
            country = st.text_input("Country*", placeholder="e.g., India")
            playing_role = st.selectbox("Playing Role*", 
                ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
            batting_style = st.selectbox("Batting Style", 
                ["Right-hand bat", "Left-hand bat", "N/A"])
        
        with col2:
            bowling_style = st.selectbox("Bowling Style", 
                ["Right-arm fast", "Left-arm fast", "Right-arm medium", "Left-arm medium",
                 "Right-arm off-break", "Right-arm leg-break", "Left-arm orthodox", "N/A"])
            dob = st.date_input("Date of Birth", 
                value=date(1990, 1, 1),
                min_value=date(1950, 1, 1),
                max_value=date.today())
            
            # Get teams for selection
            db = get_db_connection()
            teams = db.execute_query("SELECT team_id, team_name FROM teams ORDER BY team_name")
            team_options = {0: "None"}
            if teams:
                team_options.update({t['team_id']: t['team_name'] for t in teams})
            
            team_id = st.selectbox("Team", options=list(team_options.keys()), 
                format_func=lambda x: team_options[x])
        
        submitted = st.form_submit_button("➕ Add Player", type="primary")
        
        if submitted:
            if player_name and country:
                query = """
                INSERT INTO players (player_name, team_id, country, playing_role, 
                                   batting_style, bowling_style, date_of_birth)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                params = (
                    player_name,
                    team_id if team_id > 0 else None,
                    country,
                    playing_role,
                    batting_style if batting_style != "N/A" else None,
                    bowling_style if bowling_style != "N/A" else None,
                    dob
                )
                
                db = get_db_connection()
                result = db.execute_query(query, params, fetch=False)
                
                if result:
                    st.success(f"✅ Player '{player_name}' added successfully!")
                else:
                    st.error("❌ Failed to add player. Please try again.")
            else:
                st.warning("⚠️ Please fill all required fields (marked with *).")


def create_team_form():
    """Form to create new team"""
    
    st.markdown("### Add New Team")
    
    with st.form("create_team_form"):
        team_name = st.text_input("Team Name*", placeholder="e.g., India")
        country = st.text_input("Country*", placeholder="e.g., India")
        team_type = st.selectbox("Team Type", 
            ["International", "Domestic", "Franchise", "Other"])
        
        submitted = st.form_submit_button("➕ Add Team", type="primary")
        
        if submitted:
            if team_name and country:
                query = """
                INSERT INTO teams (team_name, country, team_type)
                VALUES (%s, %s, %s)
                """
                params = (team_name, country, team_type)
                
                db = get_db_connection()
                result = db.execute_query(query, params, fetch=False)
                
                if result:
                    st.success(f"✅ Team '{team_name}' added successfully!")
                else:
                    st.error("❌ Failed to add team. Team might already exist.")
            else:
                st.warning("⚠️ Please fill all required fields (marked with *).")


def create_venue_form():
    """Form to create new venue"""
    
    st.markdown("### Add New Venue")
    
    with st.form("create_venue_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            venue_name = st.text_input("Venue Name*", placeholder="e.g., Wankhede Stadium")
            city = st.text_input("City*", placeholder="e.g., Mumbai")
        
        with col2:
            country = st.text_input("Country*", placeholder="e.g., India")
            capacity = st.number_input("Capacity", min_value=0, value=30000, step=1000)
        
        submitted = st.form_submit_button("➕ Add Venue", type="primary")
        
        if submitted:
            if venue_name and city and country:
                query = """
                INSERT INTO venues (venue_name, city, country, capacity)
                VALUES (%s, %s, %s, %s)
                """
                params = (venue_name, city, country, capacity)
                
                db = get_db_connection()
                result = db.execute_query(query, params, fetch=False)
                
                if result:
                    st.success(f"✅ Venue '{venue_name}' added successfully!")
                else:
                    st.error("❌ Failed to add venue. Please try again.")
            else:
                st.warning("⚠️ Please fill all required fields (marked with *).")


def create_series_form():
    """Form to create new series"""
    
    st.markdown("### Add New Series")
    
    with st.form("create_series_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            series_name = st.text_input("Series Name*", placeholder="e.g., ICC World Cup 2024")
            host_country = st.text_input("Host Country*", placeholder="e.g., India")
            match_type = st.selectbox("Match Type*", ["Test", "ODI", "T20I", "T20"])
        
        with col2:
            start_date = st.date_input("Start Date*", value=date.today())
            end_date = st.date_input("End Date*", value=date.today())
            total_matches = st.number_input("Total Matches", min_value=1, value=10)
        
        submitted = st.form_submit_button("➕ Add Series", type="primary")
        
        if submitted:
            if series_name and host_country and start_date and end_date:
                query = """
                INSERT INTO series (series_name, host_country, match_type, 
                                  start_date, end_date, total_matches)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                params = (series_name, host_country, match_type, start_date, end_date, total_matches)
                
                db = get_db_connection()
                result = db.execute_query(query, params, fetch=False)
                
                if result:
                    st.success(f"✅ Series '{series_name}' added successfully!")
                else:
                    st.error("❌ Failed to add series. Please try again.")
            else:
                st.warning("⚠️ Please fill all required fields (marked with *).")


def create_match_form():
    """Form to create new match"""
    
    st.markdown("### Add New Match")
    st.info("💡 Make sure teams, venues, and series are created first.")
    
    # This is a simplified form - you can expand it
    st.markdown("Use the Sample Data tab to populate matches with complete data.")


def display_read_operations():
    """Display read operations"""
    
    st.subheader("📖 View Records")
    
    # Select table
    table = st.selectbox(
        "Select table to view:",
        ["players", "teams", "venues", "series", "matches", 
         "batting_stats", "bowling_stats", "player_career_stats"]
    )
    
    # Limit
    limit = st.slider("Number of records to display:", 10, 100, 50)
    
    if st.button("📊 Load Data", type="primary"):
        query = f"SELECT * FROM {table} LIMIT {limit}"
        
        db = get_db_connection()
        results = db.execute_query(query)
        
        if results:
            df = pd.DataFrame(results)
            st.success(f"✅ Loaded {len(results)} records from '{table}' table")
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"{table}_data.csv",
                mime="text/csv"
            )
        else:
            st.info(f"No data found in '{table}' table. Add some records first!")


def display_update_operations():
    """Display update operations"""
    
    st.subheader("✏️ Update Records")
    
    # Select entity type
    entity_type = st.selectbox(
        "Select entity to update:",
        ["Player", "Team", "Venue"]
    )
    
    if entity_type == "Player":
        update_player_form()
    elif entity_type == "Team":
        update_team_form()
    elif entity_type == "Venue":
        update_venue_form()


def update_player_form():
    """Form to update player"""
    
    st.markdown("### Update Player Information")
    
    # Get all players
    db = get_db_connection()
    players = db.execute_query("SELECT player_id, player_name, country FROM players ORDER BY player_name")
    
    if not players:
        st.info("No players found. Add some players first!")
        return
    
    # Select player
    player_options = {p['player_id']: f"{p['player_name']} ({p['country']})" for p in players}
    selected_player_id = st.selectbox("Select Player", 
        options=list(player_options.keys()),
        format_func=lambda x: player_options[x])
    
    # Get player details
    player_data = db.execute_query(
        "SELECT * FROM players WHERE player_id = %s", 
        (selected_player_id,)
    )
    
    if player_data:
        player = player_data[0]
        
        with st.form("update_player_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                player_name = st.text_input("Player Name", value=player['player_name'])
                country = st.text_input("Country", value=player['country'])
                playing_role = st.selectbox("Playing Role", 
                    ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"],
                    index=["Batsman", "Bowler", "All-rounder", "Wicket-keeper"].index(player['playing_role']) 
                        if player['playing_role'] in ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"] else 0)
            
            with col2:
                batting_style = st.text_input("Batting Style", 
                    value=player['batting_style'] or "")
                bowling_style = st.text_input("Bowling Style", 
                    value=player['bowling_style'] or "")
            
            submitted = st.form_submit_button("✏️ Update Player", type="primary")
            
            if submitted:
                query = """
                UPDATE players 
                SET player_name = %s, country = %s, playing_role = %s,
                    batting_style = %s, bowling_style = %s
                WHERE player_id = %s
                """
                params = (player_name, country, playing_role, 
                         batting_style or None, bowling_style or None, 
                         selected_player_id)
                
                result = db.execute_query(query, params, fetch=False)
                
                if result:
                    st.success(f"✅ Player '{player_name}' updated successfully!")
                else:
                    st.error("❌ Failed to update player.")


def update_team_form():
    """Form to update team"""
    
    st.markdown("### Update Team Information")
    
    # Get all teams
    db = get_db_connection()
    teams = db.execute_query("SELECT team_id, team_name FROM teams ORDER BY team_name")
    
    if not teams:
        st.info("No teams found. Add some teams first!")
        return
    
    # Select team
    team_options = {t['team_id']: t['team_name'] for t in teams}
    selected_team_id = st.selectbox("Select Team", 
        options=list(team_options.keys()),
        format_func=lambda x: team_options[x])
    
    # Get team details
    team_data = db.execute_query(
        "SELECT * FROM teams WHERE team_id = %s", 
        (selected_team_id,)
    )
    
    if team_data:
        team = team_data[0]
        
        with st.form("update_team_form"):
            team_name = st.text_input("Team Name", value=team['team_name'])
            country = st.text_input("Country", value=team['country'])
            team_type = st.selectbox("Team Type", 
                ["International", "Domestic", "Franchise", "Other"],
                index=["International", "Domestic", "Franchise", "Other"].index(team['team_type']) 
                    if team['team_type'] in ["International", "Domestic", "Franchise", "Other"] else 0)
            
            submitted = st.form_submit_button("✏️ Update Team", type="primary")
            
            if submitted:
                query = """
                UPDATE teams 
                SET team_name = %s, country = %s, team_type = %s
                WHERE team_id = %s
                """
                params = (team_name, country, team_type, selected_team_id)
                
                result = db.execute_query(query, params, fetch=False)
                
                if result:
                    st.success(f"✅ Team '{team_name}' updated successfully!")
                else:
                    st.error("❌ Failed to update team.")


def update_venue_form():
    """Form to update venue"""
    
    st.markdown("### Update Venue Information")
    
    # Get all venues
    db = get_db_connection()
    venues = db.execute_query("SELECT venue_id, venue_name, city FROM venues ORDER BY venue_name")
    
    if not venues:
        st.info("No venues found. Add some venues first!")
        return
    
    # Select venue
    venue_options = {v['venue_id']: f"{v['venue_name']}, {v['city']}" for v in venues}
    selected_venue_id = st.selectbox("Select Venue", 
        options=list(venue_options.keys()),
        format_func=lambda x: venue_options[x])
    
    # Get venue details
    venue_data = db.execute_query(
        "SELECT * FROM venues WHERE venue_id = %s", 
        (selected_venue_id,)
    )
    
    if venue_data:
        venue = venue_data[0]
        
        with st.form("update_venue_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                venue_name = st.text_input("Venue Name", value=venue['venue_name'])
                city = st.text_input("City", value=venue['city'])
            
            with col2:
                country = st.text_input("Country", value=venue['country'])
                capacity = st.number_input("Capacity", value=venue['capacity'] or 0)
            
            submitted = st.form_submit_button("✏️ Update Venue", type="primary")
            
            if submitted:
                query = """
                UPDATE venues 
                SET venue_name = %s, city = %s, country = %s, capacity = %s
                WHERE venue_id = %s
                """
                params = (venue_name, city, country, capacity, selected_venue_id)
                
                result = db.execute_query(query, params, fetch=False)
                
                if result:
                    st.success(f"✅ Venue '{venue_name}' updated successfully!")
                else:
                    st.error("❌ Failed to update venue.")


def display_delete_operations():
    """Display delete operations"""
    
    st.subheader("🗑️ Delete Records")
    st.warning("⚠️ Warning: Deleting records is permanent and cannot be undone!")
    
    # Select entity type
    entity_type = st.selectbox(
        "Select entity to delete:",
        ["Player", "Team", "Venue", "Series"]
    )
    
    if entity_type == "Player":
        delete_player_form()
    elif entity_type == "Team":
        delete_team_form()
    elif entity_type == "Venue":
        delete_venue_form()
    elif entity_type == "Series":
        delete_series_form()


def delete_player_form():
    """Form to delete player"""
    
    st.markdown("### Delete Player")
    
    # Get all players
    db = get_db_connection()
    players = db.execute_query("SELECT player_id, player_name, country FROM players ORDER BY player_name")
    
    if not players:
        st.info("No players found.")
        return
    
    # Select player
    player_options = {p['player_id']: f"{p['player_name']} ({p['country']})" for p in players}
    selected_player_id = st.selectbox("Select Player to Delete", 
        options=list(player_options.keys()),
        format_func=lambda x: player_options[x])
    
    confirm = st.checkbox("I confirm I want to delete this player")
    
    if st.button("🗑️ Delete Player", type="primary", disabled=not confirm):
        query = "DELETE FROM players WHERE player_id = %s"
        result = db.execute_query(query, (selected_player_id,), fetch=False)
        
        if result:
            st.success("✅ Player deleted successfully!")
            st.rerun()
        else:
            st.error("❌ Failed to delete player.")


def delete_team_form():
    """Form to delete team"""
    
    st.markdown("### Delete Team")
    
    # Get all teams
    db = get_db_connection()
    teams = db.execute_query("SELECT team_id, team_name FROM teams ORDER BY team_name")
    
    if not teams:
        st.info("No teams found.")
        return
    
    # Select team
    team_options = {t['team_id']: t['team_name'] for t in teams}
    selected_team_id = st.selectbox("Select Team to Delete", 
        options=list(team_options.keys()),
        format_func=lambda x: team_options[x])
    
    confirm = st.checkbox("I confirm I want to delete this team")
    
    if st.button("🗑️ Delete Team", type="primary", disabled=not confirm):
        query = "DELETE FROM teams WHERE team_id = %s"
        result = db.execute_query(query, (selected_team_id,), fetch=False)
        
        if result:
            st.success("✅ Team deleted successfully!")
            st.rerun()
        else:
            st.error("❌ Failed to delete team.")


def delete_venue_form():
    """Form to delete venue"""
    
    st.markdown("### Delete Venue")
    
    # Get all venues
    db = get_db_connection()
    venues = db.execute_query("SELECT venue_id, venue_name FROM venues ORDER BY venue_name")
    
    if not venues:
        st.info("No venues found.")
        return
    
    # Select venue
    venue_options = {v['venue_id']: v['venue_name'] for v in venues}
    selected_venue_id = st.selectbox("Select Venue to Delete", 
        options=list(venue_options.keys()),
        format_func=lambda x: venue_options[x])
    
    confirm = st.checkbox("I confirm I want to delete this venue")
    
    if st.button("🗑️ Delete Venue", type="primary", disabled=not confirm):
        query = "DELETE FROM venues WHERE venue_id = %s"
        result = db.execute_query(query, (selected_venue_id,), fetch=False)
        
        if result:
            st.success("✅ Venue deleted successfully!")
            st.rerun()
        else:
            st.error("❌ Failed to delete venue.")


def delete_series_form():
    """Form to delete series"""
    
    st.markdown("### Delete Series")
    
    # Get all series
    db = get_db_connection()
    series_list = db.execute_query("SELECT series_id, series_name FROM series ORDER BY series_name")
    
    if not series_list:
        st.info("No series found.")
        return
    
    # Select series
    series_options = {s['series_id']: s['series_name'] for s in series_list}
    selected_series_id = st.selectbox("Select Series to Delete", 
        options=list(series_options.keys()),
        format_func=lambda x: series_options[x])
    
    confirm = st.checkbox("I confirm I want to delete this series")
    
    if st.button("🗑️ Delete Series", type="primary", disabled=not confirm):
        query = "DELETE FROM series WHERE series_id = %s"
        result = db.execute_query(query, (selected_series_id,), fetch=False)
        
        if result:
            st.success("✅ Series deleted successfully!")
            st.rerun()
        else:
            st.error("❌ Failed to delete series.")


def display_sample_data_loader():
    """Display sample data loader"""
    
    st.subheader("📊 Load Sample Data")
    st.markdown("Populate the database with sample cricket data for testing SQL queries")
    
    st.info("""
    💡 **What this does:**
    - Adds sample teams (India, Australia, England, etc.)
    - Adds sample players with statistics
    - Adds sample venues
    - Adds sample series and matches
    - Adds batting and bowling statistics
    """)
    
    if st.button("📥 Load Sample Data", type="primary"):
        load_sample_data()


def load_sample_data():
    """Load sample data into database"""
    
    db = get_db_connection()
    
    with st.spinner("Loading sample data..."):
        try:
            # Sample teams
            teams_data = [
                ("India", "India", "International"),
                ("Australia", "Australia", "International"),
                ("England", "England", "International"),
                ("Pakistan", "Pakistan", "International"),
                ("South Africa", "South Africa", "International"),
                ("New Zealand", "New Zealand", "International"),
                ("West Indies", "West Indies", "International"),
                ("Sri Lanka", "Sri Lanka", "International"),
            ]
            
            for team in teams_data:
                db.execute_query(
                    "INSERT IGNORE INTO teams (team_name, country, team_type) VALUES (%s, %s, %s)",
                    team, fetch=False
                )
            
            # Sample venues
            venues_data = [
                ("Wankhede Stadium", "Mumbai", "India", 33000),
                ("Melbourne Cricket Ground", "Melbourne", "Australia", 100000),
                ("Lord's Cricket Ground", "London", "England", 30000),
                ("Eden Gardens", "Kolkata", "India", 68000),
                ("Sydney Cricket Ground", "Sydney", "Australia", 48000),
            ]
            
            for venue in venues_data:
                db.execute_query(
                    "INSERT IGNORE INTO venues (venue_name, city, country, capacity) VALUES (%s, %s, %s, %s)",
                    venue, fetch=False
                )
            
            # Sample players
            players_data = [
                ("Virat Kohli", 1, "India", "Batsman", "Right-hand bat", None, "1988-11-05"),
                ("Rohit Sharma", 1, "India", "Batsman", "Right-hand bat", None, "1987-04-30"),
                ("Jasprit Bumrah", 1, "India", "Bowler", "Right-hand bat", "Right-arm fast", "1993-12-06"),
                ("Ravindra Jadeja", 1, "India", "All-rounder", "Left-hand bat", "Left-arm orthodox", "1988-12-06"),
                ("Steve Smith", 2, "Australia", "Batsman", "Right-hand bat", "Right-arm leg-break", "1989-06-02"),
                ("Pat Cummins", 2, "Australia", "Bowler", "Right-hand bat", "Right-arm fast", "1993-05-08"),
                ("Joe Root", 3, "England", "Batsman", "Right-hand bat", "Right-arm off-break", "1990-12-30"),
                ("Ben Stokes", 3, "England", "All-rounder", "Left-hand bat", "Right-arm fast-medium", "1991-06-04"),
            ]
            
            for player in players_data:
                db.execute_query(
                    """INSERT IGNORE INTO players 
                       (player_name, team_id, country, playing_role, batting_style, bowling_style, date_of_birth) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    player, fetch=False
                )
            
            # Sample career stats
            career_stats_data = [
                (1, "ODI", 280, 270, 13000, 58.2, 183, 48, 72),
                (1, "Test", 110, 180, 8600, 48.9, 254, 28, 30),
                (2, "ODI", 250, 240, 10000, 48.9, 264, 30, 50),
                (2, "Test", 55, 90, 3800, 45.2, 212, 10, 15),
                (3, "ODI", 80, 75, 2500, 35.5, 102, 2, 8),
                (3, "Test", 35, 50, 800, 18.2, 56, 0, 0),
            ]
            
            for stat in career_stats_data:
                db.execute_query(
                    """INSERT IGNORE INTO player_career_stats 
                       (player_id, match_format, total_matches, total_innings, total_runs, 
                        batting_average, highest_score, centuries, half_centuries) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    stat, fetch=False
                )
            
            st.success("✅ Sample data loaded successfully!")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Error loading sample data: {e}")


if __name__ == "__main__":
    show()
