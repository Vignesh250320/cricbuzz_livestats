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

### 📥 Data Ingestion Page
- Fetch and populate data from Cricbuzz API into your database
- Preview data before inserting
- Automatically handles Teams, Venues, Series, and Matches
- One-click data population for testing

### 🧠 SQL Queries & Analytics Page
- Contains **25 SQL analytical queries** (Beginner → Advanced)  
- All queries optimized for MySQL ONLY_FULL_GROUP_BY mode
- Executes queries directly on the MySQL cricket database  
- Interactive UI for exploring insights with downloadable results
- Includes partnership analysis and advanced statistics

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
│   ├── data_ingestion.py       # Fetch & populate data from API
│   ├── sql_queries.py          # 25 SQL analytical queries
│   └── crud_operations.py      # CRUD operations for players/teams
│
├── utils/
│   ├── api_handler.py          # Cricbuzz API functions (30+ endpoints)
│   ├── db_connection.py        # Central DB connection handler
│   └── query_executor.py       # SQL query execution utilities
│
├── database/
│   ├── schema.sql              # Complete database schema
│   ├── insert_sample_data.py   # Sample cricket data
│   ├── add_partnership_data.py # Partnership batting data
│   ├── setup_database.py       # Automated setup script
│   └── DATABASE.md             # Database documentation
│
└── notebooks/
    └── data_fetching.ipynb     # API testing + DB population notebook
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Vignesh250320/cricbuzz_livestats.git
cd cricbuzz_livestats
```

### 2️⃣ Install Requirements
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up MySQL Database
```bash
# Login to MySQL
mysql -u root -p

# Create database and user
CREATE DATABASE cricbuzz_livestats;
CREATE USER 'cb_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON cricbuzz_livestats.* TO 'cb_user'@'localhost';
FLUSH PRIVILEGES;
USE cricbuzz_livestats;

# Run schema
SOURCE database/schema.sql;
```

### 4️⃣ Configure Environment Variables
Create a file named `.env` in the project root:
```env
RAPIDAPI_KEY=your_rapidapi_key_here
RAPIDAPI_HOST=cricbuzz-cricket.p.rapidapi.com
DB_HOST=localhost
DB_USER=cb_user
DB_PASSWORD=your_password
DB_NAME=cricbuzz_livestats
```

### 5️⃣ Populate Sample Data (Optional)
```bash
python database/insert_sample_data.py
python database/add_partnership_data.py
```

### 6️⃣ Run the Application
```bash
streamlit run app.py
```
Visit `http://localhost:8501` in your browser


---

## 🧠 SQL Practice Queries

This project includes **25 SQL practice problems** in `pages/sql_queries.py`:

### Query Difficulty Levels:
- **Beginner (1–8)**: Basic SELECT, WHERE, ORDER BY
- **Intermediate (9–16)**: JOINs, GROUP BY, Aggregations, CTEs
- **Advanced (17–25)**: Complex analytics, partnerships, statistics

### Highlights:
- ✅ All queries optimized for MySQL `ONLY_FULL_GROUP_BY` mode
- ✅ Partnership analysis (queries 13, 24)
- ✅ Performance metrics and trends
- ✅ Interactive execution with downloadable results

Each query runs interactively within Streamlit and displays results instantly.

---

## 🛠️ Technologies Used

| Category | Tools |
|----------|-------|
| **Frontend** | Streamlit |
| **Backend** | Python 3.13 |
| **Database** | MySQL 8.x |
| **API Source** | Cricbuzz (via RapidAPI) |
| **Libraries** | pandas, requests, mysql-connector-python, python-dotenv |

---

## 📦 Deliverables

- ✅ Streamlit web app with 6 pages
- ✅ Complete MySQL schema with views, triggers, and stored procedures
- ✅ 25+ SQL analytical queries (all working, no errors)
- ✅ Data ingestion system from Cricbuzz API
- ✅ CRUD functionality for database operations
- ✅ Live matches and top stats pages
- ✅ Comprehensive documentation

---

## 📸 Screenshots

### SQL Analytics Page
Run 25 practice queries with instant results and CSV download.

### Data Ingestion Page
Fetch and populate data from Cricbuzz API with one click.

### Live Matches Page
Real-time cricket match data from Cricbuzz.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Vignesh**
- GitHub: [@Vignesh250320](https://github.com/Vignesh250320)
- Project: [cricbuzz_livestats](https://github.com/Vignesh250320/cricbuzz_livestats)

---

## 🙏 Acknowledgments

- **Cricbuzz** for providing cricket data via RapidAPI
- **Streamlit** for the amazing web framework
- **MySQL** for robust database management

---

Made with ❤️ for Cricket Enthusiasts and Data Analysts 🏏




