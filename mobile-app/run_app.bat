@echo off
echo ========================================
echo    DU LICH HA NOI AI - MOBILE APP
echo ========================================
echo.

echo [1/2] Khoi dong Backend Server...
start cmd /k "cd /d d:\dean-main\backend && python main.py"

timeout /t 3 /nobreak > nul

echo [2/2] Khoi dong Mobile App Server...
cd /d d:\dean-main\mobile-app
python -m http.server 3000

pause