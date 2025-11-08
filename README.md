# 🏏 Cricbuzz LiveStats — Cricket Analytics Dashboard

## 📘 Overview
**Cricbuzz LiveStats** is a **Streamlit-based cricket analytics dashboard** that integrates **live match data** and **player statistics** from the **Cricbuzz API**, along with an internal **MySQL database** for analytics and SQL practice.  
It’s designed for both **cricket enthusiasts** and **data learners** who want to explore cricket stats, perform CRUD operations, and run SQL queries — all in one app.

---

## 🚀 Features

### 🏠 Home Page
- Overview of the project, technology stack, and navigation links  
- Displays documentation and folder structure  

### 🏏 Live Matches Page
- Fetches **live, upcoming, and recent matches** from Cricbuzz API  
- Displays scorecards, match status, venue info, and series details  
- Real-time updates with 60-second cache for live matches  

### 📊 Top Stats & Rankings Page
- Shows **top batting and bowling statistics** (most runs, wickets, etc.)  
- **ICC Rankings** for batsmen, bowlers, all-rounders, and teams  
- Filter by format (Test, ODI, T20) and stat type  
- Interactive charts and visual representation  

### 🧠 SQL Queries & Analytics Page
- Contains **25 SQL analytical queries** (Beginner → Advanced)  
- Executes queries directly on the MySQL cricket database  
- Interactive UI for exploring insights with downloadable results  

### 🛠️ CRUD Operations Page
- Perform **Create, Read, Update, Delete** on database tables  
- Useful for learning database operations visually  
- Supports players, teams, venues, and series  

---

## 🧩 Project Structure
```
cricbuzz_livestats/
│── app.py                     # Streamlit entry point
│── requirements.txt            # Dependencies
│── README.md                   # Project overview & setup guide
│
├── pages/                      # Streamlit multi-page setup
│   ├── home.py                 # Overview/dashboard
│   ├── live_matches.py         # Live, recent, upcoming matches (API)
│   ├── top_stats.py            # ICC rankings, most runs/wickets (API)
│   ├── sql_queries.py          # 25 SQL analytical queries
│   └── crud_operations.py      # CRUD operations for players/teams
│
├── utils/
│   ├── api_handler.py          # Cricbuzz API functions (30+ endpoints)
│   ├── db_connection.py        # Central DB connection handler
│   └── query_executor.py       # SQL query execution utilities
│
└── notebooks/
    └── data_fetching.ipynb     # API testing + DB population notebook
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/cricbuzz_livestats.git
cd cricbuzz_livestats

2️⃣ Install Requirements
pip install -r requirements.txt

3️⃣ Set Up MySQL Database
Run the following in your MySQL terminal:
CREATE DATABASE cricbuzz_db;
USE cricbuzz_db;
-- Run your SQL table creation and sample data script here

4️⃣ Configure Environment Variables
Create a file named .env in the project root:
RAPIDAPI_KEY=your_rapidapi_key_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=cricbuzz_db

5️⃣ Run the Application
streamlit run app.py


🧠 SQL Practice Queries
This project includes 25 SQL practice problems in pages/sql_queries.py


Beginner: 1–8


Intermediate: 9–16


Advanced: 17–25
Each query runs interactively within Streamlit and displays results instantly.



🛠️ Technologies Used
CategoryToolsFrontendStreamlitBackendPythonDatabaseMySQLAPI SourceCricbuzz (via RapidAPI)Librariespandas, requests, mysql-connector-python, plotly

📦 Deliverables


✅ Streamlit web app (app.py)


✅ MySQL schema & data


✅ .env config for secure API keys


✅ 25+ SQL query scripts


✅ CRUD functionality


✅ Live & top stats pages


✅ Documentation and setup guide




