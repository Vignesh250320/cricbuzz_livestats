USE cricbuzz_livestats;

-- Create Matches table without foreign keys first
CREATE TABLE IF NOT EXISTS Matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    match_description VARCHAR(200),
    team1_id INT,
    team2_id INT,
    venue_id INT,
    match_date DATE,
    match_format ENUM('Test', 'ODI', 'T20I'),
    winning_team_id INT,
    victory_margin VARCHAR(50),
    victory_type ENUM('runs', 'wickets', 'tie', 'no result'),
    toss_winner_id INT,
    toss_decision ENUM('bat', 'field'),
    match_status ENUM('Scheduled', 'Live', 'Completed', 'Abandoned') DEFAULT 'Completed',
    series_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_match_date (match_date),
    INDEX idx_match_format (match_format),
    INDEX idx_match_status (match_status)
) ENGINE=InnoDB;

-- Create Batting_Performance table
CREATE TABLE IF NOT EXISTS Batting_Performance (
    batting_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    match_id INT NOT NULL,
    innings_id INT NOT NULL,
    runs INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    fours INT DEFAULT 0,
    sixes INT DEFAULT 0,
    strike_rate DECIMAL(6,2) DEFAULT 0.00,
    batting_position INT,
    dismissal_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_player (player_id),
    INDEX idx_match (match_id),
    INDEX idx_innings (innings_id)
) ENGINE=InnoDB;

-- Create Bowling_Performance table
CREATE TABLE IF NOT EXISTS Bowling_Performance (
    bowling_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    match_id INT NOT NULL,
    innings_id INT NOT NULL,
    overs DECIMAL(5,1) DEFAULT 0.0,
    wickets INT DEFAULT 0,
    runs_conceded INT DEFAULT 0,
    economy_rate DECIMAL(5,2) DEFAULT 0.00,
    maidens INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_player (player_id),
    INDEX idx_match (match_id),
    INDEX idx_innings (innings_id)
) ENGINE=InnoDB;

-- Create match summary view
CREATE OR REPLACE VIEW vw_match_summary AS
SELECT 
    m.match_id,
    m.match_description,
    m.match_date,
    m.match_format,
    t1.team_name AS team1,
    t2.team_name AS team2,
    v.venue_name,
    v.city,
    tw.team_name AS winning_team,
    m.victory_margin,
    m.victory_type,
    m.match_status
FROM Matches m
LEFT JOIN Teams t1 ON m.team1_id = t1.team_id
LEFT JOIN Teams t2 ON m.team2_id = t2.team_id
LEFT JOIN Venues v ON m.venue_id = v.venue_id
LEFT JOIN Teams tw ON m.winning_team_id = tw.team_id;
