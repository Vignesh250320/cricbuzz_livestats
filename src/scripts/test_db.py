import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        print("Testing database connection...")
        
        # Direct connection parameters
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="vicky@123",  # Replace with your MySQL password
            database="cricbuzz_db"  # Replace with your database name
        )
        
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database")
            
            # Test query
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()
            print("\nAvailable databases:")
            for db in databases:
                print(f"- {db['Database']}")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_connection()