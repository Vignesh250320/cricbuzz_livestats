"""
Test Script for SQL Queries
This script runs all SQL queries and displays their results
"""

import pandas as pd
import traceback
from src.utils.db_connection import get_db_connection, DatabaseConnection
from src.features.sql_queries import SQLQueries

def run_query(query_func, query_name):
    """Run a single query and return results as a DataFrame"""
    db = None
    try:
        # Get the SQL query string
        query = query_func().strip()
        if not query:
            print("❌ Empty query string")
            return None
            
        print(f"\n{'='*80}")
        print(f"🔍 QUERY: {query_name}")
        print(f"{'='*80}")
        print(f"\n📜 SQL Query:")
        print(query)
        
        # Create a new database connection
        db = DatabaseConnection()
        conn = db.connect()
        if not conn:
            print("❌ Failed to connect to database")
            return None
            
        cursor = conn.cursor(dictionary=True)
        
        # Execute the query
        cursor.execute(query)
        
        # Get column names
        columns = [i[0] for i in cursor.description] if cursor.description else []
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        if not rows:
            print("\nℹ️  No results returned.")
            # Return empty DataFrame with columns if available
            return pd.DataFrame(columns=columns) if columns else None
            
        df = pd.DataFrame(rows, columns=columns)
        print(f"\n✅ Rows returned: {len(df)}")
        if not df.empty:
            print("\n📊 First 5 rows:")
            print(df.head().to_string())
        return df
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nStack trace:")
        traceback.print_exc()
        return None
        
    finally:
        if db:
            db.close()

def extract_query_number(method_name):
    """Extract query number from method name (e.g., 'query_1_indian_players' -> 1)"""
    try:
        # Extract the number after 'query_'
        num_str = method_name.split('_')[1]
        return int(num_str)
    except (IndexError, ValueError):
        # If can't extract number, return a large number to put these at the end
        return 9999

def main():
    # Get all query methods from SQLQueries class
    query_methods = []
    for method in dir(SQLQueries):
        if method.startswith('query_'):
            # Get a friendly name for display
            friendly_name = ' '.join(part.capitalize() for part in method.split('_')[1:])
            query_methods.append((getattr(SQLQueries, method), friendly_name, method))
    
    # Sort by query number
    query_methods.sort(key=lambda x: extract_query_number(x[2]))
    
    # Run each query
    all_results = {}
    for query_func, friendly_name, method_name in query_methods:
        print(f"\n\n{'*'*50}")
        print(f"Testing: {method_name} - {friendly_name}")
        print(f"{'*'*50}")
        df = run_query(query_func, friendly_name)
        if df is not None and not df.empty:
            all_results[friendly_name] = df
    
    # Save results to Excel for review
    if all_results:
        try:
            output_file = 'query_results.xlsx'
            with pd.ExcelWriter(output_file) as writer:
                for name, df in all_results.items():
                    # Clean sheet name (Excel has restrictions)
                    sheet_name = ''.join(c if c.isalnum() or c in ' _-' else '_' for c in name)[:31]
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"\n\n📂 All results saved to '{output_file}'")
        except Exception as e:
            print(f"\n❌ Error saving to Excel: {str(e)}")

if __name__ == "__main__":
    main()
