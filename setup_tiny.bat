@echo off
echo ======================================
echo Speech Translation - TINY Setup
echo For systems with limited RAM
echo ======================================
echo.

echo Checking your system...
echo.

REM Get available RAM
for /f "skip=1" %%p in ('wmic os get freephysicalmemory') do (
    set /a RAM_KB=%%p
    goto :got_ram
)
:got_ram
set /a RAM_GB=RAM_KB/1024/1024
echo Available RAM: %RAM_GB%GB

echo.
echo [Step 1/4] Checking Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ollama not installed!
    echo Install from: https://ollama.ai
    pause
    exit /b 1
)
echo ✓ Ollama installed

echo.
echo [Step 2/4] Selecting best tiny model for your system...
echo.

if %RAM_GB% LEQ 3 (
    echo Your system has %RAM_GB%GB available RAM
    echo Recommended: Qwen2.5 0.5B (uses only 1GB RAM)
    set MODEL=qwen2.5:0.5b
    set MODEL_NAME=Qwen2.5 0.5B (Ultra-Tiny)
) else if %RAM_GB% LEQ 5 (
    echo Your system has %RAM_GB%GB available RAM
    echo Recommended: Qwen2.5 1.5B (uses only 2GB RAM)
    set MODEL=qwen2.5:1.5b
    set MODEL_NAME=Qwen2.5 1.5B (Tiny, Good Quality)
) else (
    echo Your system has %RAM_GB%GB available RAM
    echo Recommended: Gemma 2 2B (uses 3GB RAM)
    set MODEL=gemma2:2b
    set MODEL_NAME=Gemma 2 2B (Small, Best Quality)
)

echo.
echo Recommended model: %MODEL_NAME%
echo.
set /p confirm="Use this model? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo.
    echo Available tiny models:
    echo   1. Qwen2.5 0.5B - 1GB RAM, ultra-fast
    echo   2. Llama 3.2 1B - 1.5GB RAM, fast
    echo   3. Qwen2.5 1.5B - 2GB RAM, good quality (RECOMMENDED)
    echo   4. Gemma 2 2B - 3GB RAM, best quality
    echo.
    set /p choice="Choose model (1-4): "
    
    if "%choice%"=="1" (
        set MODEL=qwen2.5:0.5b
        set MODEL_NAME=Qwen2.5 0.5B
    ) else if "%choice%"=="2" (
        set MODEL=llama3.2:1b
        set MODEL_NAME=Llama 3.2 1B
    ) else if "%choice%"=="3" (
        set MODEL=qwen2.5:1.5b
        set MODEL_NAME=Qwen2.5 1.5B
    ) else if "%choice%"=="4" (
        set MODEL=gemma2:2b
        set MODEL_NAME=Gemma 2 2B
    ) else (
        echo Invalid choice. Using Qwen2.5 1.5B
        set MODEL=qwen2.5:1.5b
    )
)

echo.
echo [Step 3/4] Pulling %MODEL%...
echo This is a small download (300MB-1.5GB)
ollama pull %MODEL%
if %errorlevel% neq 0 (
    echo ERROR: Failed to pull model
    pause
    exit /b 1
)
echo ✓ Model downloaded

echo.
echo [Step 4/4] Configuring system...

REM Update .env
if not exist .env copy .env.example .env
powershell -Command "(Get-Content .env) -replace 'OLLAMA_MODEL=.*', 'OLLAMA_MODEL=%MODEL%' | Set-Content .env"
powershell -Command "(Get-Content .env) -replace 'WHISPER_MODEL=.*', 'WHISPER_MODEL=tiny' | Set-Content .env"

echo ✓ Configuration updated

echo.
echo Installing dependencies...
cd backend
if not exist venv python -m venv venv
call venv\Scripts\activate
pip install --quiet -r requirements.txt
cd ..\frontend
call npm install --silent
cd ..

echo.
echo ======================================
echo ✓ TINY Setup Complete!
echo ======================================
echo.
echo Configuration:
echo   Translation Model: %MODEL%
echo   Whisper Model: tiny (fast, lightweight)
echo   Text-to-Speech: Edge TTS (cloud, free)
echo.
echo Total RAM usage: ~2-3GB
echo Total disk space: ~1-2GB
echo.
echo Next: Run start.bat
echo.
pause
