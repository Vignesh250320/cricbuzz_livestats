# utils/db_connection.py

import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_engine():
    """
    Create and return a SQLAlchemy engine for MySQL database connection.
    Automatically encodes special characters in the password.
    Returns None if connection fails.
    """
    try:
        # Load DB credentials from .env
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME")

        # Safely encode password to handle @, #, etc.
        password_encoded = quote_plus(password)

        # Build SQLAlchemy connection URL
        connection_string = (
            f"mysql+pymysql://{user}:{password_encoded}@{host}:{port}/{db_name}"
        )

        # Create engine
        engine = create_engine(connection_string, echo=False, pool_pre_ping=True)

        # Test the connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Database connected successfully!")

        return engine

    except SQLAlchemyError as e:
        print(f"❌ Database connection error: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        return None


def get_connection():
    """
    Return an active connection object.
    You can use this in CRUD operations or SQL analytics pages.
    Example:
        conn = get_connection()
        result = conn.execute(text("SELECT * FROM Players"))
    """
    engine = get_engine()
    if engine:
        return engine.connect()
    return None


def close_connection(conn):
    """Safely close an open SQLAlchemy connection"""
    try:
        if conn:
            conn.close()
            print("🔒 Connection closed.")
    except Exception as e:
        print(f"⚠️ Error closing connection: {e}")


def run_query(query, params=None):
    """
    Execute a SQL SELECT query safely and return results as a list of rows.
    - query: SQL string (use named parameters like :team)
    - params: dictionary of parameters, e.g. {"team": "India"}

    Returns:
        List of rows, or [] if error occurs.
    """
    conn = get_connection()
    if not conn:
        print("⚠️ Could not establish database connection.")
        return []

    try:
        result = conn.execute(text(query), params or {})
        rows = result.fetchall()
        return rows
    except SQLAlchemyError as e:
        print(f"❌ SQL Error: {e}")
        return []
    finally:
        close_connection(conn)


def execute_statement(query, params=None):
    """
    Execute an INSERT, UPDATE, or DELETE SQL statement.
    Commits changes automatically and closes the connection.
    Returns True if successful, False otherwise.
    """
    conn = get_connection()
    if not conn:
        print("⚠️ Could not establish database connection.")
        return False

    try:
        conn.execute(text(query), params or {})
        conn.commit()  # commit changes
        print("✅ Statement executed successfully.")
        return True
    except SQLAlchemyError as e:
        print(f"❌ SQL Execution Error: {e}")
        return False
    finally:
        close_connection(conn)
