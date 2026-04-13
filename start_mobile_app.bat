@echo off
echo ========================================
echo    DU LICH HA NOI AI - MOBILE APP
echo ========================================
echo.

echo [1/2] Starting Backend API Server...
start "Backend Server" cmd /k "cd /d d:\dean-main && .venv\Scripts\activate && cd backend && python main.py"

echo [2/2] Starting Mobile App Server...
start "Mobile App" cmd /k "cd /d d:\dean-main\mobile-app && python -m http.server 3000"

echo.
echo ========================================
echo SERVERS STARTED SUCCESSFULLY!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Mobile App:  http://localhost:3000
echo.
echo To access from mobile:
echo 1. Connect phone to same WiFi network
echo 2. Find your PC IP: ipconfig (look for IPv4)
echo 3. Open browser: http://192.168.25.100:3000
echo.
echo Press any key to close this window...
pause > nul