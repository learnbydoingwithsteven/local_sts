@echo off
echo ======================================
echo Real-Time Speech Translation System
echo Starting Services...
echo ======================================

echo.
echo [1/4] Checking Ollama...
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ollama is not installed or not running
    echo Please install Ollama from: https://ollama.ai
    pause
    exit /b 1
)
echo ✓ Ollama is running

echo.
echo [2/4] Pulling required models...
echo Pulling qwen2:7b (recommended for translation)...
ollama pull qwen2:7b

echo.
echo [3/4] Starting Backend...
cd backend
start cmd /k "python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python main.py"
cd ..

timeout /t 5 /nobreak >nul

echo.
echo [4/4] Starting Frontend...
cd frontend
start cmd /k "npm install && npm run dev"
cd ..

echo.
echo ======================================
echo ✓ All services started!
echo ======================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C in each terminal to stop services
pause
