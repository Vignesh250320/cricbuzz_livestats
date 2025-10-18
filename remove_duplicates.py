"""
Remove duplicate player records from the database
Keeps only the oldest record for each player name
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("REMOVING DUPLICATE PLAYERS")
print("=" * 70)

try:
    # Connect to database
    conn = mysql.connector.connect(
        host='localhost',
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'vicky@123'),
        database=os.getenv('DB_NAME', 'cricbuzz_db'),
        autocommit=False
    )
    
    cursor = conn.cursor()
    
    # Check current player count
    cursor.execute("SELECT COUNT(*) FROM players")
    before_count = cursor.fetchone()[0]
    print(f"\n📊 Players before cleanup: {before_count}")
    
    # Find duplicates
    cursor.execute("""
        SELECT player_name, COUNT(*) as count
        FROM players
        GROUP BY player_name
        HAVING count > 1
        ORDER BY count DESC
    """)
    
    duplicates = cursor.fetchall()
    
    if duplicates:
        print(f"\n🔍 Found {len(duplicates)} duplicate player names:")
        for name, count in duplicates:
            print(f"   - {name}: {count} records")
        
        # Remove duplicates - keep only the oldest record (lowest player_id)
        print("\n🗑️  Removing duplicates...")
        
        cursor.execute("""
            DELETE p1 FROM players p1
            INNER JOIN players p2 
            WHERE p1.player_name = p2.player_name 
            AND p1.player_id > p2.player_id
        """)
        
        deleted_count = cursor.rowcount
        print(f"✅ Deleted {deleted_count} duplicate records")
        
        # Commit the changes
        conn.commit()
        print("✅ Changes committed to database")
        
    else:
        print("\n✅ No duplicates found!")
    
    # Check final count
    cursor.execute("SELECT COUNT(*) FROM players")
    after_count = cursor.fetchone()[0]
    print(f"\n📊 Players after cleanup: {after_count}")
    
    # Show remaining players
    print("\n📋 Current players in database:")
    cursor.execute("""
        SELECT player_id, player_name, country, playing_role 
        FROM players 
        ORDER BY player_id
    """)
    
    players = cursor.fetchall()
    for pid, name, country, role in players:
        print(f"   {pid:2d}. {name:20s} | {country:12s} | {role or 'N/A'}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ CLEANUP COMPLETE!")
    print("=" * 70)
    print("\nRefresh your Streamlit app to see the updated data.")
    
except Error as e:
    print(f"\n❌ Error: {e}")
    if conn:
        conn.rollback()
        print("⚠️  Changes rolled back")
