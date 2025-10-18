@echo off
echo ========================================
echo Starting Cricbuzz LiveStats...
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run Streamlit app
streamlit run app.py

pause
