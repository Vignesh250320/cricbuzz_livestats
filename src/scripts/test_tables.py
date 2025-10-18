from ..utils.db_connection import DatabaseConnection

def test_tables():
    db = DatabaseConnection()
    try:
        # Test connection
        conn = db.connect()
        if conn and conn.is_connected():
            print("✅ Successfully connected to the database")
            
            # Get cursor
            cursor = conn.cursor(dictionary=True)
            
            # Test query - list all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("\nTables in the database:")
            for table in tables:
                print(f"- {table['Tables_in_cricbuzz_db']}")
            
            # If you have a players table, try to fetch some data
            cursor.execute("SELECT * FROM players LIMIT 5")
            players = cursor.fetchall()
            if players:
                print("\nSample players:")
                for player in players:
                    print(f"ID: {player['player_id']}, Name: {player['player_name']}")
            else:
                print("\nNo players found in the database")
            
            cursor.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if db.connection:
            db.close()

if __name__ == "__main__":
    test_tables()