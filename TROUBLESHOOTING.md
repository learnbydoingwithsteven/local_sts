# Troubleshooting Guide

Quick solutions to common problems.

## 🔍 Step 1: Run Diagnostics

```bash
# Run diagnostic script
diagnose.bat
```

This will check:
- ✅ Python installation
- ✅ Node.js installation
- ✅ Ollama installation
- ✅ Ollama service status
- ✅ Port availability
- ✅ Models installed

## ❌ Common Issues & Solutions

### Issue 1: "Python not found"

**Solution:**
```bash
# Install Python 3.11+
# Download from: https://www.python.org/downloads/

# OR use winget
winget install Python.Python.3.11

# Verify
python --version
```

### Issue 2: "Node.js not found"

**Solution:**
```bash
# Install Node.js 20+
# Download from: https://nodejs.org/

# OR use winget
winget install OpenJS.NodeJS.LTS

# Verify
node --version
npm --version
```

### Issue 3: "Ollama not installed"

**Solution:**
```bash
# Install Ollama
# Download from: https://ollama.ai

# OR use winget
winget install Ollama.Ollama

# Verify
ollama --version

# Start Ollama (should auto-start)
# Check system tray for Ollama icon
```

### Issue 4: "Ollama service not running"

**Solution:**
```bash
# Option 1: Restart Ollama app
# Close and reopen Ollama from Start menu

# Option 2: Check if running
curl http://localhost:11434/api/tags

# Option 3: Manual start
ollama serve
```

### Issue 5: "No models available"

**Solution:**
```bash
# Pull recommended model
ollama pull qwen2:7b

# Verify
ollama list

# Alternative models
ollama pull gemma2:9b    # Better quality
ollama pull llama3.2:3b  # Faster
```

### Issue 6: "Port 8000 already in use"

**Solution:**
```bash
# Find process using port
netstat -ano | findstr :8000

# Kill the process (replace <PID> with actual PID)
taskkill /PID <PID> /F

# OR change backend port in .env
# Edit .env and change PORT=8000 to PORT=8001
```

### Issue 7: "Port 5173 already in use"

**Solution:**
```bash
# Find and kill process
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# OR change frontend port in vite.config.js
```

### Issue 8: "Backend fails to start"

**Check logs:**
```bash
cd backend
type logs\app.log
```

**Common causes:**

1. **Missing dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Python version too old**
```bash
python --version  # Must be 3.11+
```

3. **Virtual environment not activated**
```bash
cd backend
venv\Scripts\activate
```

### Issue 9: "Frontend won't load"

**Solution:**
```bash
cd frontend

# Clear cache and reinstall
rmdir /s /q node_modules
del package-lock.json
npm install

# Try again
npm run dev
```

### Issue 10: "Module not found" errors

**Backend:**
```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Frontend:**
```bash
cd frontend
npm ci  # Clean install
```

### Issue 11: "Microphone not working"

**Solution:**
1. Check browser permissions
   - Chrome: Settings > Privacy > Site Settings > Microphone
   - Allow access for localhost

2. Check Windows permissions
   - Settings > Privacy > Microphone
   - Allow apps to access microphone

3. Test microphone
   - Open browser console (F12)
   - Run: `navigator.mediaDevices.getUserMedia({audio: true})`
   - Should prompt for permission

### Issue 12: "Translation failed"

**Check:**
```bash
# 1. Ollama is running
curl http://localhost:11434/api/tags

# 2. Model is installed
ollama list

# 3. Model works
ollama run qwen2:7b "Translate to Spanish: Hello world"

# 4. Check backend logs
cd backend
type logs\app.log
```

### Issue 13: "Audio playback not working"

**Solution:**
1. Check browser audio settings
2. Increase system volume
3. Try different browser
4. Check backend TTS service in logs

### Issue 14: "Docker issues"

**Docker not starting:**
```bash
# Make sure Docker Desktop is running
# Check Docker status
docker --version
docker ps
```

**Container fails:**
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs ollama

# Restart containers
docker-compose restart

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Issue 15: "Import errors in Python"

**Solution:**
```bash
cd backend

# Make sure venv is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt

# If still failing, recreate venv
deactivate
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 🐛 Debugging Steps

### 1. Check Backend Health

```bash
# Terminal 1: Start backend
cd backend
python main.py

# Terminal 2: Test health
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "All services operational",
  "version": "1.0.0",
  "services": {
    "stt": "operational",
    "translation": "operational",
    "tts": "operational"
  }
}
```

### 2. Check Frontend

```bash
# Start frontend
cd frontend
npm run dev

# Should open at http://localhost:5173
```

### 3. Test API Endpoints

```bash
# List languages
curl http://localhost:8000/api/languages

# List models
curl http://localhost:8000/api/models

# Test translation
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Hello\",\"source_lang\":\"en\",\"target_lang\":\"es\"}"
```

### 4. Check Browser Console

1. Open browser (http://localhost:5173)
2. Press F12 to open DevTools
3. Go to Console tab
4. Look for errors (red text)
5. Common issues:
   - CORS errors → Check backend CORS_ORIGINS
   - Network errors → Backend not running
   - Permission errors → Allow microphone access

## 📝 Getting Detailed Error Information

### Backend Errors

```bash
# View logs
cd backend
type logs\app.log

# Run with debug mode
set LOG_LEVEL=DEBUG
python main.py
```

### Frontend Errors

```bash
# Browser console (F12)
# Look for red errors

# Check network tab
# F12 > Network
# Filter: XHR
# Look for failed requests (red)
```

### Ollama Errors

```bash
# Check Ollama logs
# Windows: C:\Users\<username>\.ollama\logs\

# Test Ollama directly
ollama run qwen2:7b "Hello"

# Check API
curl http://localhost:11434/api/tags
```

## 🔧 Reset Everything

If nothing works, try a complete reset:

```bash
# 1. Stop all services
# Close all terminals running backend/frontend

# 2. Clean Python
cd backend
rmdir /s /q venv
rmdir /s /q __pycache__
rmdir /s /q app\__pycache__

# 3. Clean Node
cd ..\frontend
rmdir /s /q node_modules
del package-lock.json

# 4. Clean logs
cd ..
rmdir /s /q logs
mkdir logs

# 5. Reinstall
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

cd ..\frontend
npm install

# 6. Try again
cd ..
start.bat
```

## 📞 Still Not Working?

### Collect Debug Information

```bash
# Run diagnostics
diagnose.bat > debug_info.txt

# Add backend logs
type backend\logs\app.log >> debug_info.txt

# Add system info
systeminfo >> debug_info.txt
```

### Check These Files

1. **Backend logs**: `backend/logs/app.log`
2. **Browser console**: F12 > Console tab
3. **Network requests**: F12 > Network tab
4. **Ollama status**: `ollama list`

### Provide This Information

When asking for help, include:
- 🖥️ OS version (Windows 10/11)
- 🐍 Python version (`python --version`)
- 📦 Node version (`node --version`)
- 🤖 Ollama version (`ollama --version`)
- ❌ Exact error message
- 📋 Steps to reproduce
- 📝 Relevant log entries

## ✅ Verification Checklist

Before running the system, verify:

- [ ] Python 3.11+ installed
- [ ] Node.js 20+ installed
- [ ] Ollama installed and running
- [ ] At least one model pulled (`ollama list`)
- [ ] Ports 8000, 5173, 11434 available
- [ ] Virtual environment created (`backend/venv/`)
- [ ] Dependencies installed (backend and frontend)
- [ ] .env file exists
- [ ] No red errors in backend terminal
- [ ] No red errors in frontend terminal
- [ ] Browser can access http://localhost:5173

## 🎯 Quick Fixes

**"Everything is installed but not working"**
```bash
# Restart Ollama
# Close Ollama app, restart from Start menu

# Restart terminals
# Close all terminals, open new ones

# Try Docker instead
docker-compose up
```

**"Slow performance"**
```bash
# Use smaller model
ollama pull llama3.2:3b

# Use smaller Whisper model
# Edit .env: WHISPER_MODEL=tiny

# Close other applications
```

**"Out of memory"**
```bash
# Use smaller models
ollama pull qwen2:1.5b  # Smallest

# Reduce Whisper model size
# Edit .env: WHISPER_MODEL=tiny or base
```

---

**If you've tried everything and it still doesn't work, please share the specific error message and I'll help you debug it! 🔧**
