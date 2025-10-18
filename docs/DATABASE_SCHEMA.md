# 🗄️ Database Schema Documentation

Complete database schema for Cricbuzz LiveStats project.

---

## 📊 Entity Relationship Diagram

```
┌─────────────────┐
│     TEAMS       │
├─────────────────┤
│ team_id (PK)    │◄─────┐
│ team_name       │      │
│ country         │      │
│ team_type       │      │
│ created_at      │      │
└─────────────────┘      │
                         │
                         │ FK
┌─────────────────┐      │
│    PLAYERS      │      │
├─────────────────┤      │
│ player_id (PK)  │      │
│ player_name     │      │
│ team_id (FK)    │──────┘
│ country         │
│ playing_role    │
│ batting_style   │
│ bowling_style   │
│ date_of_birth   │
│ created_at      │
└─────────────────┘
        │
        │ FK
        ▼
┌──────────────────────┐
│ PLAYER_CAREER_STATS  │
├──────────────────────┤
│ career_stat_id (PK)  │
│ player_id (FK)       │
│ match_format         │
│ total_matches        │
│ total_innings        │
│ total_runs           │
│ batting_average      │
│ highest_score        │
│ centuries            │
│ half_centuries       │
│ total_wickets        │
│ bowling_average      │
│ best_bowling         │
│ catches              │
│ stumpings            │
│ created_at           │
│ updated_at           │
└──────────────────────┘


┌─────────────────┐
│     VENUES      │
├─────────────────┤
│ venue_id (PK)   │◄─────┐
│ venue_name      │      │
│ city            │      │
│ country         │      │
│ capacity        │      │
│ created_at      │      │
└─────────────────┘      │
                         │
                         │ FK
┌─────────────────┐      │
│     SERIES      │      │
├─────────────────┤      │
│ series_id (PK)  │◄───┐ │
│ series_name     │    │ │
│ host_country    │    │ │
│ match_type      │    │ │
│ start_date      │    │ │
│ end_date        │    │ │
│ total_matches   │    │ │
│ created_at      │    │ │
└─────────────────┘    │ │
                       │ │
                       │ │ FK
┌─────────────────────┤ │
│      MATCHES        │ │
├─────────────────────┤ │
│ match_id (PK)       │ │
│ series_id (FK)      │─┘
│ match_description   │
│ match_format        │
│ team1_id (FK)       │───┐
│ team2_id (FK)       │───┤ FK to TEAMS
│ venue_id (FK)       │───┼─┘
│ match_date          │   │
│ toss_winner_id (FK) │───┤
│ toss_decision       │   │
│ winner_id (FK)      │───┘
│ victory_margin      │
│ victory_type        │
│ match_status        │
│ created_at          │
└─────────────────────┘
        │
        │ FK
        ├──────────────────┐
        │                  │
        ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│ BATTING_STATS   │  │ BOWLING_STATS   │
├─────────────────┤  ├─────────────────┤
│ stat_id (PK)    │  │ stat_id (PK)    │
│ player_id (FK)  │  │ player_id (FK)  │
│ match_id (FK)   │  │ match_id (FK)   │
│ innings_number  │  │ innings_number  │
│ runs_scored     │  │ overs_bowled    │
│ balls_faced     │  │ runs_conceded   │
│ fours           │  │ wickets_taken   │
│ sixes           │  │ maidens         │
│ strike_rate     │  │ economy_rate    │
│ is_out          │  │ created_at      │
│ dismissal_type  │  └─────────────────┘
│ created_at      │
└─────────────────┘
```

---

## 📋 Table Definitions

### 1. TEAMS

**Purpose**: Store cricket team information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| team_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique team identifier |
| team_name | VARCHAR(100) | NOT NULL, UNIQUE | Team name |
| country | VARCHAR(100) | | Country name |
| team_type | VARCHAR(50) | | International/Domestic/Franchise |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

**Sample Data**:
```sql
INSERT INTO teams (team_name, country, team_type) VALUES
('India', 'India', 'International'),
('Australia', 'Australia', 'International');
```

---

### 2. VENUES

**Purpose**: Store cricket venue/stadium information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| venue_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique venue identifier |
| venue_name | VARCHAR(200) | NOT NULL | Venue/stadium name |
| city | VARCHAR(100) | | City location |
| country | VARCHAR(100) | | Country location |
| capacity | INT | | Seating capacity |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

**Sample Data**:
```sql
INSERT INTO venues (venue_name, city, country, capacity) VALUES
('Wankhede Stadium', 'Mumbai', 'India', 33000),
('MCG', 'Melbourne', 'Australia', 100000);
```

---

### 3. PLAYERS

**Purpose**: Store player profiles and information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| player_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique player identifier |
| player_name | VARCHAR(100) | NOT NULL | Player full name |
| team_id | INT | FOREIGN KEY → teams(team_id) | Current team |
| country | VARCHAR(100) | | Player's country |
| playing_role | VARCHAR(50) | | Batsman/Bowler/All-rounder/WK |
| batting_style | VARCHAR(50) | | Right/Left hand bat |
| bowling_style | VARCHAR(50) | | Bowling type |
| date_of_birth | DATE | | Birth date |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

**Sample Data**:
```sql
INSERT INTO players (player_name, team_id, country, playing_role, batting_style) VALUES
('Virat Kohli', 1, 'India', 'Batsman', 'Right-hand bat');
```

---

### 4. SERIES

**Purpose**: Store cricket series information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| series_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique series identifier |
| series_name | VARCHAR(200) | NOT NULL | Series name |
| host_country | VARCHAR(100) | | Hosting country |
| match_type | VARCHAR(50) | | Test/ODI/T20I |
| start_date | DATE | | Series start date |
| end_date | DATE | | Series end date |
| total_matches | INT | | Number of matches |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

**Sample Data**:
```sql
INSERT INTO series (series_name, host_country, match_type, start_date, total_matches) VALUES
('ICC World Cup 2024', 'India', 'ODI', '2024-10-01', 48);
```

---

### 5. MATCHES

**Purpose**: Store individual match details

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| match_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique match identifier |
| series_id | INT | FOREIGN KEY → series(series_id) | Parent series |
| match_description | VARCHAR(300) | | Match description |
| match_format | VARCHAR(50) | | Test/ODI/T20I/T20 |
| team1_id | INT | FOREIGN KEY → teams(team_id) | First team |
| team2_id | INT | FOREIGN KEY → teams(team_id) | Second team |
| venue_id | INT | FOREIGN KEY → venues(venue_id) | Match venue |
| match_date | DATE | | Match date |
| toss_winner_id | INT | FOREIGN KEY → teams(team_id) | Toss winner |
| toss_decision | VARCHAR(20) | | Bat/Bowl |
| winner_id | INT | FOREIGN KEY → teams(team_id) | Match winner |
| victory_margin | INT | | Margin of victory |
| victory_type | VARCHAR(20) | | runs/wickets |
| match_status | VARCHAR(50) | | Completed/Live/Upcoming |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

---

### 6. BATTING_STATS

**Purpose**: Store individual batting performances

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| stat_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique stat identifier |
| player_id | INT | FOREIGN KEY → players(player_id) | Player reference |
| match_id | INT | FOREIGN KEY → matches(match_id) | Match reference |
| innings_number | INT | | 1st or 2nd innings |
| runs_scored | INT | | Runs scored |
| balls_faced | INT | | Balls faced |
| fours | INT | | Number of fours |
| sixes | INT | | Number of sixes |
| strike_rate | DECIMAL(5,2) | | Strike rate |
| is_out | BOOLEAN | | Whether dismissed |
| dismissal_type | VARCHAR(50) | | How out |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

---

### 7. BOWLING_STATS

**Purpose**: Store individual bowling performances

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| stat_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique stat identifier |
| player_id | INT | FOREIGN KEY → players(player_id) | Player reference |
| match_id | INT | FOREIGN KEY → matches(match_id) | Match reference |
| innings_number | INT | | 1st or 2nd innings |
| overs_bowled | DECIMAL(4,1) | | Overs bowled |
| runs_conceded | INT | | Runs given |
| wickets_taken | INT | | Wickets taken |
| maidens | INT | | Maiden overs |
| economy_rate | DECIMAL(4,2) | | Economy rate |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

---

### 8. PLAYER_CAREER_STATS

**Purpose**: Store aggregated career statistics

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| career_stat_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique stat identifier |
| player_id | INT | FOREIGN KEY → players(player_id) | Player reference |
| match_format | VARCHAR(50) | | Test/ODI/T20I |
| total_matches | INT | DEFAULT 0 | Matches played |
| total_innings | INT | DEFAULT 0 | Innings batted |
| total_runs | INT | DEFAULT 0 | Career runs |
| batting_average | DECIMAL(6,2) | | Batting average |
| highest_score | INT | | Highest score |
| centuries | INT | DEFAULT 0 | 100+ scores |
| half_centuries | INT | DEFAULT 0 | 50+ scores |
| total_wickets | INT | DEFAULT 0 | Career wickets |
| bowling_average | DECIMAL(6,2) | | Bowling average |
| best_bowling | VARCHAR(20) | | Best figures |
| catches | INT | DEFAULT 0 | Catches taken |
| stumpings | INT | DEFAULT 0 | Stumpings done |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Last update time |

**Unique Constraint**: (player_id, match_format)

---

## 🔗 Relationships

### One-to-Many Relationships:

1. **teams → players**
   - One team has many players
   - `players.team_id` → `teams.team_id`

2. **teams → matches** (multiple relationships)
   - One team plays many matches
   - `matches.team1_id` → `teams.team_id`
   - `matches.team2_id` → `teams.team_id`
   - `matches.toss_winner_id` → `teams.team_id`
   - `matches.winner_id` → `teams.team_id`

3. **venues → matches**
   - One venue hosts many matches
   - `matches.venue_id` → `venues.venue_id`

4. **series → matches**
   - One series has many matches
   - `matches.series_id` → `series.series_id`

5. **players → player_career_stats**
   - One player has stats for multiple formats
   - `player_career_stats.player_id` → `players.player_id`

6. **matches → batting_stats**
   - One match has many batting performances
   - `batting_stats.match_id` → `matches.match_id`

7. **matches → bowling_stats**
   - One match has many bowling performances
   - `bowling_stats.match_id` → `matches.match_id`

8. **players → batting_stats**
   - One player has many batting performances
   - `batting_stats.player_id` → `players.player_id`

9. **players → bowling_stats**
   - One player has many bowling performances
   - `bowling_stats.player_id` → `players.player_id`

---

## 🔑 Indexes

### Primary Keys (Automatically Indexed):
- teams(team_id)
- venues(venue_id)
- players(player_id)
- series(series_id)
- matches(match_id)
- batting_stats(stat_id)
- bowling_stats(stat_id)
- player_career_stats(career_stat_id)

### Foreign Keys (Automatically Indexed):
- players(team_id)
- matches(series_id, team1_id, team2_id, venue_id, toss_winner_id, winner_id)
- batting_stats(player_id, match_id)
- bowling_stats(player_id, match_id)
- player_career_stats(player_id)

### Recommended Additional Indexes:
```sql
CREATE INDEX idx_player_country ON players(country);
CREATE INDEX idx_match_date ON matches(match_date);
CREATE INDEX idx_match_status ON matches(match_status);
CREATE INDEX idx_career_format ON player_career_stats(match_format);
```

---

## 📊 Sample Queries

### Get Player with Team:
```sql
SELECT p.player_name, t.team_name, p.playing_role
FROM players p
LEFT JOIN teams t ON p.team_id = t.team_id
WHERE p.country = 'India';
```

### Get Match Details:
```sql
SELECT 
    m.match_description,
    t1.team_name AS team1,
    t2.team_name AS team2,
    v.venue_name,
    tw.team_name AS winner
FROM matches m
LEFT JOIN teams t1 ON m.team1_id = t1.team_id
LEFT JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN venues v ON m.venue_id = v.venue_id
LEFT JOIN teams tw ON m.winner_id = tw.team_id;
```

### Get Player Career Stats:
```sql
SELECT 
    p.player_name,
    pcs.match_format,
    pcs.total_runs,
    pcs.batting_average,
    pcs.centuries
FROM player_career_stats pcs
JOIN players p ON pcs.player_id = p.player_id
WHERE pcs.match_format = 'ODI'
ORDER BY pcs.total_runs DESC;
```

---

## 🛡️ Data Integrity

### Foreign Key Constraints:
- **ON DELETE SET NULL**: When parent is deleted, FK is set to NULL
- **ON DELETE CASCADE**: When parent is deleted, child is also deleted

### Unique Constraints:
- teams.team_name (UNIQUE)
- player_career_stats(player_id, match_format) (UNIQUE)

### Default Values:
- All created_at fields default to CURRENT_TIMESTAMP
- Numeric stats default to 0
- updated_at auto-updates on modification

---

## 📈 Database Statistics

- **Total Tables**: 8
- **Total Columns**: ~90
- **Foreign Keys**: 12
- **Indexes**: 20+ (including auto-generated)
- **Relationships**: 9 one-to-many

---

**Database Schema Complete! 🎉**
