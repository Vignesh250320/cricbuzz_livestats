"""
Generate all 25 SQL queries from the SQLQueries class
This script extracts and displays all queries with their descriptions
"""

from src.features.sql_queries import SQLQueries

def generate_all_queries():
    """Generate and print all SQL queries"""
    
    queries = [
        # Beginner Level (1-8)
        ("Q1", "Find all players who represent India", SQLQueries.query_1_indian_players()),
        ("Q2", "Show all cricket matches played in last few days", SQLQueries.query_2_recent_matches()),
        ("Q3", "List top 10 highest run scorers in ODI", SQLQueries.query_3_top_odi_scorers()),
        ("Q4", "Display venues with capacity > 30,000", SQLQueries.query_4_large_venues()),
        ("Q5", "Calculate matches won by each team", SQLQueries.query_5_team_wins()),
        ("Q6", "Count players by playing role", SQLQueries.query_6_players_by_role()),
        ("Q7", "Highest individual batting score in each format", SQLQueries.query_7_highest_scores_by_format()),
        ("Q8", "Show all series that started in 2024", SQLQueries.query_8_series_2024()),
        
        # Intermediate Level (9-16)
        ("Q9", "All-rounders with 1000+ runs AND 50+ wickets", SQLQueries.query_9_allrounders()),
        ("Q10", "Last 20 completed matches with details", SQLQueries.query_10_recent_completed_matches()),
        ("Q11", "Player performance across different formats", SQLQueries.query_11_player_format_comparison()),
        ("Q12", "Team performance - Home vs Away", SQLQueries.query_12_home_away_performance()),
        ("Q13", "Batting partnerships with 100+ combined runs", SQLQueries.query_13_batting_partnerships()),
        ("Q14", "Bowling performance at different venues", SQLQueries.query_14_bowling_venue_analysis()),
        ("Q15", "Players performing well in close matches", SQLQueries.query_15_close_match_performers()),
        ("Q16", "Player batting performance trends over years", SQLQueries.query_16_performance_trends()),
        
        # Advanced Level (17-25)
        ("Q17", "Toss advantage analysis", SQLQueries.query_17_toss_advantage()),
        ("Q18", "Most economical bowlers in limited-overs", SQLQueries.query_18_economical_bowlers()),
        ("Q19", "Most consistent batsmen", SQLQueries.query_19_consistent_batsmen()),
        ("Q20", "Player experience across formats", SQLQueries.query_20_format_wise_experience()),
        ("Q21", "Comprehensive performance ranking", SQLQueries.query_21_performance_ranking()),
        ("Q22", "Head-to-head team analysis", SQLQueries.query_22_head_to_head()),
        ("Q23", "Recent player form analysis", SQLQueries.query_23_recent_form()),
        ("Q24", "Best batting partnerships analysis", SQLQueries.query_24_best_partnerships()),
        ("Q25", "Time-series career trajectory analysis", SQLQueries.query_25_career_trajectory()),
    ]
    
    print("=" * 80)
    print("CRICKET DATA ANALYTICS - 25 SQL QUERIES")
    print("=" * 80)
    print()
    
    # Beginner Level
    print("BEGINNER LEVEL (Questions 1-8)")
    print("-" * 80)
    for i in range(8):
        q_num, desc, query = queries[i]
        print(f"\n{q_num}: {desc}")
        print(query)
        print("-" * 80)
    
    # Intermediate Level
    print("\n\nINTERMEDIATE LEVEL (Questions 9-16)")
    print("-" * 80)
    for i in range(8, 16):
        q_num, desc, query = queries[i]
        print(f"\n{q_num}: {desc}")
        print(query)
        print("-" * 80)
    
    # Advanced Level
    print("\n\nADVANCED LEVEL (Questions 17-25)")
    print("-" * 80)
    for i in range(16, 25):
        q_num, desc, query = queries[i]
        print(f"\n{q_num}: {desc}")
        print(query)
        print("-" * 80)

if __name__ == "__main__":
    generate_all_queries()
