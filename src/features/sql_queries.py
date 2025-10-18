"""
SQL Practice Queries - 25 Complete Queries
Organized by difficulty level: Beginner, Intermediate, Advanced
"""


class SQLQueries:
    """Collection of 25 SQL practice queries"""
    
    # ==================== BEGINNER LEVEL (1-8) ====================
    
    @staticmethod
    def query_1_indian_players():
        """Q1: Find all players who represent India"""
        return """
        SELECT 
            p.player_name AS 'Player Name',
            p.playing_role AS 'Role',
            p.batting_style AS 'Batting Style',
            p.bowling_style AS 'Bowling Style',
            t.team_name AS 'Team'
        FROM players p
        JOIN teams t ON p.team_id = t.team_id
        WHERE p.country = 'India'
        ORDER BY p.player_name
        LIMIT 10;
        """
    
    @staticmethod
    def query_2_recent_matches():
        """Q2: Show recent cricket matches"""
        return """
        SELECT 
            m.match_id AS 'Match ID',
            s.series_name AS 'Series',
            t1.team_name AS 'Team 1',
            t2.team_name AS 'Team 2',
            v.venue_name AS 'Venue',
            m.match_date AS 'Date',
            m.match_status AS 'Status',
            CASE 
                WHEN m.winner_id = t1.team_id THEN t1.team_name
                WHEN m.winner_id = t2.team_id THEN t2.team_name
                ELSE 'Draw/No Result'
            END AS 'Winner'
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        JOIN venues v ON m.venue_id = v.venue_id
        JOIN series s ON m.series_id = s.series_id
        ORDER BY m.match_date DESC
        LIMIT 10;
        """
    
    @staticmethod
    def query_3_top_odi_scorers():
        """Q3: List top 10 highest run scorers in ODI cricket"""
        return """
        SELECT 
            p.player_name AS 'Player',
            pcs.total_runs AS 'Runs',
            pcs.batting_average AS 'Avg',
            pcs.highest_score AS 'HS',
            pcs.centuries AS '100s',
            pcs.half_centuries AS '50s'
        FROM player_career_stats pcs
        JOIN players p ON pcs.player_id = p.player_id
        WHERE pcs.match_format = 'ODI'
        ORDER BY pcs.total_runs DESC
        LIMIT 10;
        """
    
    @staticmethod
    def query_4_large_venues():
        """Q4: Display venues with capacity > 50,000"""
        return """
        SELECT 
            venue_name AS 'Venue Name',
            city AS 'City',
            country AS 'Country',
            capacity AS 'Capacity'
        FROM venues
        WHERE capacity > 50000
        ORDER BY capacity DESC;
        """
    
    @staticmethod
    def query_5_team_wins():
        """Q5: Calculate matches won by each team"""
        return """
        SELECT 
            t.team_name AS 'Team Name',
            COUNT(m.match_id) AS 'Total Wins'
        FROM teams t
        LEFT JOIN matches m ON t.team_id = m.winner_id
        WHERE m.winner_id IS NOT NULL
        GROUP BY t.team_id, t.team_name
        ORDER BY COUNT(m.match_id) DESC;
        """
    
    @staticmethod
    def query_6_players_by_role():
        """Q6: Count players by playing role"""
        return """
        SELECT 
            playing_role AS 'Playing Role',
            COUNT(*) AS 'Number of Players'
        FROM players
        WHERE playing_role IS NOT NULL
        GROUP BY playing_role
        ORDER BY COUNT(*) DESC;
        """
    
    @staticmethod
    def query_7_highest_scores_by_format():
        """Q7: Highest individual batting score in each format"""
        return """
        SELECT 
            pcs.match_format AS 'Format',
            MAX(pcs.highest_score) AS 'Highest Score'
        FROM player_career_stats pcs
        WHERE pcs.highest_score IS NOT NULL
        GROUP BY pcs.match_format
        ORDER BY MAX(pcs.highest_score) DESC;
        """
    
    @staticmethod
    def query_8_series_2024():
        """Q8: Show all series that started in 2024"""
        return """
        SELECT 
            series_name AS 'Series Name',
            host_country AS 'Host Country',
            match_type AS 'Match Type',
            start_date AS 'Start Date',
            total_matches AS 'Total Matches'
        FROM series
        WHERE YEAR(start_date) = 2024
        ORDER BY start_date;
        """
    
    # ==================== INTERMEDIATE LEVEL (9-16) ====================
    
    @staticmethod
    def query_9_allrounders():
        """Q9: All-rounders with 1000+ runs AND 50+ wickets"""
        return """
        SELECT 
            p.player_name AS 'Player Name',
            pcs.total_runs AS 'Total Runs',
            pcs.total_wickets AS 'Total Wickets',
            pcs.match_format AS 'Format'
        FROM player_career_stats pcs
        JOIN players p ON pcs.player_id = p.player_id
        WHERE pcs.total_runs > 1000 
          AND pcs.total_wickets > 50
          AND p.playing_role = 'All-rounder'
        ORDER BY pcs.total_runs DESC;
        """
    
    @staticmethod
    def query_10_recent_completed_matches():
        """Q10: Last 20 completed matches with details"""
        return """
        SELECT 
            m.match_description AS 'Match',
            t1.team_name AS 'Team 1',
            t2.team_name AS 'Team 2',
            tw.team_name AS 'Winner',
            m.victory_margin AS 'Victory Margin',
            m.victory_type AS 'Victory Type',
            v.venue_name AS 'Venue'
        FROM matches m
        LEFT JOIN teams t1 ON m.team1_id = t1.team_id
        LEFT JOIN teams t2 ON m.team2_id = t2.team_id
        LEFT JOIN teams tw ON m.winner_id = tw.team_id
        LEFT JOIN venues v ON m.venue_id = v.venue_id
        WHERE m.match_status = 'Completed' AND m.winner_id IS NOT NULL
        ORDER BY m.match_date DESC
        LIMIT 20;
        """
    
    @staticmethod
    def query_11_player_format_comparison():
        """Q11: Player performance across different formats"""
        return """
        SELECT 
            p.player_name AS 'Player Name',
            MAX(CASE WHEN pcs.match_format = 'Test' THEN pcs.total_runs END) AS 'Test Runs',
            MAX(CASE WHEN pcs.match_format = 'ODI' THEN pcs.total_runs END) AS 'ODI Runs',
            MAX(CASE WHEN pcs.match_format = 'T20I' THEN pcs.total_runs END) AS 'T20I Runs',
            ROUND(AVG(pcs.batting_average), 2) AS 'Overall Average'
        FROM players p
        JOIN player_career_stats pcs ON p.player_id = pcs.player_id
        GROUP BY p.player_id, p.player_name
        HAVING COUNT(DISTINCT pcs.match_format) >= 2
        ORDER BY AVG(pcs.batting_average) DESC;
        """
    
    @staticmethod
    def query_12_home_away_performance():
        """Q12: Team performance - Home vs Away"""
        return """
        SELECT 
            t.team_name AS 'Team',
            SUM(CASE WHEN v.country = t.country AND m.winner_id = t.team_id THEN 1 ELSE 0 END) AS 'Home Wins',
            SUM(CASE WHEN v.country != t.country AND m.winner_id = t.team_id THEN 1 ELSE 0 END) AS 'Away Wins',
            COUNT(m.match_id) AS 'Total Matches'
        FROM teams t
        JOIN matches m ON (t.team_id = m.team1_id OR t.team_id = m.team2_id)
        LEFT JOIN venues v ON m.venue_id = v.venue_id
        WHERE m.match_status = 'Completed'
        GROUP BY t.team_id, t.team_name, t.country
        ORDER BY (SUM(CASE WHEN v.country = t.country AND m.winner_id = t.team_id THEN 1 ELSE 0 END) + 
                  SUM(CASE WHEN v.country != t.country AND m.winner_id = t.team_id THEN 1 ELSE 0 END)) DESC;
        """
    
    @staticmethod
    def query_13_batting_partnerships():
        """Q13: Batting partnerships with 100+ combined runs"""
        return """
        SELECT 
            p1.player_name AS 'Batsman 1',
            p2.player_name AS 'Batsman 2',
            (bs1.runs_scored + bs2.runs_scored) AS 'Partnership Runs',
            bs1.innings_number AS 'Innings'
        FROM batting_stats bs1
        JOIN batting_stats bs2 ON bs1.match_id = bs2.match_id 
            AND bs1.innings_number = bs2.innings_number
            AND bs1.stat_id < bs2.stat_id
        JOIN players p1 ON bs1.player_id = p1.player_id
        JOIN players p2 ON bs2.player_id = p2.player_id
        WHERE (bs1.runs_scored + bs2.runs_scored) >= 100
        ORDER BY (bs1.runs_scored + bs2.runs_scored) DESC;
        """
    
    @staticmethod
    def query_14_bowling_venue_analysis():
        """Q14: Bowling performance at different venues"""
        return """
        SELECT 
            p.player_name AS 'Bowler',
            v.venue_name AS 'Venue',
            ROUND(AVG(bw.economy_rate), 2) AS 'Avg Economy',
            SUM(bw.wickets_taken) AS 'Total Wickets',
            COUNT(DISTINCT bw.match_id) AS 'Matches'
        FROM bowling_stats bw
        JOIN players p ON bw.player_id = p.player_id
        JOIN matches m ON bw.match_id = m.match_id
        JOIN venues v ON m.venue_id = v.venue_id
        WHERE bw.overs_bowled >= 4
        GROUP BY p.player_id, p.player_name, v.venue_id, v.venue_name
        HAVING COUNT(DISTINCT bw.match_id) >= 3
        ORDER BY AVG(bw.economy_rate) ASC;
        """
    
    @staticmethod
    def query_15_close_match_performers():
        """Q15: Players performing well in close matches"""
        return """
        SELECT 
            p.player_name AS 'Player',
            ROUND(AVG(bs.runs_scored), 2) AS 'Avg Runs in Close Matches',
            COUNT(DISTINCT m.match_id) AS 'Close Matches Played',
            SUM(CASE WHEN m.winner_id = t.team_id THEN 1 ELSE 0 END) AS 'Close Matches Won'
        FROM batting_stats bs
        JOIN players p ON bs.player_id = p.player_id
        JOIN matches m ON bs.match_id = m.match_id
        JOIN teams t ON p.team_id = t.team_id
        WHERE (m.victory_type = 'runs' AND m.victory_margin < 50)
           OR (m.victory_type = 'wickets' AND m.victory_margin < 5)
        GROUP BY p.player_id, p.player_name, t.team_id
        HAVING COUNT(DISTINCT m.match_id) >= 5
        ORDER BY AVG(bs.runs_scored) DESC;
        """
    
    @staticmethod
    def query_16_performance_trends():
        """Q16: Player batting performance trends over years"""
        return """
        SELECT 
            p.player_name AS 'Player',
            YEAR(m.match_date) AS 'Year',
            ROUND(AVG(bs.runs_scored), 2) AS 'Avg Runs per Match',
            ROUND(AVG(bs.strike_rate), 2) AS 'Avg Strike Rate'
        FROM batting_stats bs
        JOIN players p ON bs.player_id = p.player_id
        JOIN matches m ON bs.match_id = m.match_id
        WHERE YEAR(m.match_date) >= 2020
        GROUP BY p.player_id, p.player_name, YEAR(m.match_date)
        HAVING COUNT(DISTINCT m.match_id) >= 5
        ORDER BY p.player_name, YEAR(m.match_date);
        """
    
    # ==================== ADVANCED LEVEL (17-25) ====================
    
    @staticmethod
    def query_17_toss_advantage():
        """Q17: Toss advantage analysis"""
        return """
        SELECT 
            m.toss_decision AS 'Toss Decision',
            COUNT(*) AS 'Total Matches',
            SUM(CASE WHEN m.toss_winner_id = m.winner_id THEN 1 ELSE 0 END) AS 'Toss Winner Won',
            ROUND(100.0 * SUM(CASE WHEN m.toss_winner_id = m.winner_id THEN 1 ELSE 0 END) / COUNT(*), 2) AS 'Win Percentage'
        FROM matches m
        WHERE m.toss_winner_id IS NOT NULL 
          AND m.winner_id IS NOT NULL
          AND m.toss_decision IS NOT NULL
        GROUP BY m.toss_decision;
        """
    
    @staticmethod
    def query_18_economical_bowlers():
        """Q18: Most economical bowlers in limited-overs"""
        return """
        SELECT 
            p.player_name AS 'Bowler',
            ROUND(AVG(bw.economy_rate), 2) AS 'Overall Economy Rate',
            SUM(bw.wickets_taken) AS 'Total Wickets',
            COUNT(DISTINCT bw.match_id) AS 'Matches Bowled'
        FROM bowling_stats bw
        JOIN players p ON bw.player_id = p.player_id
        JOIN matches m ON bw.match_id = m.match_id
        WHERE m.match_format IN ('ODI', 'T20I')
          AND bw.overs_bowled >= 2
        GROUP BY p.player_id, p.player_name
        HAVING COUNT(DISTINCT bw.match_id) >= 10
           AND AVG(bw.overs_bowled) >= 2
        ORDER BY AVG(bw.economy_rate) ASC
        LIMIT 20;
        """
    
    @staticmethod
    def query_19_consistent_batsmen():
        """Q19: Most consistent batsmen (low standard deviation)"""
        return """
        SELECT 
            p.player_name AS 'Player',
            ROUND(AVG(bs.runs_scored), 2) AS 'Average Runs',
            ROUND(STDDEV(bs.runs_scored), 2) AS 'Standard Deviation',
            COUNT(bs.stat_id) AS 'Innings'
        FROM batting_stats bs
        JOIN players p ON bs.player_id = p.player_id
        JOIN matches m ON bs.match_id = m.match_id
        WHERE bs.balls_faced >= 10
          AND YEAR(m.match_date) >= 2022
        GROUP BY p.player_id, p.player_name
        HAVING COUNT(bs.stat_id) >= 15
        ORDER BY STDDEV(bs.runs_scored) ASC
        LIMIT 20;
        """
    
    @staticmethod
    def query_20_format_wise_experience():
        """Q20: Player experience across formats"""
        return """
        SELECT 
            p.player_name AS 'Player',
            SUM(CASE WHEN pcs.match_format = 'Test' THEN pcs.total_matches ELSE 0 END) AS 'Test Matches',
            SUM(CASE WHEN pcs.match_format = 'ODI' THEN pcs.total_matches ELSE 0 END) AS 'ODI Matches',
            SUM(CASE WHEN pcs.match_format = 'T20I' THEN pcs.total_matches ELSE 0 END) AS 'T20I Matches',
            ROUND(AVG(CASE WHEN pcs.match_format = 'Test' THEN pcs.batting_average END), 2) AS 'Test Avg',
            ROUND(AVG(CASE WHEN pcs.match_format = 'ODI' THEN pcs.batting_average END), 2) AS 'ODI Avg',
            ROUND(AVG(CASE WHEN pcs.match_format = 'T20I' THEN pcs.batting_average END), 2) AS 'T20I Avg'
        FROM players p
        JOIN player_career_stats pcs ON p.player_id = pcs.player_id
        GROUP BY p.player_id, p.player_name
        HAVING SUM(pcs.total_matches) >= 20
        ORDER BY SUM(pcs.total_matches) DESC;
        """
    
    @staticmethod
    def query_21_performance_ranking():
        """Q21: Comprehensive performance ranking"""
        return """
        SELECT 
            p.player_name AS 'Player',
            pcs.match_format AS 'Format',
            ROUND(
                (pcs.total_runs * 0.01) + 
                (COALESCE(pcs.batting_average, 0) * 0.5) + 
                (COALESCE(pcs.total_runs / NULLIF(pcs.total_innings, 0) * 100 / NULLIF(pcs.total_innings, 0), 0) * 0.3),
                2
            ) AS 'Batting Points',
            ROUND(
                (pcs.total_wickets * 2) + 
                ((50 - COALESCE(pcs.bowling_average, 50)) * 0.5),
                2
            ) AS 'Bowling Points',
            ROUND(
                (pcs.total_runs * 0.01) + 
                (COALESCE(pcs.batting_average, 0) * 0.5) + 
                (pcs.total_wickets * 2) + 
                ((50 - COALESCE(pcs.bowling_average, 50)) * 0.5),
                2
            ) AS 'Total Points'
        FROM player_career_stats pcs
        JOIN players p ON pcs.player_id = p.player_id
        WHERE pcs.total_matches >= 10
        ORDER BY pcs.match_format, 
                 (pcs.total_runs * 0.01 + COALESCE(pcs.batting_average, 0) * 0.5 + 
                  pcs.total_wickets * 2 + (50 - COALESCE(pcs.bowling_average, 50)) * 0.5) DESC;
        """
    
    @staticmethod
    def query_22_head_to_head():
        """Q22: Head-to-head team analysis"""
        return """
        SELECT 
            t1.team_name AS 'Team 1',
            t2.team_name AS 'Team 2',
            COUNT(*) AS 'Total Matches',
            SUM(CASE WHEN m.winner_id = t1.team_id THEN 1 ELSE 0 END) AS 'Team 1 Wins',
            SUM(CASE WHEN m.winner_id = t2.team_id THEN 1 ELSE 0 END) AS 'Team 2 Wins',
            ROUND(AVG(CASE WHEN m.winner_id = t1.team_id THEN m.victory_margin END), 2) AS 'Team 1 Avg Margin',
            ROUND(AVG(CASE WHEN m.winner_id = t2.team_id THEN m.victory_margin END), 2) AS 'Team 2 Avg Margin'
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        WHERE m.match_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
          AND m.winner_id IS NOT NULL
        GROUP BY t1.team_id, t1.team_name, t2.team_id, t2.team_name
        HAVING COUNT(*) >= 5
        ORDER BY COUNT(*) DESC;
        """
    
    @staticmethod
    def query_23_recent_form():
        """Q23: Recent player form analysis"""
        return """
        WITH RecentStats AS (
            SELECT 
                bs.player_id,
                bs.runs_scored,
                bs.strike_rate,
                m.match_date,
                ROW_NUMBER() OVER (PARTITION BY bs.player_id ORDER BY m.match_date DESC) AS rn
            FROM batting_stats bs
            JOIN matches m ON bs.match_id = m.match_id
            WHERE m.match_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        )
        SELECT 
            p.player_name AS 'Player',
            ROUND(AVG(CASE WHEN rs.rn <= 5 THEN rs.runs_scored END), 2) AS 'Last 5 Avg',
            ROUND(AVG(CASE WHEN rs.rn <= 10 THEN rs.runs_scored END), 2) AS 'Last 10 Avg',
            ROUND(AVG(CASE WHEN rs.rn <= 10 THEN rs.strike_rate END), 2) AS 'Recent SR',
            SUM(CASE WHEN rs.rn <= 10 AND rs.runs_scored >= 50 THEN 1 ELSE 0 END) AS '50+ Scores',
            CASE 
                WHEN AVG(CASE WHEN rs.rn <= 5 THEN rs.runs_scored END) >= 50 THEN 'Excellent Form'
                WHEN AVG(CASE WHEN rs.rn <= 5 THEN rs.runs_scored END) >= 35 THEN 'Good Form'
                WHEN AVG(CASE WHEN rs.rn <= 5 THEN rs.runs_scored END) >= 20 THEN 'Average Form'
                ELSE 'Poor Form'
            END AS 'Form Status'
        FROM RecentStats rs
        JOIN players p ON rs.player_id = p.player_id
        GROUP BY p.player_id, p.player_name
        HAVING COUNT(*) >= 10
        ORDER BY AVG(CASE WHEN rs.rn <= 5 THEN rs.runs_scored END) DESC;
        """
    
    @staticmethod
    def query_24_best_partnerships():
        """Q24: Best batting partnerships analysis"""
        return """
        WITH Partnerships AS (
            SELECT 
                bs1.player_id AS player1_id,
                bs2.player_id AS player2_id,
                bs1.match_id,
                (bs1.runs_scored + bs2.runs_scored) AS partnership_runs
            FROM batting_stats bs1
            JOIN batting_stats bs2 ON bs1.match_id = bs2.match_id 
                AND bs1.innings_number = bs2.innings_number
                AND bs1.player_id < bs2.player_id
        )
        SELECT 
            p1.player_name AS 'Player 1',
            p2.player_name AS 'Player 2',
            ROUND(AVG(pt.partnership_runs), 2) AS 'Avg Partnership',
            COUNT(*) AS 'Total Partnerships',
            SUM(CASE WHEN pt.partnership_runs >= 50 THEN 1 ELSE 0 END) AS '50+ Partnerships',
            MAX(pt.partnership_runs) AS 'Highest Partnership',
            ROUND(100.0 * SUM(CASE WHEN pt.partnership_runs >= 50 THEN 1 ELSE 0 END) / COUNT(*), 2) AS 'Success Rate %'
        FROM Partnerships pt
        JOIN players p1 ON pt.player1_id = p1.player_id
        JOIN players p2 ON pt.player2_id = p2.player_id
        GROUP BY p1.player_id, p1.player_name, p2.player_id, p2.player_name
        HAVING COUNT(*) >= 5
        ORDER BY AVG(pt.partnership_runs) DESC
        LIMIT 20;
        """
    
    @staticmethod
    def query_25_career_trajectory():
        """Q25: Time-series career trajectory analysis"""
        return """
        WITH QuarterlyStats AS (
            SELECT 
                p.player_id,
                p.player_name,
                YEAR(m.match_date) AS year,
                QUARTER(m.match_date) AS quarter,
                ROUND(AVG(bs.runs_scored), 2) AS avg_runs,
                ROUND(AVG(bs.strike_rate), 2) AS avg_sr,
                COUNT(DISTINCT m.match_id) AS matches
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
            JOIN matches m ON bs.match_id = m.match_id
            WHERE m.match_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
            GROUP BY p.player_id, p.player_name, YEAR(m.match_date), QUARTER(m.match_date)
            HAVING COUNT(DISTINCT m.match_id) >= 3
        ),
        TrendAnalysis AS (
            SELECT 
                player_id,
                player_name,
                COUNT(DISTINCT CONCAT(year, '-', quarter)) AS total_quarters,
                AVG(avg_runs) AS overall_avg,
                STDDEV(avg_runs) AS runs_volatility
            FROM QuarterlyStats
            GROUP BY player_id, player_name
        )
        SELECT 
            ta.player_name AS 'Player',
            ta.total_quarters AS 'Quarters Analyzed',
            ROUND(ta.overall_avg, 2) AS 'Overall Average',
            ROUND(ta.runs_volatility, 2) AS 'Performance Volatility',
            CASE 
                WHEN ta.runs_volatility < 10 THEN 'Career Stable'
                WHEN ta.overall_avg > 40 AND ta.runs_volatility < 20 THEN 'Career Ascending'
                WHEN ta.overall_avg < 25 THEN 'Career Declining'
                ELSE 'Career Stable'
            END AS 'Career Phase'
        FROM TrendAnalysis ta
        WHERE ta.total_quarters >= 6
        ORDER BY ta.overall_avg DESC;
        """
    
    @staticmethod
    def get_all_queries():
        """Return dictionary of all queries"""
        return {
            # Beginner
            "Q1: Indian Players": SQLQueries.query_1_indian_players(),
            "Q2: Recent Matches": SQLQueries.query_2_recent_matches(),
            "Q3: Top ODI Scorers": SQLQueries.query_3_top_odi_scorers(),
            "Q4: Large Venues": SQLQueries.query_4_large_venues(),
            "Q5: Team Wins": SQLQueries.query_5_team_wins(),
            "Q6: Players by Role": SQLQueries.query_6_players_by_role(),
            "Q7: Highest Scores by Format": SQLQueries.query_7_highest_scores_by_format(),
            "Q8: Series in 2024": SQLQueries.query_8_series_2024(),
            
            # Intermediate
            "Q9: All-rounders Performance": SQLQueries.query_9_allrounders(),
            "Q10: Recent Completed Matches": SQLQueries.query_10_recent_completed_matches(),
            "Q11: Format Comparison": SQLQueries.query_11_player_format_comparison(),
            "Q12: Home vs Away": SQLQueries.query_12_home_away_performance(),
            "Q13: Batting Partnerships": SQLQueries.query_13_batting_partnerships(),
            "Q14: Bowling Venue Analysis": SQLQueries.query_14_bowling_venue_analysis(),
            "Q15: Close Match Performers": SQLQueries.query_15_close_match_performers(),
            "Q16: Performance Trends": SQLQueries.query_16_performance_trends(),
            
            # Advanced
            "Q17: Toss Advantage": SQLQueries.query_17_toss_advantage(),
            "Q18: Economical Bowlers": SQLQueries.query_18_economical_bowlers(),
            "Q19: Consistent Batsmen": SQLQueries.query_19_consistent_batsmen(),
            "Q20: Format-wise Experience": SQLQueries.query_20_format_wise_experience(),
            "Q21: Performance Ranking": SQLQueries.query_21_performance_ranking(),
            "Q22: Head-to-Head Analysis": SQLQueries.query_22_head_to_head(),
            "Q23: Recent Form": SQLQueries.query_23_recent_form(),
            "Q24: Best Partnerships": SQLQueries.query_24_best_partnerships(),
            "Q25: Career Trajectory": SQLQueries.query_25_career_trajectory(),
        }
