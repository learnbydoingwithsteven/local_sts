# Quick Start Guide 🚀

Get up and running with the Real-Time Speech Translation System in minutes!

## Prerequisites

### Required
- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Node.js 20+** ([Download](https://nodejs.org/))
- **Ollama** ([Download](https://ollama.ai))

### Optional
- **Docker & Docker Compose** (for containerized deployment)

## Option 1: Quick Start (Windows)

### 1. Install Ollama
```bash
# Download and install from https://ollama.ai
# Or use winget:
winget install Ollama.Ollama
```

### 2. Run the launcher
```bash
# Double-click start.bat
# OR run in terminal:
start.bat
```

That's it! The system will:
- ✅ Check Ollama installation
- ✅ Pull required models (qwen2:7b)
- ✅ Start backend server
- ✅ Start frontend UI
- ✅ Open browser automatically

Access the UI at: **http://localhost:5173**

## Option 2: Manual Setup

### Step 1: Install Ollama & Models
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh  # Linux/Mac
# OR download from https://ollama.ai          # Windows

# Pull recommended models
ollama pull qwen2:7b      # Best balance (recommended)
ollama pull gemma2:9b     # Best quality
ollama pull llama3.2:3b   # Fastest
```

### Step 2: Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/Mac

# Run server
python main.py
```

Backend will start at: **http://localhost:8000**
API docs at: **http://localhost:8000/docs**

### Step 3: Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will start at: **http://localhost:5173**

## Option 3: Docker Compose (Easiest)

```bash
# Make sure Docker is running

# Start all services
docker-compose up

# OR run in background
docker-compose up -d

# Pull required models
docker exec -it sts-ollama ollama pull qwen2:7b

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Access: **http://localhost:5173**

## Usage

### 1. Select Languages
- Source: Auto-detect or specific language
- Target: Choose your desired output language

### 2. Choose Model
- **Qwen3 8B**: Best balance of speed and quality (recommended)
- **Gemma 2 9B**: Highest quality translations
- **Llama 3.2 3B**: Fastest response time

### 3. Record Audio
1. Click the microphone button
2. Speak clearly into your microphone
3. Click again to stop recording
4. Wait for processing (1-3 seconds)
5. See transcription, translation, and hear audio output

## Troubleshooting

### "Ollama not installed"
```bash
# Install Ollama first
# Windows: https://ollama.ai/download/windows
# Mac: brew install ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh
```

### "No models available"
```bash
# Pull at least one model
ollama pull qwen2:7b
```

### "Failed to access microphone"
```
# Check browser permissions
# Chrome: Settings > Privacy > Site Settings > Microphone
# Allow access for localhost
```

### "Backend not responding"
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not, start it manually:
cd backend
python main.py
```

### "Port already in use"
```bash
# Backend (8000)
netstat -ano | findstr :8000   # Windows
# lsof -i :8000                # Linux/Mac

# Kill process or change port in .env

# Frontend (5173)
# Change port in vite.config.js
```

## Configuration

Edit `.env` file:

```env
# Backend
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2:7b
WHISPER_MODEL=base          # base, small, medium, large
TTS_VOICE=en-US-AriaNeural

# Frontend
VITE_API_URL=http://localhost:8000
```

## Performance Tips

### For Faster Processing
- Use **Whisper base** model (less accurate but faster)
- Use **Llama 3.2 3B** for translation
- Close other applications

### For Better Quality
- Use **Whisper medium** model
- Use **Gemma 2 9B** for translation
- Speak clearly with minimal background noise

## Supported Languages

**70+ languages** including:
- English, Spanish, French, German, Italian, Portuguese
- Chinese (Simplified/Traditional), Japanese, Korean
- Arabic, Hindi, Russian, Turkish, Vietnamese
- And many more...

## Next Steps

- **Customize voices**: Explore Edge TTS voices in settings
- **Add more models**: `ollama pull model-name`
- **Deploy to server**: See `README.md` for production setup
- **Extend features**: Check API docs at `/docs`

## Getting Help

- **Documentation**: See `README.md`
- **API Reference**: http://localhost:8000/docs
- **Issues**: Check backend terminal for error messages
- **Logs**: `backend/logs/app.log`

---

**Enjoy real-time speech translation! 🎙️🌐🔊**
