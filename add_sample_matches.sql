-- Add Sample Matches Data for Cricbuzz LiveStats
-- Run this in MySQL to populate matches and related data

USE cricbuzz_db;

-- Insert Series
INSERT INTO series (series_name, host_country, match_type, start_date, end_date, total_matches) VALUES
('ICC World Cup 2023', 'India', 'ODI', '2023-10-05', '2023-11-19', 48),
('India vs Australia Test Series 2024', 'India', 'Test', '2024-02-09', '2024-03-09', 4),
('T20 World Cup 2024', 'West Indies', 'T20I', '2024-06-01', '2024-06-29', 55),
('Asia Cup 2023', 'Pakistan', 'ODI', '2023-08-30', '2023-09-17', 13);

-- Insert Matches (Recent dates for testing)
INSERT INTO matches (series_id, match_description, match_format, team1_id, team2_id, venue_id, match_date, toss_winner_id, toss_decision, winner_id, victory_margin, victory_type, match_status) VALUES
-- Recent matches (last 30 days)
(1, 'Final', 'ODI', 1, 2, 1, DATE_SUB(CURDATE(), INTERVAL 5 DAY), 1, 'bat', 1, 6, 'wickets', 'Completed'),
(1, 'Semi Final 1', 'ODI', 1, 6, 1, DATE_SUB(CURDATE(), INTERVAL 8 DAY), 6, 'bowl', 1, 70, 'runs', 'Completed'),
(1, 'Semi Final 2', 'ODI', 2, 5, 2, DATE_SUB(CURDATE(), INTERVAL 8 DAY), 2, 'bat', 2, 3, 'wickets', 'Completed'),
(3, 'Group Stage', 'T20I', 1, 4, 1, DATE_SUB(CURDATE(), INTERVAL 12 DAY), 4, 'bowl', 1, 8, 'runs', 'Completed'),
(3, 'Group Stage', 'T20I', 2, 3, 2, DATE_SUB(CURDATE(), INTERVAL 15 DAY), 3, 'bat', 2, 5, 'wickets', 'Completed'),
(4, 'Final', 'ODI', 1, 8, 1, DATE_SUB(CURDATE(), INTERVAL 20 DAY), 1, 'bat', 1, 10, 'wickets', 'Completed'),
(2, '1st Test', 'Test', 1, 2, 4, DATE_SUB(CURDATE(), INTERVAL 25 DAY), 2, 'bowl', 1, 280, 'runs', 'Completed'),

-- Older matches (for historical data)
(1, 'Quarter Final 1', 'ODI', 1, 5, 1, '2023-11-11', 1, 'bat', 1, 87, 'runs', 'Completed'),
(1, 'Quarter Final 2', 'ODI', 2, 4, 2, '2023-11-11', 2, 'bowl', 2, 4, 'wickets', 'Completed'),
(1, 'Group Stage', 'ODI', 1, 4, 1, '2023-10-14', 1, 'bat', 1, 8, 'wickets', 'Completed'),
(1, 'Group Stage', 'ODI', 2, 3, 2, '2023-10-08', 3, 'bowl', 2, 5, 'wickets', 'Completed'),
(2, '2nd Test', 'Test', 1, 2, 1, '2024-02-17', 1, 'bat', 2, 6, 'wickets', 'Completed'),
(2, '3rd Test', 'Test', 1, 2, 4, '2024-03-01', 2, 'bowl', 1, 434, 'runs', 'Completed'),
(4, 'Group Stage', 'ODI', 1, 4, 1, '2023-09-02', 4, 'bat', 1, 228, 'runs', 'Completed'),
(4, 'Group Stage', 'ODI', 1, 8, 1, '2023-09-12', 1, 'bat', 1, 41, 'runs', 'Completed');

-- Insert Batting Stats (sample performances)
INSERT INTO batting_stats (player_id, match_id, innings_number, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
-- Match 1 (Final - India won)
(1, 1, 1, 82, 65, 8, 2, 126.15, TRUE, 'caught'),
(2, 1, 1, 137, 126, 15, 4, 108.73, FALSE, NULL),
(5, 1, 2, 66, 58, 7, 1, 113.79, TRUE, 'bowled'),

-- Match 2 (Semi Final 1)
(1, 2, 1, 117, 113, 9, 4, 103.54, FALSE, NULL),
(2, 2, 1, 45, 38, 5, 1, 118.42, TRUE, 'lbw'),

-- Match 3 (Semi Final 2)
(5, 3, 1, 46, 43, 4, 0, 106.98, TRUE, 'caught'),
(6, 3, 1, 34, 28, 3, 2, 121.43, TRUE, 'run out'),

-- Match 4 (T20 Group Stage)
(1, 4, 1, 82, 53, 6, 4, 154.72, FALSE, NULL),
(2, 4, 1, 56, 35, 4, 3, 160.00, TRUE, 'caught'),

-- Match 5 (T20 Group Stage)
(5, 5, 1, 61, 44, 5, 2, 138.64, TRUE, 'bowled'),
(7, 5, 2, 87, 47, 8, 4, 185.11, FALSE, NULL);

-- Insert Bowling Stats (sample performances)
INSERT INTO bowling_stats (player_id, match_id, innings_number, overs_bowled, runs_conceded, wickets_taken, maidens, economy_rate) VALUES
-- Match 1 (Final)
(3, 1, 2, 10.0, 43, 3, 1, 4.30),
(4, 1, 2, 10.0, 48, 2, 0, 4.80),
(6, 1, 1, 10.0, 67, 2, 0, 6.70),

-- Match 2 (Semi Final 1)
(3, 2, 2, 10.0, 39, 2, 2, 3.90),
(4, 2, 2, 10.0, 52, 1, 0, 5.20),

-- Match 3 (Semi Final 2)
(6, 3, 1, 10.0, 45, 3, 1, 4.50),

-- Match 4 (T20)
(3, 4, 2, 4.0, 28, 2, 0, 7.00),
(4, 4, 2, 4.0, 35, 1, 0, 8.75),

-- Match 5 (T20)
(6, 5, 1, 4.0, 42, 2, 0, 10.50),
(8, 5, 2, 4.0, 38, 3, 0, 9.50);

-- Verify the data
SELECT 'Teams' as TableName, COUNT(*) as Count FROM teams
UNION ALL
SELECT 'Venues', COUNT(*) FROM venues
UNION ALL
SELECT 'Players', COUNT(*) FROM players
UNION ALL
SELECT 'Series', COUNT(*) FROM series
UNION ALL
SELECT 'Matches', COUNT(*) FROM matches
UNION ALL
SELECT 'Batting Stats', COUNT(*) FROM batting_stats
UNION ALL
SELECT 'Bowling Stats', COUNT(*) FROM bowling_stats
UNION ALL
SELECT 'Career Stats', COUNT(*) FROM player_career_stats;

-- Show recent matches
SELECT 
    m.match_description AS 'Match',
    t1.team_name AS 'Team 1',
    t2.team_name AS 'Team 2',
    tw.team_name AS 'Winner',
    m.match_date AS 'Date'
FROM matches m
LEFT JOIN teams t1 ON m.team1_id = t1.team_id
LEFT JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN teams tw ON m.winner_id = tw.team_id
WHERE m.match_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY m.match_date DESC;
