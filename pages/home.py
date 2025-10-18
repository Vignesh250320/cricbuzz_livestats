"""
Home Page - Project Overview and Navigation
"""

import streamlit as st


def show():
    """Display home page"""
    
    # Header
    st.title("🏏 Cricbuzz LiveStats")
    st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")
    
    # Introduction
    st.markdown("""
    Welcome to **Cricbuzz LiveStats** - A comprehensive cricket analytics dashboard that combines 
    real-time data from the Cricbuzz API with powerful SQL-driven analytics.
    """)
    
    # Features
    st.markdown("---")
    st.header("✨ Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Live Match Updates
        - Real-time match scores
        - Detailed scorecards
        - Player performance tracking
        - Match status and updates
        
        ### 🎯 Top Player Statistics
        - Batting leaders
        - Bowling leaders
        - All-rounder rankings
        - Format-wise statistics
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 SQL Analytics
        - 25+ practice queries
        - Beginner to Advanced levels
        - Interactive query execution
        - Custom SQL interface
        
        ### 🛠️ CRUD Operations
        - Add new players
        - Update player stats
        - Delete records
        - Full database management
        """)
    
    # Technology Stack
    st.markdown("---")
    st.header("🚀 Technology Stack")
    
    tech_col1, tech_col2, tech_col3 = st.columns(3)
    
    with tech_col1:
        st.markdown("""
        **Backend**
        - Python 3.x
        - MySQL Database
        - REST API Integration
        """)
    
    with tech_col2:
        st.markdown("""
        **Frontend**
        - Streamlit
        - Pandas
        - Plotly
        """)
    
    with tech_col3:
        st.markdown("""
        **Data Source**
        - Cricbuzz API
        - RapidAPI Platform
        - Real-time Updates
        """)
    
    # Business Use Cases
    st.markdown("---")
    st.header("💼 Business Use Cases")
    
    use_cases = {
        "📺 Sports Media & Broadcasting": [
            "Real-time match updates for commentary teams",
            "Player performance analysis for pre-match discussions",
            "Historical data trends for match predictions"
        ],
        "🎮 Fantasy Cricket Platforms": [
            "Player form analysis and recent performance tracking",
            "Head-to-head statistics for team selection",
            "Real-time score updates for fantasy leagues"
        ],
        "📈 Cricket Analytics Firms": [
            "Advanced statistical modeling and player evaluation",
            "Performance trend analysis across different formats",
            "Data-driven insights for team management"
        ],
        "🎓 Educational Institutions": [
            "Teaching database operations with real-world data",
            "SQL practice with engaging cricket datasets",
            "API integration and web development learning"
        ]
    }
    
    for use_case, points in use_cases.items():
        with st.expander(use_case):
            for point in points:
                st.markdown(f"- {point}")
    
    # Project Structure
    st.markdown("---")
    st.header("📁 Project Structure")
    
    st.code("""
cricbuzz_livestats/
│── app.py                    # Streamlit entry point
│── requirements.txt          # Dependencies
│── README.md                 # Documentation
│── .env                      # Environment variables
│
├── pages/                    # Streamlit multipage
│   ├── home.py              # Overview page
│   ├── live_matches.py      # Live match updates
│   ├── top_stats.py         # Player statistics
│   ├── sql_queries.py       # SQL analytics
│   └── crud_operations.py   # CRUD operations
│
├── utils/                    # Utility modules
│   ├── db_connection.py     # Database connection
│   ├── api_helper.py        # API integration
│   └── sql_queries.py       # SQL query collection
│
└── notebooks/               # Jupyter notebooks
    └── data_fetching.ipynb  # API testing
    """, language="text")
    
    # Getting Started
    st.markdown("---")
    st.header("🎯 Getting Started")
    
    st.markdown("""
    ### Setup Instructions
    
    1. **Clone the repository**
       ```bash
       git clone <repository-url>
       cd cricbuzz_livestats
       ```
    
    2. **Create virtual environment**
       ```bash
       python -m venv venv
       venv\\Scripts\\activate  # Windows
       source venv/bin/activate  # Linux/Mac
       ```
    
    3. **Install dependencies**
       ```bash
       pip install -r requirements.txt
       ```
    
    4. **Configure environment variables**
       - Copy `.env.example` to `.env`
       - Update database credentials
       - Add your RapidAPI key
    
    5. **Initialize database**
       - Create MySQL database
       - Run the application (tables will be created automatically)
    
    6. **Run the application**
       ```bash
       streamlit run app.py
       ```
    """)
    
    # Navigation Guide
    st.markdown("---")
    st.header("🧭 Navigation Guide")
    
    nav_col1, nav_col2 = st.columns(2)
    
    with nav_col1:
        st.info("""
        **📱 Live Matches**  
        View ongoing cricket matches with real-time scores and detailed scorecards.
        """)
        
        st.info("""
        **📊 Top Stats**  
        Explore top batting and bowling statistics from the Cricbuzz API.
        """)
    
    with nav_col2:
        st.info("""
        **🔍 SQL Queries**  
        Practice 25+ SQL queries ranging from beginner to advanced levels.
        """)
        
        st.info("""
        **🛠️ CRUD Operations**  
        Manage player data with full Create, Read, Update, Delete functionality.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using Python, Streamlit, and MySQL</p>
        <p>Data powered by Cricbuzz API via RapidAPI</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show()
