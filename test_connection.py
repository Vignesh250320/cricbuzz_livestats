import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("MySQL Connection Diagnostic Tool")
print("=" * 60)

# Show configuration
print("\n📋 Configuration:")
print(f"  Host: {os.getenv('DB_HOST', '127.0.0.1')}")
print(f"  User: {os.getenv('DB_USER', 'root')}")
print(f"  Database: {os.getenv('DB_NAME', 'cricbuzz_db')}")
print(f"  Port: {os.getenv('DB_PORT', '3306')}")

# Test 1: Connect without database
print("\n🔍 Test 1: Connecting to MySQL server (no database)...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'vicky@123'),
        port=3306,
        connection_timeout=10
    )
    print("✅ SUCCESS: Connected to MySQL server!")
    
    # Check if database exists
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES LIKE 'cricbuzz_db'")
    result = cursor.fetchone()
    
    if result:
        print("✅ Database 'cricbuzz_db' exists")
    else:
        print("❌ Database 'cricbuzz_db' does NOT exist")
        print("\n💡 Creating database...")
        cursor.execute("CREATE DATABASE cricbuzz_db")
        print("✅ Database created successfully!")
    
    cursor.close()
    conn.close()
    
except Error as e:
    print(f"❌ FAILED: {e}")
    print("\n🔧 Troubleshooting steps:")
    print("  1. Check if MySQL service is running")
    print("  2. Verify your password in .env file")
    print("  3. Try: net start MySQL80")

# Test 2: Connect with database
print("\n🔍 Test 2: Connecting to cricbuzz_db database...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'vicky@123'),
        database='cricbuzz_db',
        port=3306,
        connection_timeout=10
    )
    print("✅ SUCCESS: Connected to cricbuzz_db!")
    
    # Check tables
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    if tables:
        print(f"✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")
    else:
        print("⚠️  No tables found. Run database_setup.py to create tables.")
    
    cursor.close()
    conn.close()
    
except Error as e:
    print(f"❌ FAILED: {e}")

print("\n" + "=" * 60)
print("Diagnostic complete!")
print("=" * 60)
