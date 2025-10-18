"""
Database Verification Script
Checks if database and tables exist and contain data
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file in project root"""
    # Go up two levels from the current script's directory to reach project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    env_path = os.path.join(project_root, '.env')
    load_dotenv(env_path)
    
    # Print environment info (except password)
    print(f"\n{'='*50}")
    print("DATABASE CONNECTION INFO:")
    print("="*50)
    print(f"Host: {os.getenv('DB_HOST')}")
    print(f"User: {os.getenv('DB_USER')}")
    print(f"Database: {os.getenv('DB_NAME')}")
    print(f"Environment file: {env_path}")
    print("="*50 + "\n")

def check_database_connection():
    """Check if database connection is successful"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Get database version
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
            print(f"✅ Connected to MySQL Server version: {db_version[0]}")
            
            # List all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if not tables:
                print("\n❌ No tables found in the database.")
                return False
                
            print("\n📋 Found tables:")
            for table in tables:
                table_name = table[0]
                print(f"\nTable: {table_name}")
                print("-" * (len(table_name) + 8))
                
                # Get table structure
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                print("\nColumns:")
                for col in columns:
                    print(f"  - {col[0]} ({col[1]})")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"\n  Rows: {count}")
                
                # Show first few rows if table has data
                if count > 0:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                    rows = cursor.fetchall()
                    print("\n  Sample data:")
                    for row in rows:
                        print(f"    {row}")
            
            cursor.close()
            conn.close()
            return True
            
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        
        # If database doesn't exist, try to connect without database
        if "Unknown database" in str(e):
            print("\nAttempting to connect without database to check server...")
            try:
                conn = mysql.connector.connect(
                    host=os.getenv('DB_HOST'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD')
                )
                if conn.is_connected():
                    cursor = conn.cursor()
                    cursor.execute("SHOW DATABASES")
                    dbs = cursor.fetchall()
                    print("\nAvailable databases:")
                    for db in dbs:
                        print(f"- {db[0]}")
                    cursor.close()
                    conn.close()
            except Error as e:
                print(f"Error: {e}")
                
        return False

if __name__ == "__main__":
    load_environment()
    check_database_connection()
