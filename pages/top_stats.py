import streamlit as st
import pandas as pd
from utils.api_handler import get_top_stats, get_icc_rankings

st.set_page_config(page_title="📊 Top Player Stats", layout="wide")

st.title("📊 Cricbuzz Top Player Stats & Rankings")

# Tab selection
tab1, tab2 = st.tabs(["🏆 Top Records", "🎯 ICC Rankings"])

# ==================== TOP RECORDS TAB ====================
with tab1:
    st.subheader("🏏 Cricket Records")
    
    col1, col2 = st.columns(2)
    
    with col1:
        format_map = {
            "All Formats": 0,
            "Test": 1,
            "ODI": 2,
            "T20": 3
        }
        format_type = st.selectbox("Select Format", list(format_map.keys()))
    
    with col2:
        stat_map = {
            "Most Runs": "mostRuns",
            "Most Wickets": "mostWickets",
            "Highest Scores": "highestScore",
            "Best Bowling": "bestBowling",
            "Most Hundreds": "mostHundreds",
            "Most Fifties": "mostFifties",
            "Most Sixes": "mostSixes",
            "Most Fours": "mostFours"
        }
        stat_type = st.selectbox("Select Stat Type", list(stat_map.keys()))
    
    if st.button("📈 Fetch Records", type="primary"):
        with st.spinner("Fetching data..."):
            api_data = get_top_stats(format_map[format_type], stat_map[stat_type])
            
            if "error" in api_data:
                error_msg = api_data['error']
                status_code = api_data.get('status_code', 'Unknown')
                
                if status_code == 404:
                    st.warning(f"⚠️ No data found (404) for {format_type} - {stat_type}")
                elif status_code == 403:
                    st.error(f"❌ Access Denied (403): Check your API key")
                elif status_code == 429:
                    st.error(f"❌ Rate Limit Exceeded (429): Please wait")
                else:
                    st.error(f"❌ API Error ({status_code}): {error_msg}")
            else:
                records = api_data.get("values", [])
                data = []
                for rec in records:
                    values = rec.get("values", [])
                    if len(values) >= 6:
                        data.append({
                            "Player ID": values[0],
                            "Name": values[1],
                            "Matches": values[2],
                            "Innings": values[3],
                            "Runs/Wickets": values[4],
                            "Average": values[5]
                        })
                
                if data:
                    df = pd.DataFrame(data)
                    st.success(f"✅ Top {len(data)} players in {stat_type}")
                    st.dataframe(df, width='stretch')
                    
                    # Visualization
                    try:
                        chart_data = df.set_index("Name")["Runs/Wickets"].astype(float).head(15)
                        st.bar_chart(chart_data)
                    except:
                        pass
                else:
                    st.warning("No data found or API limit reached.")

# ==================== ICC RANKINGS TAB ====================
with tab2:
    st.subheader("🌍 ICC Rankings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ranking_category = st.selectbox("Category", ["Batsmen", "Bowlers", "All-Rounders", "Teams"])
    
    with col2:
        ranking_format = st.selectbox("Format", ["Test", "ODI", "T20"])
    
    if st.button("🎯 Fetch Rankings", type="primary"):
        with st.spinner("Fetching ICC rankings..."):
            category_map = {
                "Batsmen": "batsmen",
                "Bowlers": "bowlers",
                "All-Rounders": "allrounders",
                "Teams": "teams"
            }
            
            api_data = get_icc_rankings(
                category_map[ranking_category], 
                ranking_format.lower()
            )
            
            if "error" in api_data:
                error_msg = api_data['error']
                status_code = api_data.get('status_code', 'Unknown')
                
                if status_code == 404:
                    st.warning(f"⚠️ No rankings found (404) for {ranking_format} {ranking_category}")
                elif status_code == 403:
                    st.error(f"❌ Access Denied (403): Check your API key")
                elif status_code == 429:
                    st.error(f"❌ Rate Limit Exceeded (429): Please wait")
                else:
                    st.error(f"❌ API Error ({status_code}): {error_msg}")
            else:
                rankings = api_data.get("rank", [])
                data = []
                
                for rank in rankings:
                    if ranking_category == "Teams":
                        data.append({
                            "Rank": rank.get("rank"),
                            "Team": rank.get("name"),
                            "Rating": rank.get("rating"),
                            "Points": rank.get("points")
                        })
                    else:
                        data.append({
                            "Rank": rank.get("rank"),
                            "Player": rank.get("name"),
                            "Country": rank.get("country"),
                            "Rating": rank.get("rating"),
                            "Points": rank.get("points", "")
                        })
                
                if data:
                    df = pd.DataFrame(data)
                    st.success(f"✅ ICC {ranking_format} {ranking_category} Rankings")
                    st.dataframe(df, width='stretch')
                    
                    # Top 10 chart
                    try:
                        if ranking_category == "Teams":
                            chart_data = df.set_index("Team")["Rating"].astype(float).head(10)
                        else:
                            chart_data = df.set_index("Player")["Rating"].astype(float).head(10)
                        st.bar_chart(chart_data)
                    except:
                        pass
                else:
                    st.warning("No rankings data found.")

st.markdown("---")
st.caption("💡 Data cached for 1 hour to reduce API calls")
