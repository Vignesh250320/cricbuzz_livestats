"""
Add comprehensive batting data to create partnerships for queries 13 & 24
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "cb_user"),
    password=os.getenv("DB_PASSWORD", "vicky@123"),
    database=os.getenv("DB_NAME", "cricbuzz_livestats")
)
cursor = conn.cursor()

print("Adding partnership batting data...")

# Get existing match and player IDs
cursor.execute("SELECT match_id FROM Matches LIMIT 5")
match_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT player_id FROM Players ORDER BY player_id LIMIT 10")
player_ids = [row[0] for row in cursor.fetchall()]

if not match_ids or not player_ids:
    print("⚠️ Need matches and players first! Run insert_sample_data.py")
    exit(1)

# Clear existing batting data to avoid duplicates
cursor.execute("DELETE FROM Batting_Performance")
conn.commit()
print("✅ Cleared old batting data")

# Create comprehensive batting data for each match
batting_data = []
innings_counter = 1

for match_idx, match_id in enumerate(match_ids):
    # Each match has 2 innings (team1 and team2)
    for innings_num in range(1, 3):
        innings_id = innings_counter
        innings_counter += 1
        
        # Each innings has 5-6 batsmen (enough for partnerships)
        batsmen_count = 6 if innings_num == 1 else 5
        
        for pos in range(1, batsmen_count + 1):
            # Assign players cyclically
            player_idx = (match_idx * 6 + innings_num * 3 + pos - 1) % len(player_ids)
            player_id = player_ids[player_idx]
            
            # Realistic runs distribution
            if pos == 1:  # Opener
                runs = 45 + (match_idx * 10)
            elif pos == 2:  # Opener partner
                runs = 55 + (match_idx * 8)
            elif pos == 3:  # Number 3
                runs = 38 + (match_idx * 12)
            elif pos == 4:  # Middle order
                runs = 42 + (match_idx * 7)
            elif pos == 5:
                runs = 28 + (match_idx * 5)
            else:
                runs = 20 + (match_idx * 3)
            
            # Calculate balls and strike rate
            balls = int(runs * 1.5) + 10
            strike_rate = (runs / balls * 100) if balls > 0 else 0
            fours = runs // 6
            sixes = runs // 15
            
            batting_data.append((
                player_id,
                match_id,
                innings_id,
                runs,
                balls,
                fours,
                sixes,
                round(strike_rate, 2),
                pos
            ))

# Insert all batting data
insert_sql = """
INSERT INTO Batting_Performance 
(player_id, match_id, innings_id, runs, balls_faced, fours, sixes, strike_rate, batting_position)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(insert_sql, batting_data)
conn.commit()

print(f"✅ Inserted {len(batting_data)} batting records")

# Verify partnerships
cursor.execute("""
    SELECT COUNT(*) FROM Batting_Performance bp1
    JOIN Batting_Performance bp2 
    ON bp1.innings_id = bp2.innings_id 
    AND bp1.batting_position + 1 = bp2.batting_position
    WHERE (bp1.runs + bp2.runs) >= 50
""")
partnerships = cursor.fetchone()[0]
print(f"✅ Created {partnerships} partnerships with 50+ runs")

cursor.execute("""
    SELECT COUNT(*) FROM Batting_Performance bp1
    JOIN Batting_Performance bp2 
    ON bp1.innings_id = bp2.innings_id 
    AND bp1.batting_position + 1 = bp2.batting_position
    WHERE (bp1.runs + bp2.runs) >= 100
""")
big_partnerships = cursor.fetchone()[0]
print(f"✅ Created {big_partnerships} partnerships with 100+ runs")

# Show sample partnership
cursor.execute("""
    SELECT p1.full_name, bp1.runs, p2.full_name, bp2.runs, (bp1.runs + bp2.runs) as total
    FROM Batting_Performance bp1
    JOIN Batting_Performance bp2 ON bp1.innings_id = bp2.innings_id AND bp1.batting_position + 1 = bp2.batting_position
    JOIN Players p1 ON bp1.player_id = p1.player_id
    JOIN Players p2 ON bp2.player_id = p2.player_id
    ORDER BY total DESC
    LIMIT 3
""")

print("\n🏏 Top 3 Partnerships:")
for row in cursor.fetchall():
    print(f"  {row[0]} ({row[1]}) + {row[2]} ({row[3]}) = {row[4]} runs")

cursor.close()
conn.close()

print("\n🎉 Partnership data added! Now Query 13 & 24 will work!")
