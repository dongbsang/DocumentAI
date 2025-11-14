@echo off
echo ========================================
echo Stopping DocumentAI Development Servers
echo ========================================
echo.

REM Kill Flask processes
echo Stopping backend (Flask)...
taskkill /FI "WINDOWTITLE eq DocumentAI Backend*" /F >nul 2>&1

REM Kill Node processes (React dev server)
echo Stopping frontend (React)...
taskkill /FI "WINDOWTITLE eq DocumentAI Frontend*" /F >nul 2>&1

REM Alternative: Kill by port
echo Cleaning up ports...
FOR /F "tokens=5" %%P IN ('netstat -ano ^| findstr :5000') DO TaskKill.exe /F /PID %%P >nul 2>&1
FOR /F "tokens=5" %%P IN ('netstat -ano ^| findstr :3000') DO TaskKill.exe /F /PID %%P >nul 2>&1

echo.
echo All development servers stopped!
echo.
pause
