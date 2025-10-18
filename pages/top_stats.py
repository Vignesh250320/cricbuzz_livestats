"""
Top Stats Page - Player statistics and rankings from Cricbuzz API
"""

import streamlit as st
import pandas as pd
from src.utils.api_helper import get_api_client


def show():
    """Display top stats page"""
    
    st.title("📊 Top Player Statistics")
    st.markdown("Batting and bowling leaders across different formats")
    
    # Initialize API client
    api_client = get_api_client()
    
    # Format selection
    format_type = st.selectbox(
        "Select Cricket Format",
        ["test", "odi", "t20"],
        format_func=lambda x: x.upper()
    )
    
    # Tabs for different statistics
    tab1, tab2, tab3 = st.tabs(["🏏 Batsmen", "⚾ Bowlers", "🌟 All-Rounders"])
    
    with tab1:
        st.subheader(f"Top Batsmen - {format_type.upper()}")
        display_batsmen_rankings(api_client, format_type)
    
    with tab2:
        st.subheader(f"Top Bowlers - {format_type.upper()}")
        display_bowlers_rankings(api_client, format_type)
    
    with tab3:
        st.subheader(f"Top All-Rounders - {format_type.upper()}")
        display_allrounders_rankings(api_client, format_type)


def display_batsmen_rankings(api_client, format_type):
    """Display batsmen rankings"""
    
    with st.spinner("Fetching batsmen rankings..."):
        data = api_client.get_rankings_batsmen(format_type)
    
    if not data:
        st.warning("Unable to fetch batsmen rankings. Please check your API connection.")
        st.info("💡 **Note:** The Cricbuzz API might require a premium subscription for rankings data.")
        display_sample_batsmen_data(format_type)
        return
    
    # Parse and display rankings
    try:
        rankings = parse_rankings(data)
        
        if rankings:
            df = pd.DataFrame(rankings)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No rankings data available.")
            display_sample_batsmen_data(format_type)
    except Exception as e:
        st.error(f"Error displaying rankings: {e}")
        display_sample_batsmen_data(format_type)


def display_bowlers_rankings(api_client, format_type):
    """Display bowlers rankings"""
    
    with st.spinner("Fetching bowlers rankings..."):
        data = api_client.get_rankings_bowlers(format_type)
    
    if not data:
        st.warning("Unable to fetch bowlers rankings. Please check your API connection.")
        st.info("💡 **Note:** The Cricbuzz API might require a premium subscription for rankings data.")
        display_sample_bowlers_data(format_type)
        return
    
    # Parse and display rankings
    try:
        rankings = parse_rankings(data)
        
        if rankings:
            df = pd.DataFrame(rankings)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No rankings data available.")
            display_sample_bowlers_data(format_type)
    except Exception as e:
        st.error(f"Error displaying rankings: {e}")
        display_sample_bowlers_data(format_type)


def display_allrounders_rankings(api_client, format_type):
    """Display all-rounders rankings"""
    
    with st.spinner("Fetching all-rounders rankings..."):
        data = api_client.get_rankings_allrounders(format_type)
    
    if not data:
        st.warning("Unable to fetch all-rounders rankings. Please check your API connection.")
        st.info("💡 **Note:** The Cricbuzz API might require a premium subscription for rankings data.")
        display_sample_allrounders_data(format_type)
        return
    
    # Parse and display rankings
    try:
        rankings = parse_rankings(data)
        
        if rankings:
            df = pd.DataFrame(rankings)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No rankings data available.")
            display_sample_allrounders_data(format_type)
    except Exception as e:
        st.error(f"Error displaying rankings: {e}")
        display_sample_allrounders_data(format_type)


def parse_rankings(data):
    """
    Parse rankings data from API response
    
    Args:
        data: API response JSON
    
    Returns:
        List of ranking dictionaries
    """
    rankings = []
    
    try:
        if isinstance(data, dict) and 'rank' in data:
            for rank_item in data['rank']:
                rankings.append({
                    'Rank': rank_item.get('rank', 'N/A'),
                    'Player': rank_item.get('name', 'N/A'),
                    'Country': rank_item.get('country', 'N/A'),
                    'Rating': rank_item.get('rating', 'N/A'),
                    'Points': rank_item.get('points', 'N/A')
                })
    except Exception as e:
        st.error(f"Error parsing rankings: {e}")
    
    return rankings


def display_sample_batsmen_data(format_type):
    """Display sample batsmen data"""
    
    st.markdown("### 📋 Sample Batsmen Statistics")
    
    sample_data = {
        'test': [
            {'Rank': 1, 'Player': 'Joe Root', 'Country': 'England', 'Runs': 11500, 'Average': 50.5, 'Centuries': 30},
            {'Rank': 2, 'Player': 'Steve Smith', 'Country': 'Australia', 'Runs': 9000, 'Average': 58.2, 'Centuries': 29},
            {'Rank': 3, 'Player': 'Kane Williamson', 'Country': 'New Zealand', 'Runs': 8500, 'Average': 54.1, 'Centuries': 28},
            {'Rank': 4, 'Player': 'Virat Kohli', 'Country': 'India', 'Runs': 8600, 'Average': 48.9, 'Centuries': 28},
            {'Rank': 5, 'Player': 'Rohit Sharma', 'Country': 'India', 'Runs': 3800, 'Average': 45.2, 'Centuries': 10},
        ],
        'odi': [
            {'Rank': 1, 'Player': 'Virat Kohli', 'Country': 'India', 'Runs': 13000, 'Average': 58.2, 'Centuries': 48},
            {'Rank': 2, 'Player': 'Rohit Sharma', 'Country': 'India', 'Runs': 10000, 'Average': 48.9, 'Centuries': 30},
            {'Rank': 3, 'Player': 'Babar Azam', 'Country': 'Pakistan', 'Runs': 5500, 'Average': 56.8, 'Centuries': 18},
            {'Rank': 4, 'Player': 'David Warner', 'Country': 'Australia', 'Runs': 6000, 'Average': 45.3, 'Centuries': 19},
            {'Rank': 5, 'Player': 'Quinton de Kock', 'Country': 'South Africa', 'Runs': 6200, 'Average': 44.5, 'Centuries': 17},
        ],
        't20': [
            {'Rank': 1, 'Player': 'Babar Azam', 'Country': 'Pakistan', 'Runs': 3500, 'Average': 45.5, 'Strike Rate': 128.5},
            {'Rank': 2, 'Player': 'Virat Kohli', 'Country': 'India', 'Runs': 4000, 'Average': 52.7, 'Strike Rate': 137.9},
            {'Rank': 3, 'Player': 'Rohit Sharma', 'Country': 'India', 'Runs': 3800, 'Average': 32.5, 'Strike Rate': 140.2},
            {'Rank': 4, 'Player': 'Aaron Finch', 'Country': 'Australia', 'Runs': 3100, 'Average': 34.2, 'Strike Rate': 142.5},
            {'Rank': 5, 'Player': 'Jos Buttler', 'Country': 'England', 'Runs': 2800, 'Average': 35.8, 'Strike Rate': 145.2},
        ]
    }
    
    df = pd.DataFrame(sample_data.get(format_type, []))
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.caption("📌 This is sample data. Connect to Cricbuzz API for live statistics.")


def display_sample_bowlers_data(format_type):
    """Display sample bowlers data"""
    
    st.markdown("### 📋 Sample Bowlers Statistics")
    
    sample_data = {
        'test': [
            {'Rank': 1, 'Player': 'Pat Cummins', 'Country': 'Australia', 'Wickets': 250, 'Average': 22.5, 'Economy': 2.85},
            {'Rank': 2, 'Player': 'Jasprit Bumrah', 'Country': 'India', 'Wickets': 150, 'Average': 21.8, 'Economy': 2.65},
            {'Rank': 3, 'Player': 'Kagiso Rabada', 'Country': 'South Africa', 'Wickets': 260, 'Average': 22.1, 'Economy': 3.05},
            {'Rank': 4, 'Player': 'James Anderson', 'Country': 'England', 'Wickets': 680, 'Average': 26.5, 'Economy': 2.88},
            {'Rank': 5, 'Player': 'R Ashwin', 'Country': 'India', 'Wickets': 500, 'Average': 23.8, 'Economy': 2.82},
        ],
        'odi': [
            {'Rank': 1, 'Player': 'Trent Boult', 'Country': 'New Zealand', 'Wickets': 200, 'Average': 25.2, 'Economy': 4.85},
            {'Rank': 2, 'Player': 'Jasprit Bumrah', 'Country': 'India', 'Wickets': 130, 'Average': 23.5, 'Economy': 4.62},
            {'Rank': 3, 'Player': 'Mitchell Starc', 'Country': 'Australia', 'Wickets': 220, 'Average': 22.8, 'Economy': 4.95},
            {'Rank': 4, 'Player': 'Rashid Khan', 'Country': 'Afghanistan', 'Wickets': 160, 'Average': 18.5, 'Economy': 4.15},
            {'Rank': 5, 'Player': 'Kagiso Rabada', 'Country': 'South Africa', 'Wickets': 140, 'Average': 27.2, 'Economy': 5.12},
        ],
        't20': [
            {'Rank': 1, 'Player': 'Rashid Khan', 'Country': 'Afghanistan', 'Wickets': 120, 'Average': 12.5, 'Economy': 6.15},
            {'Rank': 2, 'Player': 'Jasprit Bumrah', 'Country': 'India', 'Wickets': 70, 'Average': 19.8, 'Economy': 6.52},
            {'Rank': 3, 'Player': 'Adil Rashid', 'Country': 'England', 'Wickets': 90, 'Average': 21.2, 'Economy': 7.05},
            {'Rank': 4, 'Player': 'Wanindu Hasaranga', 'Country': 'Sri Lanka', 'Wickets': 65, 'Average': 15.8, 'Economy': 6.85},
            {'Rank': 5, 'Player': 'Tim Southee', 'Country': 'New Zealand', 'Wickets': 130, 'Average': 22.5, 'Economy': 8.12},
        ]
    }
    
    df = pd.DataFrame(sample_data.get(format_type, []))
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.caption("📌 This is sample data. Connect to Cricbuzz API for live statistics.")


def display_sample_allrounders_data(format_type):
    """Display sample all-rounders data"""
    
    st.markdown("### 📋 Sample All-Rounders Statistics")
    
    sample_data = {
        'test': [
            {'Rank': 1, 'Player': 'Ravindra Jadeja', 'Country': 'India', 'Runs': 2800, 'Wickets': 260, 'Rating': 385},
            {'Rank': 2, 'Player': 'Ben Stokes', 'Country': 'England', 'Runs': 6000, 'Wickets': 190, 'Rating': 365},
            {'Rank': 3, 'Player': 'Jason Holder', 'Country': 'West Indies', 'Runs': 2500, 'Wickets': 150, 'Rating': 340},
            {'Rank': 4, 'Player': 'Shakib Al Hasan', 'Country': 'Bangladesh', 'Runs': 4200, 'Wickets': 230, 'Rating': 335},
            {'Rank': 5, 'Player': 'Kyle Jamieson', 'Country': 'New Zealand', 'Runs': 800, 'Wickets': 70, 'Rating': 310},
        ],
        'odi': [
            {'Rank': 1, 'Player': 'Shakib Al Hasan', 'Country': 'Bangladesh', 'Runs': 7200, 'Wickets': 310, 'Rating': 395},
            {'Rank': 2, 'Player': 'Mohammad Nabi', 'Country': 'Afghanistan', 'Runs': 3400, 'Wickets': 155, 'Rating': 325},
            {'Rank': 3, 'Player': 'Rashid Khan', 'Country': 'Afghanistan', 'Runs': 1100, 'Wickets': 160, 'Rating': 315},
            {'Rank': 4, 'Player': 'Chris Woakes', 'Country': 'England', 'Runs': 1200, 'Wickets': 150, 'Rating': 305},
            {'Rank': 5, 'Player': 'Glenn Maxwell', 'Country': 'Australia', 'Runs': 3600, 'Wickets': 55, 'Rating': 295},
        ],
        't20': [
            {'Rank': 1, 'Player': 'Shakib Al Hasan', 'Country': 'Bangladesh', 'Runs': 2200, 'Wickets': 130, 'Rating': 280},
            {'Rank': 2, 'Player': 'Mohammad Nabi', 'Country': 'Afghanistan', 'Runs': 1900, 'Wickets': 90, 'Rating': 265},
            {'Rank': 3, 'Player': 'Hardik Pandya', 'Country': 'India', 'Runs': 1500, 'Wickets': 60, 'Rating': 255},
            {'Rank': 4, 'Player': 'Glenn Maxwell', 'Country': 'Australia', 'Runs': 2200, 'Wickets': 45, 'Rating': 250},
            {'Rank': 5, 'Player': 'Wanindu Hasaranga', 'Country': 'Sri Lanka', 'Runs': 800, 'Wickets': 65, 'Rating': 245},
        ]
    }
    
    df = pd.DataFrame(sample_data.get(format_type, []))
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.caption("📌 This is sample data. Connect to Cricbuzz API for live statistics.")


if __name__ == "__main__":
    show()
