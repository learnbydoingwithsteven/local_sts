@echo off
echo ================================
echo System Status Check
echo ================================
echo.

echo [1] Backend Status:
curl -s http://localhost:8000/health 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Backend not responding
) else (
    echo OK: Backend is running
)

echo.
echo [2] Frontend Status:
curl -s http://localhost:5173 2>nul >nul
if %errorlevel% neq 0 (
    echo ERROR: Frontend not responding
) else (
    echo OK: Frontend is running
)

echo.
echo [3] Ollama Status:
ollama list 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Ollama not available
) else (
    echo OK: Ollama models available
)

echo.
echo [4] Test Translation:
curl -X POST http://localhost:8000/api/translate ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Hello\",\"source_lang\":\"en\",\"target_lang\":\"es\"}" 2>nul

echo.
echo.
pause
