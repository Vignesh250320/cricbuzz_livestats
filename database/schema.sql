-- =====================================
-- 🏏 Cricbuzz LiveStats Database Schema
-- Compatible with MySQL 8.x
-- Version: 2.0
-- =====================================

DROP DATABASE IF EXISTS cricbuzz_livestats;
CREATE DATABASE cricbuzz_livestats 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE cricbuzz_livestats;

-- =====================
-- 1️⃣ Teams Table
-- =====================
CREATE TABLE Teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(100) NOT NULL,
    total_wins INT DEFAULT 0,
    total_losses INT DEFAULT 0,
    total_matches INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_country (country),
    INDEX idx_team_name (team_name)
) ENGINE=InnoDB;

-- =====================
-- 2️⃣ Venues Table
-- =====================
CREATE TABLE Venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INT DEFAULT 0,
    established_year INT,
    
    INDEX idx_country (country),
    INDEX idx_city (city),
    INDEX idx_venue_name (venue_name)
) ENGINE=InnoDB;

-- =====================
-- 3️⃣ Players Table
-- =====================
CREATE TABLE Players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    country VARCHAR(100),
    playing_role ENUM('Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper') DEFAULT 'Batsman',
    batting_style VARCHAR(50),
    bowling_style VARCHAR(50),
    date_of_birth DATE,
    total_runs INT DEFAULT 0,
    total_wickets INT DEFAULT 0,
    total_matches INT DEFAULT 0,
    batting_average DECIMAL(6,2) DEFAULT 0.00,
    bowling_average DECIMAL(6,2) DEFAULT 0.00,
    strike_rate DECIMAL(6,2) DEFAULT 0.00,
    economy_rate DECIMAL(5,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_country (country),
    INDEX idx_full_name (full_name),
    INDEX idx_playing_role (playing_role),
    INDEX idx_total_runs (total_runs),
    INDEX idx_total_wickets (total_wickets)
) ENGINE=InnoDB;

-- =====================
-- 4️⃣ Matches Table
-- =====================
CREATE TABLE Matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    match_description VARCHAR(200),
    team1_id INT NOT NULL,
    team2_id INT NOT NULL,
    venue_id INT,
    match_date DATE NOT NULL,
    match_format ENUM('Test', 'ODI', 'T20I') NOT NULL,
    winning_team_id INT,
    victory_margin VARCHAR(50),
    victory_type ENUM('runs', 'wickets', 'tie', 'no result'),
    toss_winner_id INT,
    toss_decision ENUM('bat', 'field', 'Bat', 'Field'),
    match_status ENUM('Scheduled', 'Live', 'Completed', 'Abandoned') DEFAULT 'Completed',
    series_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (venue_id) REFERENCES Venues(venue_id) ON DELETE SET NULL,
    FOREIGN KEY (team1_id) REFERENCES Teams(team_id) ON DELETE CASCADE,
    FOREIGN KEY (team2_id) REFERENCES Teams(team_id) ON DELETE CASCADE,
    FOREIGN KEY (winning_team_id) REFERENCES Teams(team_id) ON DELETE SET NULL,
    FOREIGN KEY (toss_winner_id) REFERENCES Teams(team_id) ON DELETE SET NULL,
    
    INDEX idx_match_date (match_date),
    INDEX idx_match_format (match_format),
    INDEX idx_match_status (match_status),
    INDEX idx_team1 (team1_id),
    INDEX idx_team2 (team2_id),
    INDEX idx_venue (venue_id),
    INDEX idx_winning_team (winning_team_id)
) ENGINE=InnoDB;

-- =====================
-- 5️⃣ Batting Performance
-- =====================
CREATE TABLE Batting_Performance (
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
    
    FOREIGN KEY (player_id) REFERENCES Players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (match_id) REFERENCES Matches(match_id) ON DELETE CASCADE,
    
    INDEX idx_player (player_id),
    INDEX idx_match (match_id),
    INDEX idx_innings (innings_id),
    INDEX idx_runs (runs),
    INDEX idx_strike_rate (strike_rate),
    UNIQUE KEY unique_batting_performance (player_id, match_id, innings_id, batting_position)
) ENGINE=InnoDB;

-- =====================
-- 6️⃣ Bowling Performance
-- =====================
CREATE TABLE Bowling_Performance (
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
    
    FOREIGN KEY (player_id) REFERENCES Players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (match_id) REFERENCES Matches(match_id) ON DELETE CASCADE,
    
    INDEX idx_player (player_id),
    INDEX idx_match (match_id),
    INDEX idx_innings (innings_id),
    INDEX idx_wickets (wickets),
    INDEX idx_economy (economy_rate),
    UNIQUE KEY unique_bowling_performance (player_id, match_id, innings_id)
) ENGINE=InnoDB;

-- =====================
-- 7️⃣ Series Table
-- =====================
CREATE TABLE Series (
    series_id INT AUTO_INCREMENT PRIMARY KEY,
    series_name VARCHAR(150) NOT NULL,
    host_country VARCHAR(100),
    match_type ENUM('Test', 'ODI', 'T20I', 'Mixed') DEFAULT 'ODI',
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_series_name (series_name),
    INDEX idx_start_date (start_date),
    INDEX idx_match_type (match_type)
) ENGINE=InnoDB;

-- Add foreign key for Matches to Series
ALTER TABLE Matches
    ADD FOREIGN KEY (series_id) REFERENCES Series(series_id) ON DELETE SET NULL;

-- =====================================
-- 📊 USEFUL VIEWS
-- =====================================

-- View: Player Statistics Summary
CREATE OR REPLACE VIEW vw_player_stats AS
SELECT 
    p.player_id,
    p.full_name,
    p.country,
    p.playing_role,
    p.total_runs,
    p.total_wickets,
    p.total_matches,
    p.batting_average,
    p.bowling_average,
    p.strike_rate,
    p.economy_rate,
    ROUND((COALESCE(p.total_runs,0)*0.01 + COALESCE(p.batting_average,0)*0.5 + 
           COALESCE(p.strike_rate,0)*0.3 + COALESCE(p.total_wickets,0)*2 + 
           (50-COALESCE(p.bowling_average,0))*0.5 + 
           ((6-COALESCE(p.economy_rate,0))*2)),2) AS performance_score
FROM Players p;

-- View: Match Summary
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

-- View: Top Run Scorers
CREATE OR REPLACE VIEW vw_top_run_scorers AS
SELECT 
    p.full_name,
    p.country,
    p.total_runs,
    p.batting_average,
    p.strike_rate,
    p.total_matches
FROM Players p
WHERE p.total_runs > 0
ORDER BY p.total_runs DESC
LIMIT 50;

-- View: Top Wicket Takers
CREATE OR REPLACE VIEW vw_top_wicket_takers AS
SELECT 
    p.full_name,
    p.country,
    p.total_wickets,
    p.bowling_average,
    p.economy_rate,
    p.total_matches
FROM Players p
WHERE p.total_wickets > 0
ORDER BY p.total_wickets DESC
LIMIT 50;

-- =====================================
-- 🔧 STORED PROCEDURES
-- =====================================

-- Procedure: Update Player Statistics
DELIMITER //
CREATE PROCEDURE sp_update_player_stats(IN p_player_id INT)
BEGIN
    UPDATE Players p
    SET 
        total_runs = COALESCE((SELECT SUM(runs) FROM Batting_Performance WHERE player_id = p_player_id), 0),
        total_wickets = COALESCE((SELECT SUM(wickets) FROM Bowling_Performance WHERE player_id = p_player_id), 0),
        total_matches = COALESCE((SELECT COUNT(DISTINCT match_id) 
                                  FROM (SELECT match_id FROM Batting_Performance WHERE player_id = p_player_id
                                        UNION
                                        SELECT match_id FROM Bowling_Performance WHERE player_id = p_player_id) AS matches), 0),
        batting_average = COALESCE((SELECT AVG(runs) FROM Batting_Performance WHERE player_id = p_player_id AND balls_faced > 0), 0),
        strike_rate = COALESCE((SELECT AVG(strike_rate) FROM Batting_Performance WHERE player_id = p_player_id AND balls_faced > 0), 0),
        bowling_average = COALESCE((SELECT AVG(runs_conceded/NULLIF(wickets,0)) FROM Bowling_Performance WHERE player_id = p_player_id AND wickets > 0), 0),
        economy_rate = COALESCE((SELECT AVG(economy_rate) FROM Bowling_Performance WHERE player_id = p_player_id AND overs > 0), 0)
    WHERE player_id = p_player_id;
END //
DELIMITER ;

-- Procedure: Update Team Statistics
DELIMITER //
CREATE PROCEDURE sp_update_team_stats(IN p_team_id INT)
BEGIN
    UPDATE Teams t
    SET 
        total_wins = (SELECT COUNT(*) FROM Matches WHERE winning_team_id = p_team_id),
        total_losses = (SELECT COUNT(*) FROM Matches 
                       WHERE (team1_id = p_team_id OR team2_id = p_team_id) 
                       AND winning_team_id != p_team_id 
                       AND winning_team_id IS NOT NULL),
        total_matches = (SELECT COUNT(*) FROM Matches 
                        WHERE team1_id = p_team_id OR team2_id = p_team_id)
    WHERE team_id = p_team_id;
END //
DELIMITER ;

-- =====================================
-- 🎯 TRIGGERS
-- =====================================

-- Trigger: Auto-update player stats after batting performance insert
DELIMITER //
CREATE TRIGGER tr_after_batting_insert
AFTER INSERT ON Batting_Performance
FOR EACH ROW
BEGIN
    CALL sp_update_player_stats(NEW.player_id);
END //
DELIMITER ;

-- Trigger: Auto-update player stats after bowling performance insert
DELIMITER //
CREATE TRIGGER tr_after_bowling_insert
AFTER INSERT ON Bowling_Performance
FOR EACH ROW
BEGIN
    CALL sp_update_player_stats(NEW.player_id);
END //
DELIMITER ;

-- =====================================
-- 📝 INITIAL DATA (Optional)
-- =====================================

-- Insert sample countries/teams (Uncomment to use)
/*
INSERT INTO Teams (team_name, country) VALUES
    ('India', 'India'),
    ('Australia', 'Australia'),
    ('England', 'England'),
    ('Pakistan', 'Pakistan'),
    ('South Africa', 'South Africa'),
    ('New Zealand', 'New Zealand'),
    ('Sri Lanka', 'Sri Lanka'),
    ('West Indies', 'West Indies'),
    ('Bangladesh', 'Bangladesh'),
    ('Afghanistan', 'Afghanistan');
*/

-- Insert sample venues (Uncomment to use)
/*
INSERT INTO Venues (venue_name, city, country, capacity) VALUES
    ('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
    ('Eden Gardens', 'Kolkata', 'India', 66000),
    ('Lord\'s Cricket Ground', 'London', 'England', 31100),
    ('Wankhede Stadium', 'Mumbai', 'India', 33108),
    ('Wanderers Stadium', 'Johannesburg', 'South Africa', 34000);
*/

-- =====================================
-- ✅ SCHEMA CREATION COMPLETE
-- =====================================

-- To use this schema:
-- 1. Run: mysql -u root -p < schema.sql
-- 2. Or execute in MySQL Workbench/CLI
-- 3. Update .env file with database credentials
-- 4. Test connection: python test_env.py

-- Performance Optimization Notes:
-- - All foreign keys have ON DELETE actions defined
-- - Indexes created on frequently queried columns
-- - Composite unique keys prevent duplicate data
-- - UTF8MB4 charset supports international characters
-- - InnoDB engine for ACID compliance and foreign keys

-- Query Performance Tips:
-- 1. Use vw_* views for common queries
-- 2. Indexes optimize WHERE, JOIN, ORDER BY clauses
-- 3. EXPLAIN queries to check index usage
-- 4. Regularly run ANALYZE TABLE for updated statistics
