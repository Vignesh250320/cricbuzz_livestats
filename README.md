# Cricbuzz LiveStats

Real-time cricket insights and SQL-based analytics using Streamlit, MySQL, and the Cricbuzz API.

## Features
- Real-time match data via Cricbuzz API (RapidAPI).
- Streamlit multi-page dashboard: Home, Live Matches, Top Stats, SQL Queries (25 queries), CRUD operations.
- Database-agnostic schema (MySQL used here).
- Full CRUD for player records.

## Setup (VS Code + MySQL)
1. Clone this repo into `cricbuzz_livestats/`.
2. Create a virtualenv and install dependencies:
python -m venv .venv
source .venv/bin/activate # linux/mac
.venv\Scripts\activate # windows
pip install -r requirements.txt
3. Create MySQL DB and user:
```sql
CREATE DATABASE cricbuzz_livestats;
CREATE USER 'cb_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON cricbuzz_livestats.* TO 'cb_user'@'localhost';
FLUSH PRIVILEGES;
