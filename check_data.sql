-- Check what data we have in the database

USE cricbuzz_db;

-- Check players and their roles
SELECT '=== PLAYERS ===' as Info;
SELECT player_id, player_name, playing_role FROM players;

-- Check career stats
SELECT '=== CAREER STATS ===' as Info;
SELECT 
    p.player_name,
    pcs.match_format,
    pcs.total_runs,
    pcs.total_wickets,
    p.playing_role
FROM player_career_stats pcs
JOIN players p ON pcs.player_id = p.player_id
ORDER BY p.player_name, pcs.match_format;

-- Check matches
SELECT '=== MATCHES ===' as Info;
SELECT 
    match_id,
    match_description,
    victory_margin,
    victory_type,
    match_date
FROM matches
ORDER BY match_date DESC;

-- Check close matches
SELECT '=== CLOSE MATCHES ===' as Info;
SELECT 
    match_id,
    match_description,
    victory_margin,
    victory_type
FROM matches
WHERE (victory_type = 'runs' AND victory_margin < 50)
   OR (victory_type = 'wickets' AND victory_margin < 5);

-- Check batting stats count
SELECT '=== BATTING STATS COUNT ===' as Info;
SELECT COUNT(*) as total_batting_stats FROM batting_stats;

-- Check batting stats by player
SELECT '=== BATTING STATS BY PLAYER ===' as Info;
SELECT 
    p.player_name,
    COUNT(bs.stat_id) as innings_count
FROM batting_stats bs
JOIN players p ON bs.player_id = p.player_id
GROUP BY p.player_id, p.player_name;
