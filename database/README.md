# 🗄️ Database Setup

## Quick Setup (Recommended)

Run this **ONE command** to set up everything:

```bash
python database/setup_complete.py
```

This will:
1. ✅ Create all tables, views, triggers, and procedures
2. ✅ Insert sample data (teams, players, venues, matches)
3. ✅ Add batting and bowling performance data
4. ✅ Create partnerships for testing

---

## Manual Setup (Advanced)

If you prefer step-by-step:

### 1. Create Schema
```bash
mysql -u cb_user -p cricbuzz_livestats < database/schema.sql
```

### 2. Add Sample Data
```bash
python database/insert_sample_data.py
```

### 3. Add Partnership Data
```bash
python database/add_partnership_data.py
```

---

## Files

| File | Description |
|------|-------------|
| `setup_complete.py` | **⭐ Use this!** Complete automated setup |
| `schema.sql` | Database schema (tables, views, triggers) |
| `insert_sample_data.py` | Sample cricket data |
| `add_partnership_data.py` | Partnership batting data |
| `DATABASE.md` | Complete documentation |

---

## Requirements

Before running setup:

1. MySQL 8.x installed and running
2. Database created:
   ```sql
   CREATE DATABASE cricbuzz_livestats;
   ```
3. User created with permissions:
   ```sql
   CREATE USER 'cb_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON cricbuzz_livestats.* TO 'cb_user'@'localhost';
   ```
4. `.env` file configured with credentials

---

## Verify Setup

After running setup, check:

```python
# Should show:
Players: 10
Teams: 5
Matches: 5
Batting records: 55+
Bowling records: 25+
```

---

## Need More Data?

Use the **Data Ingestion page** in the app:
1. Run: `streamlit run app.py`
2. Go to: 📥 Data Ingestion
3. Fetch data from Cricbuzz API
4. Insert into database

---

**Ready to go!** 🚀
