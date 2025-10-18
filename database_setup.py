import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import sys

def print_header(message):
    """Print a formatted header"""
    print("\n" + "="*50)
    print(f" {message.upper()} ")
    print("="*50)

def create_connection(use_database=True):
    """Create a database connection"""
    try:
        # Load environment variables
        project_root = os.path.abspath(os.path.dirname(__file__))
        env_path = os.path.join(project_root, '.env')
        load_dotenv(env_path)
        
        # Get database credentials
        host = os.getenv('DB_HOST', '127.0.0.1')
        # Convert localhost to 127.0.0.1 for better compatibility
        if host == 'localhost':
            host = '127.0.0.1'
            
        db_config = {
            'host': host,
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'vicky@123'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'connection_timeout': 10
        }
        
        if use_database:
            db_config['database'] = os.getenv('DB_NAME', 'cricbuzz_db')
        
        # Print connection details
        print("\nConnecting to MySQL with:")
        for key, value in db_config.items():
            if key != 'password':  # Don't print password
                print(f"  {key}: {value}")
        
        conn = mysql.connector.connect(**db_config)
        print("✅ Connection successful!")
        return conn
        
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        if "Access denied" in str(e):
            print("\nPossible solutions:")
            print("1. Check if the MySQL password is correct")
            print("2. Verify the MySQL user has proper permissions")
        elif "Can't connect" in str(e):
            print("\nPossible solutions:")
            print("1. Make sure MySQL server is running")
            print("2. Check if the host and port are correct")
            print("3. Verify your firewall allows connections to MySQL")
        return None

def create_database(conn, db_name):
    """Create a database if it doesn't exist"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ Database '{db_name}' created successfully")
        return True
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_tables(conn):
    """Create all required tables"""
    tables = {
        'teams': """
            CREATE TABLE IF NOT EXISTS teams (
                team_id INT AUTO_INCREMENT PRIMARY KEY,
                team_name VARCHAR(100) NOT NULL UNIQUE,
                short_name VARCHAR(10),
                logo_url VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        'players': """
            CREATE TABLE IF NOT EXISTS players (
                player_id INT AUTO_INCREMENT PRIMARY KEY,
                player_name VARCHAR(100) NOT NULL,
                team_id INT,
                batting_style VARCHAR(50),
                bowling_style VARCHAR(50),
                date_of_birth DATE,
                country VARCHAR(50),
                profile_image_url VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        'venues': """
            CREATE TABLE IF NOT EXISTS venues (
                venue_id INT AUTO_INCREMENT PRIMARY KEY,
                venue_name VARCHAR(100) NOT NULL,
                city VARCHAR(100),
                country VARCHAR(100),
                capacity INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        'matches': """
            CREATE TABLE IF NOT EXISTS matches (
                match_id INT AUTO_INCREMENT PRIMARY KEY,
                team1_id INT,
                team2_id INT,
                venue_id INT,
                match_date DATETIME,
                match_type ENUM('T20', 'ODI', 'Test', 'IPL', 'Other') DEFAULT 'T20',
                toss_winner_id INT,
                toss_decision ENUM('bat', 'field'),
                winner_id INT,
                player_of_match_id INT,
                match_result VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (team1_id) REFERENCES teams(team_id) ON DELETE SET NULL,
                FOREIGN KEY (team2_id) REFERENCES teams(team_id) ON DELETE SET NULL,
                FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE SET NULL,
                FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id) ON DELETE SET NULL,
                FOREIGN KEY (winner_id) REFERENCES teams(team_id) ON DELETE SET NULL,
                FOREIGN KEY (player_of_match_id) REFERENCES players(player_id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    }
    
    cursor = conn.cursor()
    
    try:
        for table_name, create_query in tables.items():
            try:
                cursor.execute(create_query)
                print(f"✅ Table '{table_name}' created successfully")
            except Error as e:
                print(f"❌ Error creating table '{table_name}': {e}")
                return False
        return True
    except Error as e:
        print(f"❌ Error creating tables: {e}")
        return False
    finally:
        cursor.close()

def insert_sample_data(conn):
    """Insert sample data into the database"""
    try:
        cursor = conn.cursor()
        
        # Sample teams
        teams = [
            ("Mumbai Indians", "MI", "https://example.com/mi.png"),
            ("Chennai Super Kings", "CSK", "https://example.com/csk.png"),
            ("Royal Challengers Bangalore", "RCB", "https://example.com/rcb.png"),
            ("Kolkata Knight Riders", "KKR", "https://example.com/kkr.png"),
            ("Delhi Capitals", "DC", "https://example.com/dc.png")
        ]
        
        cursor.executemany("""
            INSERT IGNORE INTO teams (team_name, short_name, logo_url)
            VALUES (%s, %s, %s)
        """, teams)
        
        # Sample venues
        venues = [
            ("Wankhede Stadium", "Mumbai", "India", 33500),
            ("M. A. Chidambaram Stadium", "Chennai", "India", 50000),
            ("M. Chinnaswamy Stadium", "Bengaluru", "India", 40000),
            ("Eden Gardens", "Kolkata", "India", 68000),
            ("Arun Jaitley Stadium", "Delhi", "India", 41820)
        ]
        
        cursor.executemany("""
            INSERT IGNORE INTO venues (venue_name, city, country, capacity)
            VALUES (%s, %s, %s, %s)
        """, venues)
        
        # Get team IDs
        cursor.execute("SELECT team_id, team_name FROM teams")
        team_map = {name: tid for tid, name in cursor.fetchall()}
        
        # Sample players
        players = [
            ("Rohit Sharma", team_map["Mumbai Indians"], "Right-handed", "Right-arm offbreak", "1987-04-30", "India"),
            ("MS Dhoni", team_map["Chennai Super Kings"], "Right-handed", "Right-arm medium", "1981-07-07", "India"),
            ("Virat Kohli", team_map["Royal Challengers Bangalore"], "Right-handed", "Right-arm medium", "1988-11-05", "India"),
            ("Shreyas Iyer", team_map["Kolkata Knight Riders"], "Right-handed", "Legbreak", "1994-12-06", "India"),
            ("Rishabh Pant", team_map["Delhi Capitals"], "Left-handed", "N/A", "1997-10-04", "India")
        ]
        
        cursor.executemany("""
            INSERT IGNORE INTO players (player_name, team_id, batting_style, bowling_style, date_of_birth, country)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, players)
        
        # Get venue IDs
        cursor.execute("SELECT venue_id, venue_name FROM venues")
        venue_map = {name: vid for vid, name in cursor.fetchall()}
        
        # Sample matches
        matches = [
            (team_map["Mumbai Indians"], team_map["Chennai Super Kings"], 
             venue_map["Wankhede Stadium"], "2023-04-10 19:30:00", "IPL", 
             team_map["Mumbai Indians"], "bat", team_map["Mumbai Indians"], None, "Mumbai Indians won by 5 wickets"),
             
            (team_map["Chennai Super Kings"], team_map["Royal Challengers Bangalore"], 
             venue_map["M. A. Chidambaram Stadium"], "2023-04-12 19:30:00", "IPL",
             team_map["Chennai Super Kings"], "field", team_map["Chennai Super Kings"], None, "Chennai Super Kings won by 8 wickets"),
             
            (team_map["Kolkata Knight Riders"], team_map["Delhi Capitals"],
             venue_map["Eden Gardens"], "2023-04-15 15:30:00", "IPL",
             team_map["Kolkata Knight Riders"], "bat", None, None, "Match tied")
        ]
        
        cursor.executemany("""
            INSERT INTO matches 
            (team1_id, team2_id, venue_id, match_date, match_type, 
             toss_winner_id, toss_decision, winner_id, player_of_match_id, match_result)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, matches)
        
        # Get player IDs for player of the match
        cursor.execute("SELECT player_id, player_name FROM players")
        player_map = {name: pid for pid, name in cursor.fetchall()}
        
        # Update player of the match
        update_queries = [
            (player_map["Rohit Sharma"], 1),  # Match 1
            (player_map["MS Dhoni"], 2),      # Match 2
        ]
        
        cursor.executemany("""
            UPDATE matches SET player_of_match_id = %s WHERE match_id = %s
        """, update_queries)
        
        conn.commit()
        print("\n✅ Sample data inserted successfully!")
        return True
        
    except Error as e:
        conn.rollback()
        print(f"❌ Error inserting sample data: {e}")
        print(f"Error details: {e}")
        return False
    finally:
        cursor.close()

def verify_data(conn):
    """Verify the data in the database"""
    try:
        cursor = conn.cursor(dictionary=True)
        
        print("\nVerifying data...")
        
        # Count records in each table
        tables = ['teams', 'players', 'venues', 'matches']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            result = cursor.fetchone()
            print(f"📊 {table.capitalize()}: {result['count']} records")
        
        # Show sample data
        print("\nSample Teams:")
        cursor.execute("SELECT team_id, team_name, short_name FROM teams LIMIT 5")
        for row in cursor.fetchall():
            print(f"  {row['team_id']}: {row['team_name']} ({row['short_name']})")
        
        print("\nSample Players:")
        cursor.execute("""
            SELECT p.player_id, p.player_name, t.team_name 
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.team_id
            LIMIT 5
        """)
        for row in cursor.fetchall():
            print(f"  {row['player_id']}: {row['player_name']} ({row['team_name'] or 'No team'})")
        
        print("\nUpcoming Matches:")
        cursor.execute("""
            SELECT m.match_id, 
                   t1.team_name as team1, 
                   t2.team_name as team2,
                   v.venue_name,
                   m.match_date,
                   m.match_result
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            LEFT JOIN venues v ON m.venue_id = v.venue_id
            ORDER BY m.match_date DESC
            LIMIT 3
        """)
        for row in cursor.fetchall():
            print(f"\n  {row['team1']} vs {row['team2']}")
            print(f"  At: {row['venue_name']}")
            print(f"  When: {row['match_date']}")
            print(f"  Result: {row['match_result'] or 'Match not started yet'}")
        
        print("\n✅ Data verification complete!")
        return True
        
    except Error as e:
        print(f"❌ Error verifying data: {e}")
        return False
    finally:
        cursor.close()

def main():
    print_header("Cricket Database Setup")
    
    # Get database name from environment or use default
    db_name = os.getenv('DB_NAME', 'cricbuzz_db')
    
    # Step 1: Connect to MySQL server (without specifying a database)
    print("\nStep 1: Connecting to MySQL server...")
    conn = create_connection(use_database=False)
    if conn is None:
        print("❌ Failed to connect to MySQL server. Exiting...")
        sys.exit(1)
    
    try:
        # Step 2: Create database
        print("\nStep 2: Creating database...")
        if not create_database(conn, db_name):
            print("❌ Failed to create database. Exiting...")
            sys.exit(1)
        
        # Close the initial connection
        conn.close()
        
        # Step 3: Reconnect to the specific database
        print("\nStep 3: Connecting to the database...")
        conn = create_connection(use_database=True)
        if conn is None:
            print("❌ Failed to connect to the database. Exiting...")
            sys.exit(1)
        
        # Step 4: Create tables
        print("\nStep 4: Creating tables...")
        if not create_tables(conn):
            print("❌ Failed to create tables. Exiting...")
            sys.exit(1)
        
        # Step 5: Insert sample data
        print("\nStep 5: Inserting sample data...")
        insert_sample = input("\nDo you want to insert sample data? (y/n): ").strip().lower()
        if insert_sample == 'y':
            if not insert_sample_data(conn):
                print("⚠️ Some errors occurred while inserting sample data")
        
        # Step 6: Verify data
        print("\nStep 6: Verifying data...")
        if not verify_data(conn):
            print("⚠️ Some issues were found during data verification")
        
        print("\n" + "="*50)
        print("✅ Database setup completed successfully!")
        print("="*50)
        print("\nYou can now run the Streamlit app with:")
        print("  streamlit run app.py")
        
    except Error as e:
        print(f"\n❌ An error occurred: {e}")
        if conn.is_connected():
            conn.rollback()
    finally:
        if conn.is_connected():
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()