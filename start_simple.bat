@echo off
echo Starting Speech Translation System...
echo.

cd backend
start cmd /k "venv\Scripts\activate && python main.py"
timeout /t 5 /nobreak >nul

cd ..\frontend
start cmd /k "npm run dev"

echo.
echo Services starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
