# 🔧 Troubleshooting Guide

Complete troubleshooting guide for common issues in Cricbuzz LiveStats.

---

## 🗄️ Database Issues

### Issue 1: "Can't connect to MySQL server on 'localhost'"

**Symptoms**:
- Error message when starting the app
- Database connection fails
- Red status in sidebar

**Solutions**:

1. **Check if MySQL is running**:
   ```bash
   # Windows: Open Services
   # Press Win + R, type: services.msc
   # Find "MySQL80" or "MySQL" service
   # Right-click → Start
   ```

2. **Verify MySQL is installed**:
   ```bash
   mysql --version
   ```
   If not installed, download from: https://dev.mysql.com/downloads/mysql/

3. **Test connection manually**:
   ```bash
   mysql -u root -p
   # Enter your password
   ```

4. **Check `.env` file**:
   ```env
   DB_HOST=localhost  # Should be localhost
   DB_USER=root       # Your MySQL username
   DB_PASSWORD=yourpassword  # Your actual password
   DB_NAME=cricbuzz_db
   ```

---

### Issue 2: "Access denied for user 'root'@'localhost'"

**Symptoms**:
- Authentication error
- Wrong password message

**Solutions**:

1. **Verify password in `.env`**:
   - Open `.env` file
   - Check `DB_PASSWORD` matches your MySQL password
   - No extra spaces or quotes

2. **Reset MySQL password** (if forgotten):
   ```bash
   # Stop MySQL service
   # Start MySQL in safe mode
   # Reset password using MySQL documentation
   ```

3. **Try different user**:
   - Create a new MySQL user
   - Grant permissions
   - Update `.env` with new credentials

---

### Issue 3: "Unknown database 'cricbuzz_db'"

**Symptoms**:
- Database doesn't exist error
- Can't select database

**Solutions**:

1. **Create the database**:
   ```sql
   mysql -u root -p
   CREATE DATABASE cricbuzz_db;
   SHOW DATABASES;  -- Verify it's created
   exit;
   ```

2. **Check database name in `.env`**:
   ```env
   DB_NAME=cricbuzz_db  # Must match exactly
   ```

---

### Issue 4: "Table doesn't exist"

**Symptoms**:
- SQL errors about missing tables
- Empty database

**Solutions**:

1. **Let the app create tables**:
   - The app automatically creates tables on first run
   - Just restart the app

2. **Manually verify tables**:
   ```sql
   USE cricbuzz_db;
   SHOW TABLES;
   ```

3. **If tables are missing**, restart the app to auto-create them

---

## 🌐 API Issues

### Issue 5: "API request failed"

**Symptoms**:
- No data in Live Matches
- API errors in console
- Empty responses

**Solutions**:

1. **Check internet connection**:
   - Ensure you're online
   - Try opening https://www.google.com

2. **Verify API key**:
   ```env
   RAPIDAPI_KEY=your_actual_key_here
   ```
   - No spaces
   - Complete key
   - From RapidAPI dashboard

3. **Check API subscription**:
   - Go to RapidAPI dashboard
   - Verify subscription is active
   - Check you haven't exceeded quota

4. **Test API manually**:
   ```bash
   python verify_api.py
   ```

---

### Issue 6: "Rate limit exceeded"

**Symptoms**:
- 429 error code
- "Too many requests" message

**Solutions**:

1. **Check your quota**:
   - Go to RapidAPI dashboard
   - View Analytics
   - See remaining requests

2. **Wait for reset**:
   - Free plan resets monthly
   - Wait until next month

3. **Upgrade plan**:
   - Consider Pro or Ultra plan
   - More requests available

4. **Use sample data**:
   - Go to CRUD Operations → Sample Data
   - Load sample data
   - Practice without API calls

---

## 🐍 Python Issues

### Issue 7: "ModuleNotFoundError: No module named 'streamlit'"

**Symptoms**:
- Import errors
- Module not found errors

**Solutions**:

1. **Activate virtual environment**:
   ```bash
   # Windows Command Prompt:
   venv\Scripts\activate
   
   # Windows PowerShell:
   venv\Scripts\Activate.ps1
   
   # You should see (venv) in prompt
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   pip list | findstr streamlit
   ```

---

### Issue 8: "Python is not recognized"

**Symptoms**:
- Command not found
- Python not in PATH

**Solutions**:

1. **Install Python**:
   - Download from: https://www.python.org/
   - **Important**: Check "Add Python to PATH" during installation

2. **Verify installation**:
   ```bash
   python --version
   ```

3. **Add to PATH manually** (if needed):
   - Search "Environment Variables"
   - Edit PATH
   - Add Python installation directory

---

### Issue 9: "Execution policy error" (PowerShell)

**Symptoms**:
- Can't activate virtual environment in PowerShell
- Execution policy restriction

**Solutions**:

1. **Change execution policy**:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Or use Command Prompt instead**:
   ```bash
   # Use cmd.exe instead of PowerShell
   venv\Scripts\activate.bat
   ```

---

## 🎨 Streamlit Issues

### Issue 10: "Port 8501 is already in use"

**Symptoms**:
- Can't start Streamlit
- Port conflict error

**Solutions**:

1. **Kill existing Streamlit process**:
   ```bash
   # Find process
   netstat -ano | findstr :8501
   
   # Kill process (replace PID with actual number)
   taskkill /PID <PID> /F
   ```

2. **Use different port**:
   ```bash
   streamlit run app.py --server.port 8502
   ```

---

### Issue 11: "Streamlit app shows blank page"

**Symptoms**:
- White screen
- No content loads
- Browser shows blank

**Solutions**:

1. **Check browser console**:
   - Press F12
   - Look for JavaScript errors
   - Check Network tab

2. **Clear browser cache**:
   - Ctrl + Shift + Delete
   - Clear cache
   - Refresh page

3. **Try different browser**:
   - Chrome, Firefox, Edge
   - Incognito/Private mode

4. **Check terminal for errors**:
   - Look at terminal where Streamlit is running
   - Check for Python errors

---

## 📁 File Issues

### Issue 12: ".env file not found"

**Symptoms**:
- Environment variables not loading
- Default values being used

**Solutions**:

1. **Create .env file**:
   ```bash
   copy .env.example .env
   ```

2. **Verify file exists**:
   ```bash
   dir .env
   ```

3. **Check file location**:
   - Must be in project root directory
   - Same folder as `app.py`

---

### Issue 13: "Permission denied"

**Symptoms**:
- Can't write files
- Can't create directories

**Solutions**:

1. **Run as administrator**:
   - Right-click Command Prompt
   - "Run as administrator"

2. **Check folder permissions**:
   - Right-click project folder
   - Properties → Security
   - Ensure you have write permissions

---

## 💾 Data Issues

### Issue 14: "No data in database"

**Symptoms**:
- SQL queries return empty
- Tables exist but no rows

**Solutions**:

1. **Load sample data**:
   - Go to CRUD Operations
   - Click Sample Data tab
   - Click "Load Sample Data"

2. **Add data manually**:
   - Go to CRUD Operations
   - Click Create tab
   - Add teams, players, etc.

3. **Verify data exists**:
   ```sql
   SELECT COUNT(*) FROM players;
   SELECT COUNT(*) FROM teams;
   ```

---

### Issue 15: "SQL query returns error"

**Symptoms**:
- Query execution fails
- Syntax errors

**Solutions**:

1. **Check table names**:
   - Use exact table names
   - Case-sensitive in some systems

2. **Verify columns exist**:
   ```sql
   DESCRIBE players;
   ```

3. **Start with simple queries**:
   ```sql
   SELECT * FROM players LIMIT 5;
   ```

4. **Check for NULL values**:
   - Some queries fail with NULL data
   - Use `IS NOT NULL` conditions

---

## 🔄 General Issues

### Issue 16: "App is slow"

**Symptoms**:
- Long loading times
- Laggy interface

**Solutions**:

1. **Check database size**:
   - Large datasets slow queries
   - Use LIMIT in queries

2. **Optimize queries**:
   - Add indexes
   - Use WHERE clauses
   - Limit result sets

3. **Close other applications**:
   - Free up RAM
   - Close unused programs

---

### Issue 17: "Changes not reflecting"

**Symptoms**:
- Code changes don't show
- Old data still displays

**Solutions**:

1. **Rerun Streamlit**:
   - Click "Rerun" in top-right
   - Or press R in terminal

2. **Clear Streamlit cache**:
   - Press C in terminal
   - Clears cached data

3. **Restart application**:
   - Ctrl + C to stop
   - Run `streamlit run app.py` again

---

## 🆘 Getting Help

### Before Asking for Help:

1. **Check error message**:
   - Read the full error
   - Note the error type
   - Copy the stack trace

2. **Check this guide**:
   - Search for your error
   - Try suggested solutions

3. **Check logs**:
   - Terminal output
   - Browser console (F12)
   - MySQL error logs

### Information to Provide:

- Operating System (Windows version)
- Python version (`python --version`)
- Error message (full text)
- What you were trying to do
- What you've already tried

---

## 🧪 Diagnostic Commands

### Check Everything:

```bash
# Python
python --version
pip --version

# MySQL
mysql --version
mysql -u root -p -e "SELECT 1;"

# Virtual Environment
where python  # Should show venv path when activated

# Installed Packages
pip list

# Environment Variables
type .env  # Shows .env file contents
```

### Test Database Connection:

```python
# test_db.py
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    print("✅ Database connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Database connection failed: {e}")
```

Run: `python test_db.py`

---

## 📋 Quick Fixes Checklist

When something goes wrong, try these in order:

- [ ] Is virtual environment activated? (`(venv)` in prompt)
- [ ] Is MySQL running? (Check Services)
- [ ] Is `.env` file configured correctly?
- [ ] Does database exist? (`SHOW DATABASES;`)
- [ ] Are dependencies installed? (`pip list`)
- [ ] Is internet working? (For API calls)
- [ ] Try restarting the app
- [ ] Try restarting MySQL
- [ ] Try restarting computer

---

**Still Having Issues?**

1. Review the error message carefully
2. Search for the specific error online
3. Check the README.md for setup instructions
4. Review the setup_guide.md for detailed steps

---

**Good Luck! 🍀**
