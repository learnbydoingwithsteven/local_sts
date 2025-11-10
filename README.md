# Real-Time Speech Translation System 🎙️🌐🔊

A production-ready speech-to-text-to-speech translation system using **Whisper**, **Ollama**, and **Edge TTS**.

## 🌟 Features

- **Real-time Speech Recognition**: Faster Whisper for high-quality, fast transcription
- **Multi-language Translation**: Ollama with small capable models (Qwen3 8B, Gemma 2 9B)
- **Natural Voice Output**: Edge TTS with 100+ voices in 50+ languages
- **Modern Web UI**: React + Vite with real-time audio visualization
- **Production Ready**: Docker, CI/CD, security best practices
- **Agent Framework**: Extensible architecture for future AI agents

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend UI   │  React + Vite + WebRTC
└────────┬────────┘
         │ WebSocket
┌────────▼────────┐
│  FastAPI Server │  Python async backend
└─┬──────┬───────┬┘
  │      │       │
  │      │       └──> Edge TTS (Text-to-Speech)
  │      │
  │      └──> Ollama (Translation)
  │           - Qwen3 8B
  │           - Gemma 2 9B
  │           - Llama 3.2 3B
  │
  └──> Faster Whisper (Speech-to-Text)
       - base, small, medium models
```

## 📦 Tech Stack

### Backend
- **FastAPI**: High-performance async web framework
- **Faster Whisper**: Optimized Whisper implementation (4x faster)
- **Ollama**: Local LLM serving for translation
- **Edge TTS**: Microsoft Edge Text-to-Speech
- **WebSockets**: Real-time bidirectional communication

### Frontend
- **React 18**: Modern UI library
- **Vite**: Lightning-fast build tool
- **TailwindCSS**: Utility-first CSS framework
- **Zustand**: Lightweight state management
- **Wavesurfer.js**: Audio visualization

### DevOps
- **Docker & Docker Compose**: Containerization
- **GitHub Actions**: CI/CD pipeline
- **HTTPS/WSS**: Secure communication
- **CORS**: Proper security policies

## 🚀 Quick Start

### Prerequisites

```bash
# Install system dependencies
# Windows: Install Ollama from https://ollama.ai
# Linux/Mac:
curl -fsSL https://ollama.ai/install.sh | sh

# Pull recommended models
ollama pull qwen2:7b
ollama pull gemma2:9b
ollama pull llama3.2:3b
```

### Installation

```bash
# Clone repository
cd c:/Users/wjbea/Downloads/learnbydoingwithsteven/local_sts

# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### Running

**Option 1: Development Mode**

```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

**Option 2: Docker**

```bash
docker-compose up
```

Access: http://localhost:5173

## 📖 Usage

1. **Open the web app** in your browser
2. **Select languages**: Source → Target
3. **Choose model**: Qwen3 8B (fast), Gemma 2 9B (balanced), Llama 3.2 (tiny)
4. **Click microphone**: Start speaking
5. **Real-time translation**: See transcription → translation → hear voice output

## 🎯 Model Recommendations

Based on [Artificial Analysis](https://artificialanalysis.ai) rankings:

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| **Qwen3 8B** | 8B | ⚡⚡⚡ | ⭐⭐⭐⭐ | Best balance |
| **Gemma 2 9B** | 9B | ⚡⚡ | ⭐⭐⭐⭐⭐ | Best quality |
| **Llama 3.2 3B** | 3B | ⚡⚡⚡⚡ | ⭐⭐⭐ | Fastest |
| **Qwen3 1.7B** | 1.7B | ⚡⚡⚡⚡⚡ | ⭐⭐ | Ultra-fast |

## 🔒 Security Features

- ✅ CORS configuration with whitelist
- ✅ Rate limiting (10 requests/minute)
- ✅ Input validation and sanitization
- ✅ Secure WebSocket (WSS) in production
- ✅ Environment variable management
- ✅ No data persistence (privacy-first)
- ✅ Content Security Policy headers

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

## 📊 Performance

- **Transcription**: ~200ms (Faster Whisper base model)
- **Translation**: ~500-1000ms (depends on model)
- **Voice Output**: ~300ms (Edge TTS)
- **Total Latency**: ~1-2 seconds end-to-end

## 🌍 Supported Languages

**70+ languages** including:
- English, Spanish, French, German, Italian
- Chinese (Simplified/Traditional), Japanese, Korean
- Arabic, Hindi, Russian, Portuguese
- And many more...

## 🔧 Configuration

Edit `.env` file:

```env
# Backend
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2:7b
WHISPER_MODEL=base
TTS_VOICE=en-US-AriaNeural

# Security
CORS_ORIGINS=http://localhost:5173
RATE_LIMIT=10
MAX_AUDIO_SIZE=10485760  # 10MB

# Frontend
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## 📁 Project Structure

```
local_sts/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── services/         # Business logic
│   │   ├── models/           # Data models
│   │   ├── utils/            # Utilities
│   │   └── main.py           # FastAPI app
│   ├── tests/                # Backend tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API clients
│   │   ├── stores/           # State management
│   │   └── App.jsx           # Main app
│   ├── package.json
│   └── Dockerfile
├── .github/
│   └── workflows/            # CI/CD pipelines
├── docker-compose.yml
└── README.md
```

## 🚢 Deployment

### Production Build

```bash
# Build Docker images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables (Production)

```env
NODE_ENV=production
HTTPS_ENABLED=true
SSL_CERT_PATH=/path/to/cert.pem
SSL_KEY_PATH=/path/to/key.pem
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Faster Whisper](https://github.com/guillaumekln/faster-whisper)
- [Ollama](https://ollama.ai)
- [Edge TTS](https://github.com/rany2/edge-tts)
- [Microsoft Agent Lightning](https://github.com/microsoft/agent-lightning)

## 📧 Support

For issues and questions, please open a GitHub issue.

---

**Built with ❤️ for real-time multilingual communication**
