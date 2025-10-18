@echo off
echo ========================================
echo Cricbuzz LiveStats - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Python found!
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created successfully!
) else (
    echo Virtual environment already exists.
)
echo.

REM Activate virtual environment and install dependencies
echo [3/5] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed successfully!
echo.

REM Create .env file if it doesn't exist
echo [4/5] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo .env file created from template.
    echo IMPORTANT: Please edit .env file and add your MySQL password!
) else (
    echo .env file already exists.
)
echo.

REM Instructions
echo [5/5] Setup complete!
echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo 1. Edit .env file and add your MySQL password
echo 2. Create MySQL database: CREATE DATABASE cricbuzz_db;
echo 3. Run the application: streamlit run app.py
echo.
echo To activate virtual environment manually:
echo   venv\Scripts\activate
echo.
echo To run the application:
echo   streamlit run app.py
echo.
echo ========================================
pause
