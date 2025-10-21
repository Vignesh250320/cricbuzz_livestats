# pages/home.py
import streamlit as st

def app():
    st.header("Project Overview")
    st.markdown("""
**Cricbuzz LiveStats** is a Streamlit multi-page application that:
- Fetches real-time cricket data from Cricbuzz's API (via RapidAPI)
- Stores match and player stats in a MySQL database
- Provides 25 built-in SQL analytics queries (Beginner/Intermediate/Advanced)
- Allows full CRUD on player records via forms

**Tech stack**
- Python, Streamlit, SQL (MySQL via SQLAlchemy), JSON, REST API

**Folder structure**
cricbuzz_livestats/
├── app.py
├── pages/
├── utils/
└── notebooks/
                """)

    st.subheader("Setup Quick Checklist")
    st.markdown("""
1. Create a MySQL database named `cricbuzz_livestats`.
2. Add `.env` with DB and API keys.
3. Run `schema.sql` to create tables and `sample_data.sql` to insert sample rows.
4. Install requirements: `pip install -r requirements.txt`.
5. Run app: `streamlit run app.py`.
""")
