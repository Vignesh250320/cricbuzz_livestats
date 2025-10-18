"""
SQL Queries Page - Practice 25 SQL queries with interactive execution
"""

import streamlit as st
import pandas as pd
from src.utils.db_connection import get_db_connection
from src.features.sql_queries import SQLQueries


def show():
    """Display SQL queries page"""
    
    st.title("🔍 SQL Analytics & Practice Queries")
    st.markdown("Practice 25+ SQL queries from beginner to advanced levels")
    
    # Tabs for different difficulty levels
    tab1, tab2, tab3, tab4 = st.tabs([
        "📚 Beginner (Q1-Q8)", 
        "📊 Intermediate (Q9-Q16)", 
        "🚀 Advanced (Q17-Q25)",
        "✏️ Custom Query"
    ])
    
    with tab1:
        display_beginner_queries()
    
    with tab2:
        display_intermediate_queries()
    
    with tab3:
        display_advanced_queries()
    
    with tab4:
        display_custom_query()


def display_beginner_queries():
    """Display beginner level queries"""
    
    st.subheader("📚 Beginner Level Queries (1-8)")
    st.markdown("Focus on basic SELECT, WHERE, GROUP BY, and ORDER BY operations")
    
    queries = {
        "Q1: Indian Players": {
            "description": "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
            "query": SQLQueries.query_1_indian_players()
        },
        "Q2: Recent Matches": {
            "description": "Show all cricket matches played in the last few days. Include match description, both team names, venue name with city, and match date.",
            "query": SQLQueries.query_2_recent_matches()
        },
        "Q3: Top ODI Scorers": {
            "description": "List top 10 highest run scorers in ODI cricket. Show player name, total runs, batting average, and centuries.",
            "query": SQLQueries.query_3_top_odi_scorers()
        },
        "Q4: Large Venues": {
            "description": "Display all cricket venues with seating capacity > 50,000. Show venue name, city, country, and capacity.",
            "query": SQLQueries.query_4_large_venues()
        },
        "Q5: Team Wins": {
            "description": "Calculate how many matches each team has won. Show team name and total wins.",
            "query": SQLQueries.query_5_team_wins()
        },
        "Q6: Players by Role": {
            "description": "Count how many players belong to each playing role (Batsman, Bowler, All-rounder, Wicket-keeper).",
            "query": SQLQueries.query_6_players_by_role()
        },
        "Q7: Highest Scores by Format": {
            "description": "Find the highest individual batting score in each cricket format (Test, ODI, T20I).",
            "query": SQLQueries.query_7_highest_scores_by_format()
        },
        "Q8: Series in 2024": {
            "description": "Show all cricket series that started in 2024. Include series name, host country, match type, and dates.",
            "query": SQLQueries.query_8_series_2024()
        }
    }
    
    display_query_section(queries)


def display_intermediate_queries():
    """Display intermediate level queries"""
    
    st.subheader("📊 Intermediate Level Queries (9-16)")
    st.markdown("Utilize JOINs, subqueries, and aggregate functions")
    
    queries = {
        "Q9: All-rounders Performance": {
            "description": "Find all-rounders with 1000+ runs AND 50+ wickets. Show player name, total runs, wickets, and format.",
            "query": SQLQueries.query_9_allrounders()
        },
        "Q10: Recent Completed Matches": {
            "description": "Get details of last 20 completed matches with team names, winner, victory margin, and venue.",
            "query": SQLQueries.query_10_recent_completed_matches()
        },
        "Q11: Format Comparison": {
            "description": "Compare player performance across different formats. Show runs in Test, ODI, T20I, and overall average.",
            "query": SQLQueries.query_11_player_format_comparison()
        },
        "Q12: Home vs Away Performance": {
            "description": "Analyze team performance when playing at home versus away. Count wins in both conditions.",
            "query": SQLQueries.query_12_home_away_performance()
        },
        "Q13: Batting Partnerships": {
            "description": "Identify partnerships where two batsmen scored 100+ combined runs in the same innings.",
            "query": SQLQueries.query_13_batting_partnerships()
        },
        "Q14: Bowling Venue Analysis": {
            "description": "Examine bowling performance at different venues. Calculate average economy, wickets, and matches.",
            "query": SQLQueries.query_14_bowling_venue_analysis()
        },
        "Q15: Close Match Performers": {
            "description": "Identify players who perform well in close matches (decided by <50 runs or <5 wickets).",
            "query": SQLQueries.query_15_close_match_performers()
        },
        "Q16: Performance Trends": {
            "description": "Track batting performance changes over years. Show average runs and strike rate per year since 2020.",
            "query": SQLQueries.query_16_performance_trends()
        }
    }
    
    display_query_section(queries)


def display_advanced_queries():
    """Display advanced level queries"""
    
    st.subheader("🚀 Advanced Level Queries (17-25)")
    st.markdown("Implement window functions, CTEs, and complex analytical calculations")
    
    queries = {
        "Q17: Toss Advantage": {
            "description": "Investigate toss advantage. Calculate win percentage for teams winning toss by their decision.",
            "query": SQLQueries.query_17_toss_advantage()
        },
        "Q18: Economical Bowlers": {
            "description": "Find most economical bowlers in limited-overs. Calculate economy rate and total wickets.",
            "query": SQLQueries.query_18_economical_bowlers()
        },
        "Q19: Consistent Batsmen": {
            "description": "Determine most consistent batsmen using standard deviation. Lower deviation = more consistent.",
            "query": SQLQueries.query_19_consistent_batsmen()
        },
        "Q20: Format-wise Experience": {
            "description": "Analyze player experience across formats. Show match counts and averages in Test, ODI, T20I.",
            "query": SQLQueries.query_20_format_wise_experience()
        },
        "Q21: Performance Ranking": {
            "description": "Create comprehensive performance ranking combining batting, bowling, and fielding metrics.",
            "query": SQLQueries.query_21_performance_ranking()
        },
        "Q22: Head-to-Head Analysis": {
            "description": "Build head-to-head analysis between teams. Show wins, margins, and performance patterns.",
            "query": SQLQueries.query_22_head_to_head()
        },
        "Q23: Recent Form": {
            "description": "Analyze recent player form. Compare last 5 vs last 10 matches and categorize form status.",
            "query": SQLQueries.query_23_recent_form()
        },
        "Q24: Best Partnerships": {
            "description": "Study successful batting partnerships. Calculate average runs, success rate, and highest partnership.",
            "query": SQLQueries.query_24_best_partnerships()
        },
        "Q25: Career Trajectory": {
            "description": "Time-series analysis of career evolution. Track quarterly performance and identify career phase.",
            "query": SQLQueries.query_25_career_trajectory()
        }
    }
    
    display_query_section(queries)


def display_query_section(queries):
    """
    Display query section with execution capability
    
    Args:
        queries: Dictionary of queries
    """
    
    for query_name, query_data in queries.items():
        with st.expander(f"📝 {query_name}", expanded=False):
            st.markdown(f"**Description:** {query_data['description']}")
            
            # Show SQL query
            st.code(query_data['query'], language='sql')
            
            # Execute button
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("▶️ Execute", key=f"exec_{query_name}"):
                    execute_query(query_data['query'], query_name)
            with col2:
                if st.button("📋 Copy Query", key=f"copy_{query_name}"):
                    st.info("Query copied to clipboard! (Use Ctrl+C on the code block)")


def display_custom_query():
    """Display custom query interface"""
    
    st.subheader("✏️ Custom SQL Query")
    st.markdown("Write and execute your own SQL queries")
    
    # Query input
    custom_query = st.text_area(
        "Enter your SQL query:",
        height=200,
        placeholder="SELECT * FROM players LIMIT 10;"
    )
    
    # Execute button
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if st.button("▶️ Execute Query", type="primary"):
            if custom_query.strip():
                execute_query(custom_query, "Custom Query")
            else:
                st.warning("Please enter a SQL query.")
    
    with col2:
        if st.button("🗑️ Clear"):
            st.rerun()
    
    # Query tips
    with st.expander("💡 Query Tips"):
        st.markdown("""
        ### Available Tables:
        - **teams**: team_id, team_name, country, team_type
        - **venues**: venue_id, venue_name, city, country, capacity
        - **players**: player_id, player_name, team_id, country, playing_role, batting_style, bowling_style
        - **series**: series_id, series_name, host_country, match_type, start_date, end_date
        - **matches**: match_id, series_id, team1_id, team2_id, venue_id, match_date, winner_id, etc.
        - **batting_stats**: stat_id, player_id, match_id, runs_scored, balls_faced, strike_rate, etc.
        - **bowling_stats**: stat_id, player_id, match_id, overs_bowled, wickets_taken, economy_rate, etc.
        - **player_career_stats**: career_stat_id, player_id, match_format, total_runs, batting_average, etc.
        
        ### Example Queries:
        ```sql
        -- Get all Indian players
        SELECT * FROM players WHERE country = 'India';
        
        -- Count players by role
        SELECT playing_role, COUNT(*) as count 
        FROM players 
        GROUP BY playing_role;
        
        -- Top run scorers
        SELECT player_name, total_runs 
        FROM player_career_stats pcs
        JOIN players p ON pcs.player_id = p.player_id
        ORDER BY total_runs DESC LIMIT 10;
        ```
        """)


def execute_query(query, query_name):
    """
    Execute SQL query and display results
    
    Args:
        query: SQL query string
        query_name: Name of the query
    """
    
    db = get_db_connection()
    
    with st.spinner(f"Executing {query_name}..."):
        try:
            results = db.execute_query(query, fetch=True)
            
            if results is not None:
                if len(results) > 0:
                    df = pd.DataFrame(results)
                    
                    # Display results
                    st.success(f"✅ Query executed successfully! Found {len(results)} rows.")
                    
                    # Show data
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv,
                        file_name=f"{query_name.replace(' ', '_').lower()}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("Query executed successfully but returned no results.")
            else:
                st.warning("No data returned. This might be because:")
                st.markdown("""
                - The database tables are empty
                - The query conditions don't match any records
                - There was an error executing the query
                
                **💡 Tip:** Make sure you have populated the database with sample data first using the CRUD Operations page.
                """)
        
        except Exception as e:
            st.error(f"❌ Error executing query: {e}")
            st.info("Please check your SQL syntax and try again.")


if __name__ == "__main__":
    show()
