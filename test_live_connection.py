"""
Test MySQL connection while Streamlit is running
This simulates exactly what Streamlit does
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

print("=" * 70)
print("TESTING CONNECTION WHILE STREAMLIT IS RUNNING")
print("=" * 70)

# Test multiple times to check consistency
for attempt in range(1, 6):
    print(f"\n🔍 Attempt {attempt}/5:")
    try:
        start = time.time()
        conn = mysql.connector.connect(
            host='localhost',
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'vicky@123'),
            database=os.getenv('DB_NAME', 'cricbuzz_db'),
            port=int(os.getenv('DB_PORT', 3306)),
            connection_timeout=10,
            autocommit=True,
            charset='utf8mb4',
            use_unicode=True
        )
        
        elapsed = time.time() - start
        
        if conn.is_connected():
            print(f"   ✅ Connected in {elapsed:.2f}s")
            
            # Test a query
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM matches")
            count = cursor.fetchone()[0]
            print(f"   ✅ Query works: {count} matches found")
            
            cursor.close()
            conn.close()
        else:
            print(f"   ❌ Connection object created but not connected")
            
    except Error as e:
        print(f"   ❌ FAILED: {e}")
        print(f"   Error code: {e.errno if hasattr(e, 'errno') else 'N/A'}")
    
    if attempt < 5:
        time.sleep(1)

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)

# Check for connection limits
print("\n🔍 Checking MySQL connection status:")
try:
    conn = mysql.connector.connect(
        host='localhost',
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'vicky@123'),
        database=os.getenv('DB_NAME', 'cricbuzz_db')
    )
    cursor = conn.cursor()
    cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
    result = cursor.fetchone()
    print(f"   Active connections: {result[1]}")
    
    cursor.execute("SHOW VARIABLES LIKE 'max_connections'")
    result = cursor.fetchone()
    print(f"   Max connections: {result[1]}")
    
    cursor.close()
    conn.close()
except Error as e:
    print(f"   ❌ Could not check: {e}")
