@echo off
echo.
echo ===============================================
echo  Brain Checker Bot - Interactive UI Setup
echo ===============================================
echo.

echo Step 1: Checking if Ollama is running...
echo Note: Make sure Ollama is running locally on port 11434
echo You can download Ollama from: https://ollama.ai
echo.

echo Step 2: Starting FastAPI Backend...
echo.
start cmd /k "cd /d %CD% && python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Waiting 3 seconds before starting Streamlit...
timeout /t 3

echo Step 3: Starting Streamlit Frontend...
echo.
streamlit run streamlit_app.py

echo.
echo ===============================================
echo  Both services should now be running!
echo ===============================================
