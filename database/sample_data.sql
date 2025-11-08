USE cricbuzz_livestats;

-- Insert Venues
INSERT INTO Venues (venue_name, city, country, capacity)
VALUES
('Eden Gardens', 'Kolkata', 'India', 68000),
('Wankhede Stadium', 'Mumbai', 'India', 33000),
('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024);

-- Insert Teams
INSERT INTO Teams (team_name, country, total_wins, total_losses)
VALUES
('India', 'India', 580, 300),
('Australia', 'Australia', 610, 270);

-- Insert Players
INSERT INTO Players (full_name, country, playing_role, batting_style, bowling_style, total_runs, total_wickets, batting_average, bowling_average, strike_rate, economy_rate)
VALUES
('Virat Kohli', 'India', 'Batsman', 'Right-hand bat', NULL, 25000, 4, 53.4, NULL, 93.1, NULL),
('Ravindra Jadeja', 'India', 'Allrounder', 'Left-hand bat', 'Left-arm orthodox', 3500, 250, 34.1, 28.2, 82.3, 4.3),
('Mitchell Starc', 'Australia', 'Bowler', 'Left-hand bat', 'Left-arm fast', 1200, 350, 22.5, 24.3, 79.2, 4.6),
('Steve Smith', 'Australia', 'Batsman', 'Right-hand bat', NULL, 9500, 0, 59.8, NULL, 88.4, NULL);

-- Insert Matches
INSERT INTO Matches (match_description, team1_id, team2_id, venue_id, match_date, match_format, winning_team_id, victory_margin, victory_type, toss_winner_id, toss_decision, match_status)
VALUES
('India vs Australia - Test 1', 1, 2, 1, '2024-01-15', 'Test', 1, '5 wickets', 'Wickets', 1, 'Field', 'Completed'),
('India vs Australia - ODI 1', 1, 2, 2, '2024-02-20', 'ODI', 2, '20 runs', 'Runs', 2, 'Bat', 'Completed');

-- Insert Batting Performance
INSERT INTO Batting_Performance (player_id, match_id, innings_id, runs, balls_faced, fours, sixes, strike_rate, batting_position)
VALUES
(1, 2, 1, 120, 115, 12, 1, 104.3, 3),
(2, 2, 1, 45, 60, 4, 0, 75.0, 5),
(4, 1, 1, 150, 220, 16, 0, 68.1, 3);

-- Insert Bowling Performance
INSERT INTO Bowling_Performance (player_id, match_id, innings_id, overs, wickets, runs_conceded, economy_rate)
VALUES
(3, 2, 2, 10.0, 4, 50, 5.0),
(2, 2, 2, 10.0, 2, 45, 4.5),
(2, 1, 2, 25.0, 6, 80, 3.2);
