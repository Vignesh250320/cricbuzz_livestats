"""
Database Setup Script
Run this to create the database from schema.sql
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("🏏 CRICBUZZ LIVESTATS - DATABASE SETUP")
print("=" * 60)

# Database credentials
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

print("\n📋 Configuration:")
print(f"   Host: {DB_HOST}")
print(f"   Port: {DB_PORT}")
print(f"   User: {DB_USER}")

# Connect to MySQL (without specifying database)
try:
    print("\n🔌 Connecting to MySQL server...")
    connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = connection.cursor()
    print("   ✅ Connected successfully!")
    
    # Read schema file
    schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    if not os.path.exists(schema_file):
        print(f"\n❌ Error: schema.sql not found at {schema_file}")
        exit(1)
    
    print(f"\n📄 Reading schema from: {schema_file}")
    
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # Split by delimiter changes and statements
    statements = []
    current_statement = ""
    current_delimiter = ";"
    
    for line in schema_sql.split('\n'):
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith('--'):
            continue
        
        # Check for delimiter change
        if line.startswith('DELIMITER'):
            parts = line.split()
            if len(parts) > 1:
                current_delimiter = parts[1]
            continue
        
        # Add line to current statement
        current_statement += line + " "
        
        # Check if statement is complete
        if current_delimiter in line:
            stmt = current_statement.replace(current_delimiter, "").strip()
            if stmt and not stmt.startswith('--'):
                statements.append(stmt)
            current_statement = ""
    
    # Execute statements
    print(f"\n🔨 Executing {len(statements)} SQL statements...")
    
    success_count = 0
    error_count = 0
    
    for i, statement in enumerate(statements, 1):
        try:
            # Skip OR REPLACE for MySQL versions that don't support it
            statement = statement.replace('CREATE OR REPLACE VIEW', 'CREATE VIEW')
            
            cursor.execute(statement)
            connection.commit()
            success_count += 1
            
            # Show progress for major operations
            if 'CREATE TABLE' in statement:
                table_name = statement.split('CREATE TABLE')[1].split('(')[0].strip()
                print(f"   ✅ Created table: {table_name}")
            elif 'CREATE VIEW' in statement:
                view_name = statement.split('CREATE VIEW')[1].split('AS')[0].strip()
                print(f"   ✅ Created view: {view_name}")
            elif 'CREATE PROCEDURE' in statement:
                proc_name = statement.split('CREATE PROCEDURE')[1].split('(')[0].strip()
                print(f"   ✅ Created procedure: {proc_name}")
            elif 'CREATE TRIGGER' in statement:
                trigger_name = statement.split('CREATE TRIGGER')[1].split()[0].strip()
                print(f"   ✅ Created trigger: {trigger_name}")
        
        except mysql.connector.Error as e:
            # Ignore "already exists" errors
            if 'already exists' not in str(e).lower() and 'duplicate' not in str(e).lower():
                error_count += 1
                print(f"   ⚠️ Error in statement {i}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ⚠️ Errors: {error_count}")
    
    # Verify database
    print("\n🔍 Verifying database...")
    cursor.execute("USE cricbuzz_livestats")
    
    # Check tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\n📋 Tables created ({len(tables)}):")
    for table in tables:
        print(f"   • {table[0]}")
    
    # Check views
    cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
    views = cursor.fetchall()
    if views:
        print(f"\n👁️ Views created ({len(views)}):")
        for view in views:
            print(f"   • {view[0]}")
    
    # Check procedures
    cursor.execute("SHOW PROCEDURE STATUS WHERE Db = 'cricbuzz_livestats'")
    procedures = cursor.fetchall()
    if procedures:
        print(f"\n⚙️ Procedures created ({len(procedures)}):")
        for proc in procedures:
            print(f"   • {proc[1]}")
    
    print("\n" + "=" * 60)
    print("✅ DATABASE SETUP COMPLETE!")
    print("=" * 60)
    print("\n📝 Next Steps:")
    print("   1. Update your .env file with database credentials")
    print("   2. Run: python test_env.py (to test connection)")
    print("   3. Run: streamlit run app.py (to start the app)")
    print("\n" + "=" * 60)

except mysql.connector.Error as e:
    print(f"\n❌ MySQL Error: {e}")
    print("\n💡 Troubleshooting:")
    print("   1. Check if MySQL server is running")
    print("   2. Verify credentials in .env file")
    print("   3. Ensure user has CREATE DATABASE privileges")
    exit(1)

except FileNotFoundError as e:
    print(f"\n❌ File Error: {e}")
    exit(1)

except Exception as e:
    print(f"\n❌ Unexpected Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
        print("\n🔌 Connection closed.")
