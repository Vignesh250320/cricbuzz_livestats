-- Additional Sample Data for All Queries to Work
-- This adds more matches, batting stats, and bowling stats

USE cricbuzz_db;

-- Update existing players to have all-rounder stats
UPDATE player_career_stats 
SET total_wickets = 75, bowling_average = 32.5, best_bowling = '5/42'
WHERE player_id = 4 AND match_format = 'ODI';  -- Ravindra Jadeja

UPDATE player_career_stats 
SET total_runs = 1500, batting_average = 28.5, highest_score = 87, half_centuries = 8
WHERE player_id = 4 AND match_format = 'ODI';  -- Ravindra Jadeja

-- Add more all-rounder stats
INSERT INTO player_career_stats (player_id, match_format, total_matches, total_innings, total_runs, batting_average, highest_score, centuries, half_centuries, total_wickets, bowling_average, best_bowling) VALUES
(8, 'ODI', 120, 115, 2800, 32.5, 135, 3, 18, 85, 35.2, '4/38'),  -- Ben Stokes
(8, 'Test', 95, 165, 5500, 38.8, 258, 12, 28, 180, 31.8, '6/36');  -- Ben Stokes

-- Insert more recent matches (for Q15 - close matches and Q16 - trends)
INSERT INTO matches (series_id, match_description, match_format, team1_id, team2_id, venue_id, match_date, toss_winner_id, toss_decision, winner_id, victory_margin, victory_type, match_status) VALUES
-- Close matches (margin < 50 runs or < 5 wickets)
(1, 'Group Match 1', 'ODI', 1, 2, 1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), 1, 'bat', 1, 15, 'runs', 'Completed'),
(1, 'Group Match 2', 'ODI', 1, 3, 2, DATE_SUB(CURDATE(), INTERVAL 11 DAY), 3, 'bowl', 1, 2, 'wickets', 'Completed'),
(1, 'Group Match 3', 'ODI', 2, 4, 1, DATE_SUB(CURDATE(), INTERVAL 13 DAY), 2, 'bat', 2, 28, 'runs', 'Completed'),
(1, 'Group Match 4', 'ODI', 1, 5, 2, DATE_SUB(CURDATE(), INTERVAL 14 DAY), 5, 'bowl', 1, 3, 'wickets', 'Completed'),
(1, 'Group Match 5', 'ODI', 3, 6, 1, DATE_SUB(CURDATE(), INTERVAL 16 DAY), 3, 'bat', 3, 42, 'runs', 'Completed'),
(3, 'T20 Match 1', 'T20I', 1, 2, 1, DATE_SUB(CURDATE(), INTERVAL 18 DAY), 2, 'bowl', 1, 4, 'wickets', 'Completed'),
(3, 'T20 Match 2', 'T20I', 1, 3, 2, DATE_SUB(CURDATE(), INTERVAL 19 DAY), 1, 'bat', 1, 18, 'runs', 'Completed'),

-- Matches from 2020-2024 for trends (Q16)
(2, 'Test Match 2020', 'Test', 1, 2, 4, '2020-01-15', 1, 'bat', 1, 150, 'runs', 'Completed'),
(2, 'Test Match 2020-2', 'Test', 1, 2, 1, '2020-02-20', 2, 'bowl', 2, 7, 'wickets', 'Completed'),
(2, 'Test Match 2021', 'Test', 1, 2, 4, '2021-03-10', 1, 'bat', 1, 200, 'runs', 'Completed'),
(2, 'Test Match 2021-2', 'Test', 1, 2, 1, '2021-06-15', 2, 'bowl', 1, 4, 'wickets', 'Completed'),
(2, 'Test Match 2022', 'Test', 1, 2, 4, '2022-02-25', 1, 'bat', 2, 180, 'runs', 'Completed'),
(2, 'Test Match 2022-2', 'Test', 1, 2, 1, '2022-08-10', 2, 'bowl', 1, 5, 'wickets', 'Completed'),
(2, 'Test Match 2023', 'Test', 1, 2, 4, '2023-01-20', 1, 'bat', 1, 250, 'runs', 'Completed'),
(2, 'Test Match 2023-2', 'Test', 1, 2, 1, '2023-07-05', 2, 'bowl', 2, 3, 'wickets', 'Completed'),
(2, 'Test Match 2024', 'Test', 1, 2, 4, '2024-01-10', 1, 'bat', 1, 320, 'runs', 'Completed'),
(2, 'Test Match 2024-2', 'Test', 1, 2, 1, '2024-05-18', 2, 'bowl', 1, 6, 'wickets', 'Completed');

-- Get the match IDs for the newly inserted matches
SET @match_close_1 = (SELECT match_id FROM matches WHERE match_description = 'Group Match 1' LIMIT 1);
SET @match_close_2 = (SELECT match_id FROM matches WHERE match_description = 'Group Match 2' LIMIT 1);
SET @match_close_3 = (SELECT match_id FROM matches WHERE match_description = 'Group Match 3' LIMIT 1);
SET @match_close_4 = (SELECT match_id FROM matches WHERE match_description = 'Group Match 4' LIMIT 1);
SET @match_close_5 = (SELECT match_id FROM matches WHERE match_description = 'Group Match 5' LIMIT 1);
SET @match_close_6 = (SELECT match_id FROM matches WHERE match_description = 'T20 Match 1' LIMIT 1);
SET @match_close_7 = (SELECT match_id FROM matches WHERE match_description = 'T20 Match 2' LIMIT 1);

SET @match_2020_1 = (SELECT match_id FROM matches WHERE match_description = 'Test Match 2020' LIMIT 1);
SET @match_2020_2 = (SELECT match_id FROM matches WHERE match_description = 'Test Match 2020-2' LIMIT 1);
SET @match_2021_1 = (SELECT match_id FROM matches WHERE match_description = 'Test Match 2021' LIMIT 1);
SET @match_2021_2 = (SELECT match_id FROM matches WHERE match_description = 'Test Match 2021-2' LIMIT 1);
SET @match_2022_1 = (SELECT match_id FROM matches WHERE match_description = 'Test Match 2022' LIMIT 1);
SET @match_2022_2 = (SELECT match_id FROM matches WHERE match_description = 'Test Match 2022-2' LIMIT 1);
SET @match_2023_1 = (SELECT match_id FROM matches WHERE match_description = 'Test Match 2023' LIMIT 1);
SET @match_2023_2 = (SELECT match_id FROM matches WHERE match_description = 'Test Match 2023-2' LIMIT 1);
SET @match_2024_1 = (SELECT match_id FROM matches WHERE match_description = 'Test Match 2024' LIMIT 1);
SET @match_2024_2 = (SELECT match_id FROM matches WHERE match_description = 'Test Match 2024-2' LIMIT 1);

-- Insert batting stats for close matches (Q15)
INSERT INTO batting_stats (player_id, match_id, innings_number, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
-- Match Close 1 (India won by 15 runs)
(1, @match_close_1, 1, 78, 82, 8, 2, 95.12, TRUE, 'caught'),
(2, @match_close_1, 1, 92, 105, 10, 3, 87.62, FALSE, NULL),
(5, @match_close_1, 2, 65, 78, 7, 1, 83.33, TRUE, 'bowled'),

-- Match Close 2 (India won by 2 wickets - very close!)
(1, @match_close_2, 1, 95, 98, 9, 3, 96.94, FALSE, NULL),
(2, @match_close_2, 1, 52, 61, 5, 1, 85.25, TRUE, 'lbw'),
(7, @match_close_2, 2, 88, 92, 8, 2, 95.65, TRUE, 'caught'),

-- Match Close 3 (Australia won by 28 runs)
(5, @match_close_3, 1, 72, 68, 7, 2, 105.88, TRUE, 'run out'),
(6, @match_close_3, 1, 45, 52, 4, 1, 86.54, TRUE, 'bowled'),

-- Match Close 4 (India won by 3 wickets)
(1, @match_close_4, 1, 102, 115, 11, 2, 88.70, FALSE, NULL),
(2, @match_close_4, 1, 38, 45, 3, 1, 84.44, TRUE, 'caught'),

-- Match Close 5 (England won by 42 runs)
(7, @match_close_5, 1, 85, 79, 9, 3, 107.59, FALSE, NULL),
(8, @match_close_5, 1, 67, 58, 6, 2, 115.52, TRUE, 'bowled'),

-- Match Close 6 (India won by 4 wickets - T20)
(1, @match_close_6, 1, 68, 42, 6, 3, 161.90, FALSE, NULL),
(2, @match_close_6, 1, 45, 28, 4, 2, 160.71, TRUE, 'caught'),

-- Match Close 7 (India won by 18 runs - T20)
(1, @match_close_7, 1, 82, 51, 7, 4, 160.78, FALSE, NULL),
(2, @match_close_7, 1, 56, 35, 5, 3, 160.00, TRUE, 'run out');

-- Insert batting stats for trend analysis (Q16) - 2020-2024
INSERT INTO batting_stats (player_id, match_id, innings_number, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
-- 2020 matches
(1, @match_2020_1, 1, 45, 98, 5, 0, 45.92, TRUE, 'caught'),
(1, @match_2020_2, 1, 38, 85, 4, 0, 44.71, TRUE, 'lbw'),
(2, @match_2020_1, 1, 52, 105, 6, 1, 49.52, TRUE, 'bowled'),
(2, @match_2020_2, 1, 48, 92, 5, 0, 52.17, TRUE, 'caught'),

-- 2021 matches
(1, @match_2021_1, 1, 68, 125, 8, 1, 54.40, TRUE, 'caught'),
(1, @match_2021_2, 1, 72, 118, 9, 1, 61.02, FALSE, NULL),
(2, @match_2021_1, 1, 85, 142, 10, 2, 59.86, TRUE, 'lbw'),
(2, @match_2021_2, 1, 62, 108, 7, 1, 57.41, TRUE, 'caught'),

-- 2022 matches
(1, @match_2022_1, 1, 55, 102, 6, 1, 53.92, TRUE, 'bowled'),
(1, @match_2022_2, 1, 48, 95, 5, 0, 50.53, TRUE, 'caught'),
(2, @match_2022_1, 1, 78, 135, 9, 2, 57.78, FALSE, NULL),
(2, @match_2022_2, 1, 65, 118, 7, 1, 55.08, TRUE, 'lbw'),

-- 2023 matches
(1, @match_2023_1, 1, 92, 158, 11, 2, 58.23, TRUE, 'caught'),
(1, @match_2023_2, 1, 78, 142, 9, 1, 54.93, TRUE, 'run out'),
(2, @match_2023_1, 1, 105, 175, 12, 3, 60.00, FALSE, NULL),
(2, @match_2023_2, 1, 88, 152, 10, 2, 57.89, TRUE, 'caught'),

-- 2024 matches
(1, @match_2024_1, 1, 112, 185, 13, 3, 60.54, FALSE, NULL),
(1, @match_2024_2, 1, 95, 168, 11, 2, 56.55, TRUE, 'caught'),
(2, @match_2024_1, 1, 125, 198, 15, 4, 63.13, FALSE, NULL),
(2, @match_2024_2, 1, 98, 172, 12, 2, 56.98, TRUE, 'lbw');

-- Insert bowling stats for close matches
INSERT INTO bowling_stats (player_id, match_id, innings_number, overs_bowled, runs_conceded, wickets_taken, maidens, economy_rate) VALUES
(3, @match_close_1, 2, 10.0, 48, 3, 1, 4.80),
(4, @match_close_1, 2, 10.0, 52, 2, 0, 5.20),
(3, @match_close_2, 2, 10.0, 45, 4, 2, 4.50),
(4, @match_close_2, 2, 10.0, 38, 3, 1, 3.80),
(6, @match_close_3, 1, 10.0, 55, 2, 0, 5.50),
(3, @match_close_4, 2, 10.0, 42, 3, 1, 4.20),
(4, @match_close_4, 2, 10.0, 47, 2, 0, 4.70),
(3, @match_close_6, 2, 4.0, 32, 2, 0, 8.00),
(4, @match_close_6, 2, 4.0, 28, 3, 0, 7.00),
(3, @match_close_7, 2, 4.0, 35, 2, 0, 8.75),
(4, @match_close_7, 2, 4.0, 30, 2, 0, 7.50);

-- Verify the data
SELECT '=== DATA SUMMARY ===' as Info;

SELECT 'Total Teams' as Item, COUNT(*) as Count FROM teams
UNION ALL
SELECT 'Total Players', COUNT(*) FROM players
UNION ALL
SELECT 'Total Venues', COUNT(*) FROM venues
UNION ALL
SELECT 'Total Series', COUNT(*) FROM series
UNION ALL
SELECT 'Total Matches', COUNT(*) FROM matches
UNION ALL
SELECT 'Total Batting Stats', COUNT(*) FROM batting_stats
UNION ALL
SELECT 'Total Bowling Stats', COUNT(*) FROM bowling_stats
UNION ALL
SELECT 'Total Career Stats', COUNT(*) FROM player_career_stats;

SELECT '=== QUERY VERIFICATION ===' as Info;

-- Test Q9: All-rounders
SELECT 'Q9: All-rounders with 1000+ runs and 50+ wickets' as Query;
SELECT 
    p.player_name AS 'Player',
    pcs.total_runs AS 'Runs',
    pcs.total_wickets AS 'Wickets',
    pcs.match_format AS 'Format'
FROM player_career_stats pcs
JOIN players p ON pcs.player_id = p.player_id
WHERE pcs.total_runs > 1000 
  AND pcs.total_wickets > 50
  AND p.playing_role = 'All-rounder'
ORDER BY pcs.total_runs DESC;

-- Test Q15: Close match performers
SELECT 'Q15: Close Match Performers (should show results now)' as Query;
SELECT COUNT(*) as 'Close Matches in Database' 
FROM matches 
WHERE (victory_type = 'runs' AND victory_margin < 50)
   OR (victory_type = 'wickets' AND victory_margin < 5);

-- Test Q16: Performance trends
SELECT 'Q16: Performance Trends 2020-2024 (should show results now)' as Query;
SELECT COUNT(DISTINCT YEAR(match_date)) as 'Years with Data' 
FROM matches 
WHERE YEAR(match_date) >= 2020;

SELECT 'Data loading complete! All queries should now work.' as Status;
