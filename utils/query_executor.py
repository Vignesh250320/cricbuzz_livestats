from utils.db_connection import run_query, execute_sql
import streamlit as st

def run_sql_query(query: str):
    """Safely execute a read-only SQL query."""
    if not query.strip().lower().startswith("select"):
        st.warning("Only SELECT queries are allowed here.")
        return []
    return run_query(query)

def run_admin_query(query: str, params=None):
    """Execute admin-level queries (for inserts/updates/deletes)."""
    execute_sql(query, params)
