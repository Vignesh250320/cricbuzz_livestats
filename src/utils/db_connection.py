"""
Database Connection Utility
Centralized MySQL database connection management
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
# Look for .env in the project root directory (two levels up from src/utils)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

# Debug: Print environment variables being used
print(f"Loading environment from: {env_path}")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")
# Don't print password for security


class DatabaseConnection:
    """Manages MySQL database connections"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', 'vicky@123')
        self.database = os.getenv('DB_NAME', 'cricbuzz_db')
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            st.error(f"Database connection error: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None, fetch=True):
        """
        Execute SQL query
        
        Args:
            query: SQL query string
            params: Query parameters (optional)
            fetch: Whether to fetch results (default True)
        
        Returns:
            Query results or None
        """
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params or ())
                
                if fetch:
                    result = cursor.fetchall()
                    cursor.close()
                    self.close()
                    return result
                else:
                    connection.commit()
                    cursor.close()
                    self.close()
                    return True
        except Error as e:
            st.error(f"Query execution error: {e}")
            return None
    
    def execute_many(self, query, data):
        """
        Execute multiple queries (batch insert/update)
        
        Args:
            query: SQL query string
            data: List of tuples containing data
        
        Returns:
            True if successful, False otherwise
        """
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()
                cursor.executemany(query, data)
                connection.commit()
                cursor.close()
                self.close()
                return True
        except Error as e:
            st.error(f"Batch execution error: {e}")
            return False


def get_db_connection():
    """Helper function to get database connection instance"""
    return DatabaseConnection()


def initialize_database():
    """Create database and tables if they don't exist"""
    try:
        # Connect without database to create it
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME', 'cricbuzz_db')}")
        cursor.execute(f"USE {os.getenv('DB_NAME', 'cricbuzz_db')}")
        
        # Create tables
        create_tables_queries = [
            """
            CREATE TABLE IF NOT EXISTS teams (
                team_id INT PRIMARY KEY AUTO_INCREMENT,
                team_name VARCHAR(100) NOT NULL UNIQUE,
                country VARCHAR(100),
                team_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS venues (
                venue_id INT PRIMARY KEY AUTO_INCREMENT,
                venue_name VARCHAR(200) NOT NULL,
                city VARCHAR(100),
                country VARCHAR(100),
                capacity INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS players (
                player_id INT PRIMARY KEY AUTO_INCREMENT,
                player_name VARCHAR(100) NOT NULL,
                team_id INT,
                country VARCHAR(100),
                playing_role VARCHAR(50),
                batting_style VARCHAR(50),
                bowling_style VARCHAR(50),
                date_of_birth DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS series (
                series_id INT PRIMARY KEY AUTO_INCREMENT,
                series_name VARCHAR(200) NOT NULL,
                host_country VARCHAR(100),
                match_type VARCHAR(50),
                start_date DATE,
                end_date DATE,
                total_matches INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS matches (
                match_id INT PRIMARY KEY AUTO_INCREMENT,
                series_id INT,
                match_description VARCHAR(300),
                match_format VARCHAR(50),
                team1_id INT,
                team2_id INT,
                venue_id INT,
                match_date DATE,
                toss_winner_id INT,
                toss_decision VARCHAR(20),
                winner_id INT,
                victory_margin INT,
                victory_type VARCHAR(20),
                match_status VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (series_id) REFERENCES series(series_id) ON DELETE SET NULL,
                FOREIGN KEY (team1_id) REFERENCES teams(team_id) ON DELETE SET NULL,
                FOREIGN KEY (team2_id) REFERENCES teams(team_id) ON DELETE SET NULL,
                FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE SET NULL,
                FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id) ON DELETE SET NULL,
                FOREIGN KEY (winner_id) REFERENCES teams(team_id) ON DELETE SET NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS batting_stats (
                stat_id INT PRIMARY KEY AUTO_INCREMENT,
                player_id INT,
                match_id INT,
                innings_number INT,
                runs_scored INT,
                balls_faced INT,
                fours INT,
                sixes INT,
                strike_rate DECIMAL(5,2),
                is_out BOOLEAN,
                dismissal_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
                FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS bowling_stats (
                stat_id INT PRIMARY KEY AUTO_INCREMENT,
                player_id INT,
                match_id INT,
                innings_number INT,
                overs_bowled DECIMAL(4,1),
                runs_conceded INT,
                wickets_taken INT,
                maidens INT,
                economy_rate DECIMAL(4,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
                FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS player_career_stats (
                career_stat_id INT PRIMARY KEY AUTO_INCREMENT,
                player_id INT,
                match_format VARCHAR(50),
                total_matches INT DEFAULT 0,
                total_innings INT DEFAULT 0,
                total_runs INT DEFAULT 0,
                batting_average DECIMAL(6,2),
                highest_score INT,
                centuries INT DEFAULT 0,
                half_centuries INT DEFAULT 0,
                total_wickets INT DEFAULT 0,
                bowling_average DECIMAL(6,2),
                best_bowling VARCHAR(20),
                catches INT DEFAULT 0,
                stumpings INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
                UNIQUE KEY unique_player_format (player_id, match_format)
            )
            """
        ]
        
        for query in create_tables_queries:
            cursor.execute(query)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return True
    except Error as e:
        st.error(f"Database initialization error: {e}")
        return False
