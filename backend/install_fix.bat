@echo off
echo Installing dependencies with pre-built wheels...
echo.

REM Install av from pre-built wheel first
pip install av --only-binary :all:

REM Then install everything else
pip install -r requirements.txt

echo.
echo Done!
pause
