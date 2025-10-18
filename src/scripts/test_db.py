"""
Database Test Script
Test database connection and run a simple query
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

def test_connection():
    """Test database connection and run a simple query"""
    try:
        # Load environment variables
        project_root = os.path.abspath(os.path.dirname(__file__))
        env_path = os.path.join(project_root, '.env')
        load_dotenv(env_path)
        
        print("Testing database connection...")
        print(f"Host: {os.getenv('DB_HOST')}")
        print(f"User: {os.getenv('DB_USER')}")
        print(f"Database: {os.getenv('DB_NAME')}")
        
        # Connect to MySQL
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            # Test query - get count of players
            cursor.execute("SELECT COUNT(*) as count FROM players")
            result = cursor.fetchone()
            print(f"\n✅ Successfully connected to database!")
            print(f"Number of players in database: {result['count']}")
            
            # Get first 5 players
            print("\nFirst 5 players:")
            cursor.execute("SELECT player_id, player_name, country FROM players LIMIT 5")
            for row in cursor:
                print(f"ID: {row['player_id']}, Name: {row['player_name']}, Country: {row['country']}")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_connection()
