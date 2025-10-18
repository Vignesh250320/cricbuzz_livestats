"""
Test MySQL connection in the same way Streamlit does
This helps diagnose why test_connection.py works but Streamlit doesn't
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables exactly like app.py
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

print("=" * 70)
print("STREAMLIT-STYLE CONNECTION TEST")
print("=" * 70)

print(f"\n📁 Project root: {project_root}")
print(f"📄 .env path: {env_path}")
print(f"📋 .env exists: {os.path.exists(env_path)}")

print("\n🔍 Environment Variables:")
print(f"  DB_HOST: {os.getenv('DB_HOST', 'NOT SET')}")
print(f"  DB_USER: {os.getenv('DB_USER', 'NOT SET')}")
print(f"  DB_NAME: {os.getenv('DB_NAME', 'NOT SET')}")
print(f"  DB_PORT: {os.getenv('DB_PORT', 'NOT SET')}")

# Test with multiple hosts like the updated app.py
hosts_to_try = ['localhost', '127.0.0.1']

for i, host in enumerate(hosts_to_try, 1):
    print(f"\n🔍 Test {i}: Trying host '{host}'...")
    try:
        conn = mysql.connector.connect(
            host=host,
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'vicky@123'),
            database=os.getenv('DB_NAME', 'cricbuzz_db'),
            port=int(os.getenv('DB_PORT', 3306)),
            connection_timeout=10,
            autocommit=True,
            charset='utf8mb4',
            use_unicode=True
        )
        
        if conn.is_connected():
            print(f"✅ SUCCESS with host '{host}'!")
            
            # Test a query
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM teams")
            count = cursor.fetchone()[0]
            print(f"✅ Query test: Found {count} teams in database")
            
            cursor.close()
            conn.close()
            print(f"\n🎉 Connection successful! Use host='{host}' in your app")
            break
    except Error as e:
        print(f"❌ FAILED with host '{host}': {e}")
        if host == hosts_to_try[-1]:
            print("\n⚠️  All connection attempts failed!")
            print("\n🔧 Troubleshooting:")
            print("  1. Check MySQL service: sc query MySQL80")
            print("  2. Restart MySQL: net stop MySQL80 && net start MySQL80")
            print("  3. Check MySQL is listening: netstat -an | findstr :3306")
            print("  4. Verify password in .env matches MySQL root password")

print("\n" + "=" * 70)
