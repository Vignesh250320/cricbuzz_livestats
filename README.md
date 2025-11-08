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
│   ├── setup_complete.py       # ⭐ ONE-COMMAND setup script
│   ├── schema.sql              # Complete database schema
│   ├── insert_sample_data.py   # Sample cricket data
│   ├── add_partnership_data.py # Partnership batting data
│   └── DATABASE.md             # Database documentation
│
└── notebooks/
    └── data_fetching.ipynb     # API testing + DB population notebook
```

### Database Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `setup_complete.py` | ⭐ **Use this!** Sets up everything in one command | First time setup |
| `schema.sql` | Database schema (tables, views, triggers) | Manual setup or reference |
| `insert_sample_data.py` | Sample cricket data | Add more test data |
| `add_partnership_data.py` | Partnership batting records | Add partnership data |
| `DATABASE.md` | Complete schema documentation | Reference and learning |

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

#### Quick Setup (Recommended) ⭐
Run this **ONE command** to set up everything:
```bash
python database/setup_complete.py
```

This will automatically:
- ✅ Create all tables, views, triggers, and procedures
- ✅ Insert sample data (teams, players, venues, matches)
- ✅ Add batting and bowling performance data
- ✅ Create partnerships for testing

#### Manual Setup (Advanced)
If you prefer step-by-step control:

```bash
# 1. Login to MySQL
mysql -u root -p

# 2. Create database and user
CREATE DATABASE cricbuzz_livestats;
CREATE USER 'cb_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON cricbuzz_livestats.* TO 'cb_user'@'localhost';
FLUSH PRIVILEGES;
USE cricbuzz_livestats;

# 3. Run schema
SOURCE database/schema.sql;
```

Then manually run the data scripts:
```bash
python database/insert_sample_data.py
python database/add_partnership_data.py
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

### 5️⃣ Run the Application
```bash
streamlit run app.py
```
Visit `http://localhost:8501` in your browser

---

## 🔄 Adding More Data

The setup script includes sample data, but you can add real cricket data:

**Option 1: Use Data Ingestion Page** (Recommended)
1. Open the app: `http://localhost:8501`
2. Go to **📥 Data Ingestion** page
3. Select data source (Matches, Players, etc.)
4. Click **Fetch Data** to preview
5. Click **Insert into Database**

**Option 2: Manual Scripts**
```bash
# Add more sample data
python database/insert_sample_data.py

# Add partnership data
python database/add_partnership_data.py
```


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




