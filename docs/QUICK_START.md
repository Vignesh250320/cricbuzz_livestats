# ⚡ Quick Start - Get Running in 5 Minutes!

## 🎯 Goal
Get the Cricbuzz LiveStats app running on your computer in 5 minutes.

---

## ✅ Prerequisites (2 minutes)

### 1. Check Python
```bash
python --version
```
✅ Should show Python 3.8 or higher  
❌ If not installed: Download from https://www.python.org/

### 2. Check MySQL
```bash
mysql --version
```
✅ Should show MySQL 8.0 or higher  
❌ If not installed: Download from https://dev.mysql.com/downloads/mysql/

---

## 🚀 Setup (3 minutes)

### Step 1: Navigate to Project (10 seconds)
```bash
cd C:\Users\Vignesh\CascadeProjects\cricbuzz_livestats
```

### Step 2: Run Setup Script (2 minutes)
```bash
setup.bat
```

This will:
- Create virtual environment
- Install all dependencies
- Create .env file

### Step 3: Configure Database (30 seconds)

**Edit `.env` file:**
```env
DB_PASSWORD=your_mysql_password_here
```

Replace `your_mysql_password_here` with your actual MySQL password.

### Step 4: Create Database (20 seconds)
```bash
mysql -u root -p
```
Enter password, then:
```sql
CREATE DATABASE cricbuzz_db;
exit;
```

---

## ▶️ Run the App (10 seconds)

### Option 1: Use Run Script
```bash
run.bat
```

### Option 2: Manual
```bash
venv\Scripts\activate
streamlit run app.py
```

**App will open at:** http://localhost:8501

---

## 📊 Load Sample Data (30 seconds)

1. In the app, click **🛠️ CRUD Operations** (sidebar)
2. Click **📊 Sample Data** tab
3. Click **📥 Load Sample Data** button
4. Wait for success message ✅

---

## 🎓 Try Your First Query (1 minute)

1. Click **🔍 SQL Queries** (sidebar)
2. Click **📚 Beginner** tab
3. Expand **Q1: Indian Players**
4. Click **▶️ Execute**
5. See the results! 🎉

---

## ✅ You're Done!

You now have:
- ✅ App running
- ✅ Database configured
- ✅ Sample data loaded
- ✅ First query executed

---

## 🎯 What's Next?

### Explore the App:
- **🏠 Home** - Project overview
- **📱 Live Matches** - Real-time cricket data
- **📊 Top Stats** - Player rankings
- **🔍 SQL Queries** - Practice 25 queries
- **🛠️ CRUD Operations** - Manage data

### Practice SQL:
1. Start with **Beginner queries (Q1-Q8)**
2. Move to **Intermediate (Q9-Q16)**
3. Challenge yourself with **Advanced (Q17-Q25)**

### Add Your Data:
1. Go to **CRUD Operations**
2. Click **➕ Create**
3. Add your own players, teams, venues

---

## 🆘 Having Issues?

### Common Problems:

**"Can't connect to MySQL"**
- Is MySQL running? Check Services
- Is password correct in `.env`?

**"Module not found"**
- Is virtual environment activated? See `(venv)` in prompt
- Run: `pip install -r requirements.txt`

**"Database doesn't exist"**
- Run: `CREATE DATABASE cricbuzz_db;` in MySQL

**More help:** See `TROUBLESHOOTING.md`

---

## 📚 Documentation

- **README.md** - Complete documentation
- **setup_guide.md** - Detailed setup steps
- **SQL_QUERIES_GUIDE.md** - Learn all 25 queries
- **API_TESTING_GUIDE.md** - API integration
- **TROUBLESHOOTING.md** - Fix common issues
- **PROJECT_SUMMARY.md** - Project overview

---

## 🎉 Success Checklist

- [ ] App opens in browser
- [ ] No error messages
- [ ] Sample data loaded
- [ ] First SQL query works
- [ ] Can navigate all pages

**All checked?** Congratulations! You're ready to learn! 🚀

---

## 💡 Pro Tips

1. **Keep terminal open** - See errors and logs
2. **Use Ctrl+C** to stop the app
3. **Press R** in app to refresh
4. **Press C** to clear cache
5. **Check sidebar** for database status

---

## 📞 Quick Commands

```bash
# Activate virtual environment
venv\Scripts\activate

# Run app
streamlit run app.py

# Stop app
Ctrl + C

# Check MySQL
mysql -u root -p

# View database
USE cricbuzz_db;
SHOW TABLES;
```

---

**Ready? Let's go! 🏏**

```bash
run.bat
```

**Happy Learning! 🎓📊**
