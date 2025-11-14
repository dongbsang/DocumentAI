@echo off
echo ========================================
echo DocumentAI Development Mode
echo ========================================
echo.
echo Starting backend and frontend servers...
echo.

REM Check if backend venv exists
if not exist backend\.venv (
    echo ERROR: Backend virtual environment not found
    echo Please run: cd backend ^&^& python -m venv .venv ^&^& .venv\Scripts\activate ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist frontend\node_modules (
    echo WARNING: Frontend dependencies not found
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
)

echo [1/2] Starting backend server...
start "DocumentAI Backend" cmd /k "cd /d %~dp0backend && .venv\Scripts\activate && flask run"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

echo [2/2] Starting frontend server...
start "DocumentAI Frontend" cmd /k "cd /d %~dp0frontend && npm start"

echo.
echo ========================================
echo Development servers started!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window
echo (Backend and Frontend will keep running)
pause >nul
