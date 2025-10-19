# 🏏 Cricbuzz LiveStats Dashboard

A real-time cricket statistics dashboard powered by Cricbuzz API, built with Python and Streamlit.

## ✨ Features

- 📡 **Real-time Data** - Live cricket data from Cricbuzz API
- 👥 **Player Stats** - Rankings, career statistics, and performance metrics
- 🏏 **Match Updates** - Recent matches, live scores, and upcoming fixtures
- 📊 **Team Analytics** - Team performance and historical data
- 🔍 **SQL Queries** - Practice SQL with 25 pre-built queries
- 🗄️ **Database Management** - View and manage cricket data

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Create a `.env` file with your MySQL credentials:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=cricbuzz_db
DB_PORT=3306
```

### 3. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
cricbuzz_livestats/
├── app.py                  # Main entry point for the Streamlit app
├── requirements.txt        # Required Python packages
├── README.md              # Project overview and setup instructions
│
├── pages/                 # Contains individual Streamlit pages
│   ├── home.py           # Overview and About the Project page
│   ├── live_matches.py   # Displays live match data from Cricbuzz API
│   ├── top_stats.py      # Shows top batting/bowling stats
│   ├── sql_queries.py    # SQL query interface and analytics
│   └── crud_operations.py # Perform CRUD on player stats
│
├── utils/                 # Utility files
│   └── db_connection.py  # SQL database connection logic
│
└── notebooks/            # Practice Jupyter notebooks (Optional)
    └── data_fetching.ipynb # For testing API calls and pushing to DB
```

## 🔄 Updating Data

Use the **"Database Management"** page in the Streamlit app and click **"Refresh from API"** to fetch latest cricket data.

## 📊 Database Tables

- **teams** - Cricket teams
- **players** - Player profiles and details
- **venues** - Cricket stadiums
- **series** - Cricket series/tournaments
- **matches** - Match information
- **batting_stats** - Batting performance
- **bowling_stats** - Bowling performance
- **player_career_stats** - Career statistics

## 🛠️ Technologies Used

- **Python 3.8+**
- **Streamlit** - Web framework
- **MySQL** - Database
- **Pandas** - Data manipulation
- **Plotly** - Data visualization
- **Cricbuzz API** - Cricket data source

## 🔧 Troubleshooting

### Database Connection Issues
1. Ensure MySQL is running
2. Verify credentials in `.env` file
3. Check if database `cricbuzz_db` exists

### API Issues
1. Check your internet connection
2. Verify API configuration in the app
3. Check API rate limits (100 requests/day on free tier)

## 📝 License

This project is for educational purposes.

---

**Made with ❤️ for cricket enthusiasts**


