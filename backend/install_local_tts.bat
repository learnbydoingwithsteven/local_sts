@echo off
echo ================================
echo Installing Local TTS
echo ================================
echo.

echo Installing pyttsx3 (local TTS engine)...
pip install pyttsx3

echo.
echo Installing Windows TTS dependencies...
pip install pywin32

echo.
echo ================================
echo Installation Complete!
echo ================================
echo.
echo Local TTS is now ready to use.
echo No internet required for speech synthesis!
echo.
pause
