# 📚 SQL Queries Guide - 25 Practice Questions

Complete guide to all 25 SQL practice queries with explanations and expected outputs.

---

## 📘 BEGINNER LEVEL (Questions 1-8)

### Question 1: Find All Indian Players
**Difficulty**: ⭐ Easy  
**Concepts**: SELECT, WHERE

**Description**: Find all players who represent India. Display their full name, playing role, batting style, and bowling style.

**SQL Query**:
```sql
SELECT 
    player_name AS 'Full Name',
    playing_role AS 'Playing Role',
    batting_style AS 'Batting Style',
    bowling_style AS 'Bowling Style'
FROM players
WHERE country = 'India'
ORDER BY player_name;
```

**Learning Points**:
- Basic SELECT statement
- Column aliasing with AS
- WHERE clause for filtering
- ORDER BY for sorting

---

### Question 2: Recent Matches
**Difficulty**: ⭐⭐ Easy  
**Concepts**: SELECT, JOIN, WHERE, DATE functions

**Description**: Show all cricket matches played in the last 30 days.

**SQL Query**:
```sql
SELECT 
    m.match_description AS 'Match Description',
    t1.team_name AS 'Team 1',
    t2.team_name AS 'Team 2',
    CONCAT(v.venue_name, ', ', v.city) AS 'Venue',
    m.match_date AS 'Match Date'
FROM matches m
LEFT JOIN teams t1 ON m.team1_id = t1.team_id
LEFT JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY m.match_date DESC;
```

**Learning Points**:
- Multiple LEFT JOINs
- CONCAT function for string concatenation
- DATE_SUB for date calculations
- CURDATE() for current date

---

### Question 3: Top ODI Scorers
**Difficulty**: ⭐⭐ Easy  
**Concepts**: SELECT, JOIN, ORDER BY, LIMIT

**Description**: List top 10 highest run scorers in ODI cricket.

**SQL Query**:
```sql
SELECT 
    p.player_name AS 'Player Name',
    pcs.total_runs AS 'Total Runs',
    pcs.batting_average AS 'Batting Average',
    pcs.centuries AS 'Centuries'
FROM player_career_stats pcs
JOIN players p ON pcs.player_id = p.player_id
WHERE pcs.match_format = 'ODI'
ORDER BY pcs.total_runs DESC
LIMIT 10;
```

**Learning Points**:
- INNER JOIN vs LEFT JOIN
- Filtering by specific column value
- LIMIT clause for top N results

---

### Question 4: Large Venues
**Difficulty**: ⭐ Easy  
**Concepts**: SELECT, WHERE, ORDER BY

**Description**: Display venues with capacity > 50,000.

**SQL Query**:
```sql
SELECT 
    venue_name AS 'Venue Name',
    city AS 'City',
    country AS 'Country',
    capacity AS 'Capacity'
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;
```

**Learning Points**:
- Numeric comparison in WHERE
- Descending order with DESC

---

### Question 5: Team Wins
**Difficulty**: ⭐⭐ Easy  
**Concepts**: SELECT, JOIN, GROUP BY, COUNT

**Description**: Calculate how many matches each team has won.

**SQL Query**:
```sql
SELECT 
    t.team_name AS 'Team Name',
    COUNT(m.match_id) AS 'Total Wins'
FROM teams t
LEFT JOIN matches m ON t.team_id = m.winner_id
WHERE m.winner_id IS NOT NULL
GROUP BY t.team_id, t.team_name
ORDER BY COUNT(m.match_id) DESC;
```

**Learning Points**:
- COUNT aggregate function
- GROUP BY for aggregation
- NULL handling with IS NOT NULL

---

### Question 6: Players by Role
**Difficulty**: ⭐ Easy  
**Concepts**: SELECT, GROUP BY, COUNT

**Description**: Count players in each playing role.

**SQL Query**:
```sql
SELECT 
    playing_role AS 'Playing Role',
    COUNT(*) AS 'Number of Players'
FROM players
WHERE playing_role IS NOT NULL
GROUP BY playing_role
ORDER BY COUNT(*) DESC;
```

**Learning Points**:
- COUNT(*) vs COUNT(column)
- Simple GROUP BY

---

### Question 7: Highest Scores by Format
**Difficulty**: ⭐⭐ Easy  
**Concepts**: SELECT, GROUP BY, MAX

**Description**: Find highest individual batting score in each format.

**SQL Query**:
```sql
SELECT 
    pcs.match_format AS 'Format',
    MAX(pcs.highest_score) AS 'Highest Score'
FROM player_career_stats pcs
WHERE pcs.highest_score IS NOT NULL
GROUP BY pcs.match_format
ORDER BY MAX(pcs.highest_score) DESC;
```

**Learning Points**:
- MAX aggregate function
- GROUP BY with aggregates

---

### Question 8: Series in 2024
**Difficulty**: ⭐ Easy  
**Concepts**: SELECT, WHERE, YEAR function

**Description**: Show all series that started in 2024.

**SQL Query**:
```sql
SELECT 
    series_name AS 'Series Name',
    host_country AS 'Host Country',
    match_type AS 'Match Type',
    start_date AS 'Start Date',
    total_matches AS 'Total Matches'
FROM series
WHERE YEAR(start_date) = 2024
ORDER BY start_date;
```

**Learning Points**:
- YEAR() function for date extraction
- Date filtering

---

## 📗 INTERMEDIATE LEVEL (Questions 9-16)

### Question 9: All-rounders Performance
**Difficulty**: ⭐⭐⭐ Medium  
**Concepts**: SELECT, JOIN, WHERE with AND

**Description**: Find all-rounders with 1000+ runs AND 50+ wickets.

**Learning Points**:
- Multiple conditions with AND
- Filtering on multiple columns

---

### Question 10: Recent Completed Matches
**Difficulty**: ⭐⭐⭐ Medium  
**Concepts**: Multiple JOINs, WHERE, ORDER BY, LIMIT

**Description**: Get details of last 20 completed matches.

**Learning Points**:
- Complex multi-table JOINs
- Combining multiple conditions

---

### Question 11: Format Comparison
**Difficulty**: ⭐⭐⭐⭐ Medium-Hard  
**Concepts**: CASE, GROUP BY, HAVING, AVG

**Description**: Compare player performance across formats.

**Learning Points**:
- CASE statements for pivoting
- MAX with CASE for conditional aggregation
- HAVING clause for filtering groups

---

### Question 12: Home vs Away Performance
**Difficulty**: ⭐⭐⭐⭐ Medium-Hard  
**Concepts**: Complex JOINs, CASE, SUM

**Description**: Analyze team performance at home vs away.

**Learning Points**:
- Conditional aggregation with CASE
- Complex WHERE conditions

---

### Question 13: Batting Partnerships
**Difficulty**: ⭐⭐⭐⭐ Medium-Hard  
**Concepts**: Self JOIN, Multiple JOINs

**Description**: Find partnerships with 100+ combined runs.

**Learning Points**:
- Self-joining tables
- Combining data from same table

---

### Question 14: Bowling Venue Analysis
**Difficulty**: ⭐⭐⭐⭐ Medium-Hard  
**Concepts**: Multiple JOINs, GROUP BY, HAVING, AVG

**Description**: Bowling performance at different venues.

**Learning Points**:
- Complex aggregations
- HAVING with multiple conditions

---

### Question 15: Close Match Performers
**Difficulty**: ⭐⭐⭐⭐ Medium-Hard  
**Concepts**: Complex WHERE, OR conditions, CASE

**Description**: Players performing well in close matches.

**Learning Points**:
- OR conditions in WHERE
- Complex filtering logic

---

### Question 16: Performance Trends
**Difficulty**: ⭐⭐⭐⭐ Medium-Hard  
**Concepts**: YEAR function, GROUP BY multiple columns

**Description**: Track batting performance over years.

**Learning Points**:
- Time-based grouping
- Multi-column GROUP BY

---

## 📕 ADVANCED LEVEL (Questions 17-25)

### Question 17: Toss Advantage
**Difficulty**: ⭐⭐⭐⭐⭐ Hard  
**Concepts**: Percentage calculations, CASE, GROUP BY

**Description**: Analyze if winning toss gives advantage.

**Learning Points**:
- Percentage calculations in SQL
- Statistical analysis

---

### Question 18: Economical Bowlers
**Difficulty**: ⭐⭐⭐⭐⭐ Hard  
**Concepts**: Multiple JOINs, Complex HAVING

**Description**: Most economical bowlers in limited-overs.

**Learning Points**:
- Economy rate calculations
- Complex filtering conditions

---

### Question 19: Consistent Batsmen
**Difficulty**: ⭐⭐⭐⭐⭐ Hard  
**Concepts**: STDDEV, Statistical functions

**Description**: Find most consistent batsmen using standard deviation.

**Learning Points**:
- STDDEV function
- Statistical analysis in SQL

---

### Question 20: Format-wise Experience
**Difficulty**: ⭐⭐⭐⭐⭐ Hard  
**Concepts**: CASE with SUM, Complex pivoting

**Description**: Player experience across all formats.

**Learning Points**:
- Data pivoting with CASE
- Multiple conditional aggregations

---

### Question 21: Performance Ranking
**Difficulty**: ⭐⭐⭐⭐⭐ Very Hard  
**Concepts**: Complex calculations, COALESCE, NULLIF

**Description**: Comprehensive performance ranking system.

**Learning Points**:
- Complex mathematical formulas
- NULL handling with COALESCE
- Division by zero prevention with NULLIF

---

### Question 22: Head-to-Head Analysis
**Difficulty**: ⭐⭐⭐⭐⭐ Very Hard  
**Concepts**: Multiple JOINs, Complex aggregations

**Description**: Team head-to-head statistics.

**Learning Points**:
- Complex team comparisons
- Multiple conditional aggregations

---

### Question 23: Recent Form
**Difficulty**: ⭐⭐⭐⭐⭐ Very Hard  
**Concepts**: CTE (Common Table Expressions), ROW_NUMBER, Window Functions

**Description**: Analyze recent player form.

**Learning Points**:
- WITH clause for CTEs
- ROW_NUMBER() window function
- PARTITION BY

---

### Question 24: Best Partnerships
**Difficulty**: ⭐⭐⭐⭐⭐ Very Hard  
**Concepts**: CTE, Complex calculations

**Description**: Analyze successful batting partnerships.

**Learning Points**:
- CTEs for complex queries
- Partnership analysis

---

### Question 25: Career Trajectory
**Difficulty**: ⭐⭐⭐⭐⭐ Expert  
**Concepts**: Multiple CTEs, QUARTER function, Complex CASE

**Description**: Time-series career trajectory analysis.

**Learning Points**:
- Multiple CTEs
- Quarterly aggregations
- Trend analysis
- Complex categorization

---

## 🎯 Practice Tips

### For Beginners (Q1-Q8):
1. Start with Q1 and work sequentially
2. Understand each clause before moving on
3. Try modifying the queries (change country, limits, etc.)
4. Practice writing queries from scratch

### For Intermediate (Q9-Q16):
1. Draw the table relationships first
2. Break complex queries into smaller parts
3. Test each JOIN separately
4. Understand HAVING vs WHERE

### For Advanced (Q17-Q25):
1. Study CTEs and window functions
2. Practice on paper first
3. Build queries incrementally
4. Understand execution order

---

## 📊 Expected Output Formats

### Beginner Queries:
- Simple tabular results
- 5-50 rows typically
- Clear column names

### Intermediate Queries:
- More complex results
- May include calculated columns
- 10-100 rows typically

### Advanced Queries:
- Highly processed data
- Multiple calculated metrics
- Statistical insights
- Variable row counts

---

**Happy Querying! 📊🎓**
