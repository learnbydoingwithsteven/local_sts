@echo off
echo ======================================
echo System Diagnostics
echo ======================================
echo.

echo [1/6] Checking Python...
python --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found or not in PATH
    echo    Install from: https://www.python.org/downloads/
) else (
    echo ✓ Python installed
)

echo.
echo [2/6] Checking Node.js...
node --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js not found
    echo    Install from: https://nodejs.org/
) else (
    echo ✓ Node.js installed
    node --version
)

echo.
echo [3/6] Checking npm...
npm --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ npm not found
) else (
    echo ✓ npm installed
    npm --version
)

echo.
echo [4/6] Checking Ollama...
ollama --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Ollama not installed
    echo    Install from: https://ollama.ai
) else (
    echo ✓ Ollama installed
    ollama --version
)

echo.
echo [5/6] Checking Ollama service...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama service not running
    echo    Start Ollama and try again
) else (
    echo ✓ Ollama service running
)

echo.
echo [6/6] Checking Ollama models...
ollama list 2>nul
if %errorlevel% neq 0 (
    echo ❌ Cannot list models
) else (
    echo ✓ Models available
)

echo.
echo ======================================
echo Port Availability Check
echo ======================================
netstat -ano | findstr :8000 >nul
if %errorlevel% equ 0 (
    echo ❌ Port 8000 is already in use
    echo    Backend port conflict detected
) else (
    echo ✓ Port 8000 available
)

netstat -ano | findstr :5173 >nul
if %errorlevel% equ 0 (
    echo ❌ Port 5173 is already in use
    echo    Frontend port conflict detected
) else (
    echo ✓ Port 5173 available
)

netstat -ano | findstr :11434 >nul
if %errorlevel% equ 0 (
    echo ✓ Port 11434 in use (Ollama running)
) else (
    echo ❌ Port 11434 not in use (Ollama not running?)
)

echo.
echo ======================================
echo Diagnosis Complete
echo ======================================
pause
