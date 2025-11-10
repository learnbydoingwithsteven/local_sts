@echo off
echo ======================================
echo Speech Translation System Setup
echo ======================================
echo.

echo [Step 1/5] Checking Ollama installation...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Ollama is not installed!
    echo.
    echo Please install Ollama first:
    echo   1. Visit: https://ollama.ai
    echo   2. Download and install for Windows
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)
echo ✓ Ollama is installed

echo.
echo [Step 2/5] Which model would you like to use?
echo.
echo   1. Qwen2.5 7B (RECOMMENDED) - Best translation quality + speed
echo   2. Gemma 2 9B - Highest quality (needs 12GB RAM)
echo   3. Llama 3.2 3B - Fastest (needs only 4GB RAM)
echo   4. All three models (for switching in UI)
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    set MODEL=qwen2.5:7b
    set MODEL_NAME=Qwen2.5 7B
    goto :pull_model
)
if "%choice%"=="2" (
    set MODEL=gemma2:9b
    set MODEL_NAME=Gemma 2 9B
    goto :pull_model
)
if "%choice%"=="3" (
    set MODEL=llama3.2:3b
    set MODEL_NAME=Llama 3.2 3B
    goto :pull_model
)
if "%choice%"=="4" (
    goto :pull_all
)

echo Invalid choice. Using default: Qwen2.5 7B
set MODEL=qwen2.5:7b
set MODEL_NAME=Qwen2.5 7B

:pull_model
echo.
echo [Step 3/5] Pulling %MODEL_NAME%...
echo This may take a few minutes depending on your internet speed...
ollama pull %MODEL%
if %errorlevel% neq 0 (
    echo ERROR: Failed to pull model
    pause
    exit /b 1
)
echo ✓ Model pulled successfully
goto :setup_env

:pull_all
echo.
echo [Step 3/5] Pulling all models...
echo This will download ~20GB total. Continue? (Y/N)
set /p confirm="Continue? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Setup cancelled.
    pause
    exit /b 0
)

echo.
echo Pulling Qwen2.5 7B...
ollama pull qwen2.5:7b
echo.
echo Pulling Gemma 2 9B...
ollama pull gemma2:9b
echo.
echo Pulling Llama 3.2 3B...
ollama pull llama3.2:3b
echo ✓ All models pulled successfully

set MODEL=qwen2.5:7b
goto :setup_env

:setup_env
echo.
echo [Step 4/5] Configuring environment...

REM Create .env file if it doesn't exist
if not exist .env (
    copy .env.example .env
    echo ✓ Created .env file
)

REM Update model in .env
powershell -Command "(Get-Content .env) -replace 'OLLAMA_MODEL=.*', 'OLLAMA_MODEL=%MODEL%' | Set-Content .env"
echo ✓ Set default model to %MODEL%

echo.
echo [Step 5/5] Installing dependencies...

REM Backend
echo.
echo Installing Python dependencies...
cd backend
if not exist venv (
    python -m venv venv
    echo ✓ Created virtual environment
)

call venv\Scripts\activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
if %errorlevel% neq 0 (
    echo WARNING: Some Python packages may have failed to install
    echo You may need to install them manually
)
echo ✓ Backend dependencies installed

REM Frontend
cd ..\frontend
echo.
echo Installing Node.js dependencies...
call npm install --silent
if %errorlevel% neq 0 (
    echo WARNING: Some Node packages may have failed to install
    echo You may need to run 'npm install' manually in the frontend folder
)
echo ✓ Frontend dependencies installed

cd ..

echo.
echo ======================================
echo ✓ Setup Complete!
echo ======================================
echo.
echo Model configured: %MODEL%
echo.
echo Next steps:
echo   1. Run: start.bat
echo   2. Open browser: http://localhost:5173
echo   3. Start translating!
echo.
echo To change models later, edit the .env file
echo or select a different model in the UI.
echo.
pause
