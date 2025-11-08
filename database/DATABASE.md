# 🏏 Cricbuzz LiveStats - Database Documentation

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Schema Overview](#schema-overview)
3. [Table Details](#table-details)
4. [Views & Procedures](#views--procedures)
5. [Common Queries](#common-queries)
6. [Setup Instructions](#setup-instructions)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Setup Database (Choose One Method)

**Python Script (Recommended):**
```bash
python database/setup_database.py
```

**MySQL Command Line:**
```bash
mysql -u root -p < database/schema.sql
```

**MySQL Workbench:**
File → Run SQL Script → Select `schema.sql`

---

## 📊 Schema Overview

### Tables (7)
- **Teams** - Cricket teams with statistics
- **Venues** - Stadium information
- **Players** - Player profiles and career stats
- **Matches** - Match details and results
- **Batting_Performance** - Match-by-match batting stats
- **Bowling_Performance** - Match-by-match bowling stats
- **Series** - Tournament/series information

### Features
- ✅ **30+ Indexes** for fast queries
- ✅ **4 Views** for common operations
- ✅ **2 Stored Procedures** for stat updates
- ✅ **2 Triggers** for auto-calculations
- ✅ **Foreign Keys** with proper CASCADE rules
- ✅ **UTF8MB4** encoding for international names
- ✅ **MySQL 8.0+** compatible

---

## 📝 Table Details

### 1. Teams
```sql
CREATE TABLE Teams (
    team_id INT PRIMARY KEY AUTO_INCREMENT,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(100) NOT NULL,
    total_wins INT DEFAULT 0,
    total_losses INT DEFAULT 0,
    total_matches INT DEFAULT 0
);
```
**Indexes:** team_name, country

---

### 2. Venues
```sql
CREATE TABLE Venues (
    venue_id INT PRIMARY KEY AUTO_INCREMENT,
    venue_name VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INT DEFAULT 0,
    established_year INT
);
```
**Indexes:** venue_name, city, country

---

### 3. Players
```sql
CREATE TABLE Players (
    player_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(120) NOT NULL,
    country VARCHAR(100),
    playing_role ENUM('Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper'),
    batting_style VARCHAR(50),
    bowling_style VARCHAR(50),
    date_of_birth DATE,
    total_runs INT DEFAULT 0,
    total_wickets INT DEFAULT 0,
    total_matches INT DEFAULT 0,
    batting_average DECIMAL(6,2),
    bowling_average DECIMAL(6,2),
    strike_rate DECIMAL(6,2),
    economy_rate DECIMAL(5,2)
);
```
**Indexes:** full_name, country, playing_role, total_runs, total_wickets  
**Auto-Updates:** Via triggers when performance data inserted

---

### 4. Matches
```sql
CREATE TABLE Matches (
    match_id INT PRIMARY KEY AUTO_INCREMENT,
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
    toss_decision ENUM('bat', 'field'),
    match_status ENUM('Scheduled', 'Live', 'Completed', 'Abandoned'),
    series_id INT,
    FOREIGN KEY (venue_id) REFERENCES Venues(venue_id),
    FOREIGN KEY (team1_id) REFERENCES Teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES Teams(team_id),
    FOREIGN KEY (winning_team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (series_id) REFERENCES Series(series_id)
);
```
**Indexes:** match_date, match_format, match_status, all team IDs

---

### 5. Batting_Performance
```sql
CREATE TABLE Batting_Performance (
    batting_id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT NOT NULL,
    match_id INT NOT NULL,
    innings_id INT NOT NULL,
    runs INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    fours INT DEFAULT 0,
    sixes INT DEFAULT 0,
    strike_rate DECIMAL(6,2),
    batting_position INT,
    dismissal_type VARCHAR(50),
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (match_id) REFERENCES Matches(match_id),
    UNIQUE KEY (player_id, match_id, innings_id, batting_position)
);
```
**Indexes:** player_id, match_id, innings_id, runs, strike_rate  
**Trigger:** Auto-updates player stats on insert

---

### 6. Bowling_Performance
```sql
CREATE TABLE Bowling_Performance (
    bowling_id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT NOT NULL,
    match_id INT NOT NULL,
    innings_id INT NOT NULL,
    overs DECIMAL(5,1) DEFAULT 0.0,
    wickets INT DEFAULT 0,
    runs_conceded INT DEFAULT 0,
    economy_rate DECIMAL(5,2),
    maidens INT DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (match_id) REFERENCES Matches(match_id),
    UNIQUE KEY (player_id, match_id, innings_id)
);
```
**Indexes:** player_id, match_id, innings_id, wickets, economy_rate  
**Trigger:** Auto-updates player stats on insert

---

### 7. Series
```sql
CREATE TABLE Series (
    series_id INT PRIMARY KEY AUTO_INCREMENT,
    series_name VARCHAR(150) NOT NULL,
    host_country VARCHAR(100),
    match_type ENUM('Test', 'ODI', 'T20I', 'Mixed'),
    start_date DATE,
    end_date DATE
);
```
**Indexes:** series_name, start_date, match_type

---

## 📊 Views & Procedures

### Views (4)

#### 1. vw_player_stats
Complete player statistics with performance score
```sql
SELECT * FROM vw_player_stats WHERE country = 'India';
```

#### 2. vw_match_summary
Match details with team and venue names
```sql
SELECT * FROM vw_match_summary WHERE match_date >= '2024-01-01';
```

#### 3. vw_top_run_scorers
Top 50 run scorers
```sql
SELECT * FROM vw_top_run_scorers;
```

#### 4. vw_top_wicket_takers
Top 50 wicket takers
```sql
SELECT * FROM vw_top_wicket_takers;
```

### Stored Procedures (2)

#### 1. sp_update_player_stats
Recalculates all player statistics
```sql
CALL sp_update_player_stats(1);  -- Update player_id 1
```

#### 2. sp_update_team_stats
Updates team win/loss counts
```sql
CALL sp_update_team_stats(2);  -- Update team_id 2
```

### Triggers (2)
- **tr_after_batting_insert** - Auto-updates player stats after batting insert
- **tr_after_bowling_insert** - Auto-updates player stats after bowling insert

---

## 🔍 Common Queries

### Get all matches for a team
```sql
SELECT * FROM vw_match_summary 
WHERE team1 = 'India' OR team2 = 'India'
ORDER BY match_date DESC;
```

### Top 10 run scorers
```sql
SELECT full_name, country, total_runs, batting_average 
FROM Players 
ORDER BY total_runs DESC 
LIMIT 10;
```

### Recent matches
```sql
SELECT * FROM vw_match_summary
ORDER BY match_date DESC
LIMIT 20;
```

### Players by role
```sql
SELECT playing_role, COUNT(*) as count
FROM Players
GROUP BY playing_role;
```

### Match stats by format
```sql
SELECT match_format, COUNT(*) as total_matches
FROM Matches
GROUP BY match_format;
```

### Player format-wise performance
```sql
SELECT 
    p.full_name,
    SUM(CASE WHEN m.match_format='Test' THEN bp.runs ELSE 0 END) AS Test_Runs,
    SUM(CASE WHEN m.match_format='ODI' THEN bp.runs ELSE 0 END) AS ODI_Runs,
    SUM(CASE WHEN m.match_format='T20I' THEN bp.runs ELSE 0 END) AS T20_Runs
FROM Batting_Performance bp
JOIN Matches m ON bp.match_id = m.match_id
JOIN Players p ON bp.player_id = p.player_id
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT m.match_format) >= 2;
```

### Venue statistics
```sql
SELECT 
    v.venue_name,
    v.city,
    COUNT(*) as total_matches,
    COUNT(DISTINCT m.team1_id) + COUNT(DISTINCT m.team2_id) as teams_played
FROM Matches m
JOIN Venues v ON m.venue_id = v.venue_id
GROUP BY v.venue_id, v.venue_name, v.city
ORDER BY total_matches DESC;
```

---

## 🔧 Setup Instructions

### Step 1: Create Database

**Using Python Script:**
```bash
cd c:\Users\Vignesh\CascadeProjects\cricbuzz_livestats
python database/setup_database.py
```

**Using MySQL CLI:**
```bash
mysql -u root -p < database/schema.sql
```

### Step 2: Create Application User

```sql
-- Create user
CREATE USER 'cb_user'@'localhost' IDENTIFIED BY 'your_password';

-- Grant permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON cricbuzz_livestats.* TO 'cb_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;
```

### Step 3: Update .env File

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=cb_user
DB_PASSWORD=your_password
DB_NAME=cricbuzz_livestats
```

### Step 4: Verify Installation

```sql
USE cricbuzz_livestats;

-- Check tables (should show 7)
SHOW TABLES;

-- Check views (should show 4)
SHOW FULL TABLES WHERE Table_type = 'VIEW';

-- Check procedures (should show 2)
SHOW PROCEDURE STATUS WHERE Db = 'cricbuzz_livestats';

-- Check triggers (should show 2)
SHOW TRIGGERS;
```

### Step 5: Test Connection

```bash
python test_env.py
```

---

## 🔧 Troubleshooting

### Connection Error
```bash
# Check if MySQL is running (Windows)
net start MySQL80

# Test connection
python test_env.py
```

### Permission Error
```sql
GRANT ALL PRIVILEGES ON cricbuzz_livestats.* TO 'cb_user'@'localhost';
FLUSH PRIVILEGES;
```

### Schema Already Exists
```sql
DROP DATABASE IF EXISTS cricbuzz_livestats;
-- Then run schema.sql again
```

### SQL Mode Issues
```sql
-- Check current SQL mode
SELECT @@sql_mode;

-- If needed, disable ONLY_FULL_GROUP_BY (temporary)
SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
```
**Note:** All queries in this project are compatible with `ONLY_FULL_GROUP_BY` mode.

---

## 💾 Backup & Restore

### Backup Database
```bash
mysqldump -u root -p cricbuzz_livestats > backup_$(date +%Y%m%d).sql
```

### Restore Database
```bash
mysql -u root -p cricbuzz_livestats < backup_20241107.sql
```

### Check Table Sizes
```sql
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
FROM information_schema.TABLES
WHERE table_schema = 'cricbuzz_livestats'
ORDER BY size_mb DESC;
```

---

## 📈 Performance Tips

### Use Indexes
```sql
-- ✅ Good - Uses index
SELECT * FROM Players WHERE total_runs > 10000;

-- ❌ Bad - Full table scan
SELECT * FROM Players WHERE full_name LIKE '%Kohli%';

-- ✅ Better - Uses index
SELECT * FROM Players WHERE full_name LIKE 'Kohli%';
```

### Use Views
```sql
-- Instead of complex JOINs
SELECT * FROM vw_match_summary WHERE match_format = 'ODI';
```

### Analyze Queries
```sql
EXPLAIN SELECT * FROM Players WHERE country = 'India';
```

### Update Statistics
```sql
ANALYZE TABLE Players, Matches, Batting_Performance, Bowling_Performance;
```

---

## ✅ Checklist

- [ ] MySQL 8.0+ installed
- [ ] Database created: `cricbuzz_livestats`
- [ ] 7 tables created
- [ ] 4 views created
- [ ] 2 procedures created
- [ ] 2 triggers created
- [ ] User credentials in `.env`
- [ ] Connection tested with `python test_env.py`
- [ ] Streamlit app runs: `streamlit run app.py`

---

## 📞 Support

### Files in database/ folder:
- `schema.sql` - Complete database schema (375 lines)
- `DATABASE.md` - This comprehensive guide
- `setup_database.py` - Automated setup script
- `sample_data.sql` - Sample data (optional)

### Need Help?
1. Check SQL mode: `SELECT @@sql_mode;`
2. Verify MySQL version: `SELECT VERSION();`
3. Test connection: `python test_env.py`
4. Check MySQL logs for errors

---

**Schema Version**: 2.0  
**MySQL**: 8.0+  
**Status**: ✅ Production Ready  
**Last Updated**: November 7, 2025
