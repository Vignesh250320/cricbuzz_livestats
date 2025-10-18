# 🚀 Quick Setup Guide - Cricbuzz LiveStats

## Step-by-Step Setup Instructions

### 1️⃣ Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8+ installed
- ✅ MySQL Server 8.0+ installed
- ✅ RapidAPI account (free tier works)

### 2️⃣ MySQL Setup

#### Install MySQL (if not installed)
1. Download MySQL from: https://dev.mysql.com/downloads/mysql/
2. Run installer and set root password (remember this!)
3. Complete installation

#### Create Database
Open MySQL Command Line or MySQL Workbench and run:

```sql
CREATE DATABASE cricbuzz_db;
```

Verify it was created:
```sql
SHOW DATABASES;
```

### 3️⃣ Project Setup

#### Navigate to Project Directory
```bash
cd C:\Users\Vignesh\CascadeProjects\cricbuzz_livestats
```

#### Create Virtual Environment
```bash
python -m venv venv
```

#### Activate Virtual Environment
```bash
# Windows Command Prompt:
venv\Scripts\activate

# Windows PowerShell:
venv\Scripts\Activate.ps1

# If you get execution policy error in PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

You should see `(venv)` in your command prompt.

#### Install Dependencies
```bash
pip install -r requirements.txt
```

Wait for all packages to install (~2-3 minutes).

### 4️⃣ Environment Configuration

#### Create .env File
```bash
copy .env.example .env
```

#### Edit .env File
Open `.env` in any text editor and update:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD_HERE
DB_NAME=cricbuzz_db

# Cricbuzz API Configuration
RAPIDAPI_KEY=99106b078cmsh5ed6a042c14c9d9p156f6ejsnfd6a1979dccc
RAPIDAPI_HOST=cricbuzz-cricket.p.rapidapi.com
```

**Important**: Replace `YOUR_MYSQL_PASSWORD_HERE` with your actual MySQL root password!

### 5️⃣ Verify MySQL Connection

Test your MySQL connection:

```bash
mysql -u root -p
```

Enter your password. If successful, you'll see:
```
mysql>
```

Type `exit` to quit.

### 6️⃣ Run the Application

```bash
streamlit run app.py
```

The application will:
1. Initialize the database (creates all tables automatically)
2. Open in your browser at `http://localhost:8501`

### 7️⃣ Load Sample Data

Once the app is running:
1. Navigate to **🛠️ CRUD Operations** (sidebar)
2. Click on **📊 Sample Data** tab
3. Click **📥 Load Sample Data** button
4. Wait for confirmation message

This will populate your database with sample teams, players, and statistics.

### 8️⃣ Test SQL Queries

1. Navigate to **🔍 SQL Queries** (sidebar)
2. Try any of the 25 practice queries
3. Click **▶️ Execute** to run them
4. View results in the table

---

## 🔧 Common Issues & Solutions

### Issue 1: "Can't connect to MySQL server"
**Solution**:
- Ensure MySQL service is running
- Windows: Services → MySQL80 → Start
- Check password in `.env` file is correct

### Issue 2: "ModuleNotFoundError"
**Solution**:
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt` again

### Issue 3: "Access denied for user 'root'"
**Solution**:
- Double-check password in `.env` file
- Try resetting MySQL root password

### Issue 4: "Database 'cricbuzz_db' doesn't exist"
**Solution**:
- Open MySQL and run: `CREATE DATABASE cricbuzz_db;`

### Issue 5: API returns no data
**Solution**:
- Check internet connection
- Verify RapidAPI key is valid
- Some endpoints may require premium subscription

---

## 📋 Quick Command Reference

### Virtual Environment
```bash
# Activate
venv\Scripts\activate

# Deactivate
deactivate
```

### Run Application
```bash
streamlit run app.py
```

### MySQL Commands
```sql
-- Show databases
SHOW DATABASES;

-- Use database
USE cricbuzz_db;

-- Show tables
SHOW TABLES;

-- Count records
SELECT COUNT(*) FROM players;
```

### Install New Package
```bash
pip install package_name
pip freeze > requirements.txt
```

---

## 🎯 Next Steps After Setup

1. ✅ **Load Sample Data** (CRUD Operations → Sample Data)
2. ✅ **Practice SQL Queries** (SQL Queries → Try Q1-Q8)
3. ✅ **Add Your Own Players** (CRUD Operations → Create)
4. ✅ **Explore Live Matches** (Live Matches → Recent)
5. ✅ **View Top Stats** (Top Stats → Select Format)

---

## 📞 Need Help?

### Check These First:
1. Is MySQL running? (Check Services)
2. Is virtual environment activated? (See `(venv)` in prompt)
3. Is `.env` file configured correctly?
4. Did you create the database?

### Verify Installation:
```bash
# Check Python version
python --version

# Check pip
pip --version

# Check installed packages
pip list

# Check MySQL
mysql --version
```

---

## 🎓 Learning Path

### Week 1: Basics
- Set up the project
- Load sample data
- Practice beginner SQL queries (Q1-Q8)

### Week 2: Intermediate
- Add your own data via CRUD
- Practice intermediate queries (Q9-Q16)
- Explore API integration

### Week 3: Advanced
- Practice advanced queries (Q17-Q25)
- Write custom SQL queries
- Understand database relationships

### Week 4: Customization
- Add new features
- Create custom queries
- Enhance the dashboard

---

**Happy Learning! 🏏📊**
