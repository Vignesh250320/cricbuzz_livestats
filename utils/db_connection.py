import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from contextlib import contextmanager
import streamlit as st

# Load environment variables
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

@contextmanager
def get_connection():
    """Context-managed MySQL connection."""
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn
    except Error as e:
        st.error(f"❌ Database connection failed: {e}")
        yield None
    finally:
        if conn and conn.is_connected():
            conn.close()

def run_query(query: str, params=None):
    """Execute SELECT queries and return results as list of dicts."""
    with get_connection() as conn:
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as e:
            st.error(f"⚠️ SQL Error: {e}")
            return []
        finally:
            cursor.close()

def execute_sql(query: str, params=None):
    """Execute INSERT, UPDATE, DELETE statements."""
    with get_connection() as conn:
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            st.success("✅ Query executed successfully.")
        except Error as e:
            st.error(f"❌ Error executing query: {e}")
            conn.rollback()
        finally:
            cursor.close()
