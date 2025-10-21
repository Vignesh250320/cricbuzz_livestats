-- schema.sql
CREATE TABLE IF NOT EXISTS Players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    playing_role VARCHAR(50),
    batting_style VARCHAR(100),
    bowling_style VARCHAR(100),
    total_runs INT DEFAULT 0,
    total_wickets INT DEFAULT 0,
    batting_average DECIMAL(6,2),
    bowling_average DECIMAL(6,2),
    strike_rate DECIMAL(6,2),
    economy_rate DECIMAL(6,2)
);

CREATE TABLE IF NOT EXISTS Teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INT
);

CREATE TABLE IF NOT EXISTS Matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(512),
    team1 VARCHAR(255),
    team2 VARCHAR(255),
    venue_id INT,
    match_date DATE,
    format VARCHAR(20),
    winning_team VARCHAR(255),
    victory_margin VARCHAR(100),
    victory_type VARCHAR(100),
    toss_winner VARCHAR(255),
    toss_decision VARCHAR(50),
    FOREIGN KEY (venue_id) REFERENCES Venues(venue_id)
);

CREATE TABLE IF NOT EXISTS Innings (
    innings_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    batting_team VARCHAR(255),
    bowling_team VARCHAR(255),
    FOREIGN KEY (match_id) REFERENCES Matches(match_id)
);

CREATE TABLE IF NOT EXISTS Batting_Performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    match_id INT,
    innings INT,
    runs INT,
    balls_faced INT,
    fours INT,
    sixes INT,
    strike_rate DECIMAL(6,2),
    batting_position INT,
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (match_id) REFERENCES Matches(match_id)
);

CREATE TABLE IF NOT EXISTS Bowling_Performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    match_id INT,
    innings INT,
    overs DECIMAL(5,1),
    wickets INT,
    runs_conceded INT,
    economy_rate DECIMAL(5,2),
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (match_id) REFERENCES Matches(match_id)
);
