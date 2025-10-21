-- sample_data.sql
INSERT INTO Venues (name, city, country, capacity) VALUES ('Eden Gardens', 'Kolkata', 'India', 68000);
INSERT INTO Venues (name, city, country, capacity) VALUES ('Wankhede Stadium', 'Mumbai', 'India', 33000);

INSERT INTO Teams (name, country) VALUES ('India', 'India');
INSERT INTO Teams (name, country) VALUES ('Australia', 'Australia');

INSERT INTO Players (name, country, playing_role, batting_style, bowling_style, total_runs, total_wickets, batting_average, bowling_average, strike_rate, economy_rate)
VALUES
('Virat Kohli', 'India', 'Batsman', 'Right-hand bat', '', 25000, 0, 53.4, NULL, 93.1, NULL),
('Ravindra Jadeja', 'India', 'Allrounder', 'Left-hand bat', 'Left-arm orthodox', 3000, 250, 34.1, 28.2, 62.5, 3.9),
('Mitchell Starc', 'Australia', 'Bowler', 'Left-hand bat', 'Left-arm fast', 1000, 350, 22.5, 24.3, 80.1, 4.2);

INSERT INTO Matches (description, team1, team2, venue_id, match_date, format, winning_team, victory_margin, victory_type, toss_winner, toss_decision)
VALUES ('India vs Australia - Test 1', 'India', 'Australia', 1, '2024-01-15', 'Test', 'India', '5 wickets', 'Wickets', 'India', 'Field'),
('India vs Australia - ODI 1', 'India', 'Australia', 2, '2024-02-20', 'ODI', 'Australia', '20 runs', 'Runs', 'Australia', 'Bat');

INSERT INTO Batting_Performance (player_id, match_id, innings, runs, balls_faced, fours, sixes, strike_rate, batting_position)
VALUES (1, 2, 1, 120, 115, 12, 1, 104.3, 3),
(2, 2, 1, 45, 60, 4, 0, 75.0, 5);

INSERT INTO Bowling_Performance (player_id, match_id, innings, overs, wickets, runs_conceded, economy_rate)
VALUES (3, 2, 2, 10.0, 4, 50, 5.0),
(2, 2, 2, 10.0, 2, 45, 4.5);
