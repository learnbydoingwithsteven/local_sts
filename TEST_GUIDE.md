# Testing Guide

Complete guide to test the Real-Time Speech Translation System.

## Quick Test (Recommended)

### 1. Start the System
```bash
# Windows
start.bat

# Linux/Mac
./start.sh

# OR Docker
docker-compose up
```

### 2. Open Browser
Navigate to: http://localhost:5173

### 3. Test the Workflow

#### Step 1: Check System Status
- Look at the "System Status" panel (bottom left)
- All services should show "Online" with green checkmarks
- If any service is offline, check the backend terminal for errors

#### Step 2: Configure Settings
- **Source Language**: Select "Auto-detect" or your speaking language
- **Target Language**: Select your desired translation language (e.g., Spanish)
- **Model**: Keep default (qwen2:7b) or select another if available
- **Voice**: Auto-selected based on target language

#### Step 3: Record and Translate
1. Click the large microphone button
2. Grant microphone permissions if prompted
3. Speak clearly: "Hello, how are you today?"
4. Click the button again to stop recording
5. Wait 2-5 seconds for processing

#### Step 4: Verify Results
- **Original Text**: Should show your transcribed speech
- **Detected Language**: Should show correct language code
- **Translation**: Should show translated text
- **Audio Output**: Should auto-play translated speech
- Click "Play" button to replay audio

## Detailed Testing

### Backend API Testing

#### 1. Health Check
```bash
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

#### 2. List Languages
```bash
curl http://localhost:8000/api/languages
```
Should return 15+ languages.

#### 3. List Models
```bash
curl http://localhost:8000/api/models
```
Should return installed Ollama models.

#### 4. Transcribe Audio
```bash
curl -X POST http://localhost:8000/api/transcribe \
  -F "file=@test_audio.wav"
```

#### 5. Translate Text
```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "source_lang": "en",
    "target_lang": "es"
  }'
```

#### 6. Full Pipeline
```bash
curl -X POST http://localhost:8000/api/full-pipeline \
  -F "file=@test_audio.wav" \
  -F "target_lang=es" \
  -o output.mp3
```

### Frontend Testing

#### 1. Component Testing
```bash
cd frontend
npm test
```

#### 2. E2E Testing (if configured)
```bash
npm run test:e2e
```

#### 3. Build Testing
```bash
npm run build
npm run preview
```

### Unit Tests

#### Backend
```bash
cd backend
pytest tests/ -v --cov=app

# Specific test
pytest tests/test_api.py::test_health_check -v

# With output
pytest tests/ -v -s
```

#### Coverage Report
```bash
pytest tests/ --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

## Performance Testing

### 1. Measure Latency

Create test script `test_latency.py`:
```python
import time
import requests

def test_pipeline_latency():
    url = "http://localhost:8000/api/full-pipeline"
    
    with open("test_audio.wav", "rb") as f:
        files = {"file": f}
        data = {"target_lang": "es"}
        
        start = time.time()
        response = requests.post(url, files=files, data=data)
        end = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Latency: {end - start:.2f} seconds")
        print(f"Audio size: {len(response.content)} bytes")

if __name__ == "__main__":
    for i in range(5):
        print(f"\nTest {i+1}:")
        test_pipeline_latency()
```

Run:
```bash
python test_latency.py
```

Expected latency:
- Whisper (base): 200-500ms
- Translation: 500-1500ms
- TTS: 300-500ms
- **Total: 1-3 seconds**

### 2. Load Testing

Use `locust` or `k6`:
```bash
pip install locust

# Create locustfile.py
cat > locustfile.py << EOF
from locust import HttpUser, task, between

class TranslationUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def health_check(self):
        self.client.get("/health")
    
    @task(3)
    def translate(self):
        self.client.post("/api/translate", json={
            "text": "Hello world",
            "source_lang": "en",
            "target_lang": "es"
        })

EOF

# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

Open: http://localhost:8089

### 3. Memory Usage

Monitor with:
```bash
# Backend
ps aux | grep python

# Docker
docker stats sts-backend sts-frontend sts-ollama
```

## Test Scenarios

### Scenario 1: English to Spanish
1. Source: Auto-detect
2. Target: Spanish
3. Speak: "Hello, how are you today?"
4. Expected: "Hola, ¿cómo estás hoy?"

### Scenario 2: Chinese to English
1. Source: Chinese
2. Target: English
3. Speak: "你好，今天天气怎么样？"
4. Expected: "Hello, how is the weather today?"

### Scenario 3: Long Recording
1. Record for 30+ seconds
2. Should handle gracefully
3. Check for proper segmentation

### Scenario 4: Background Noise
1. Record with music/noise in background
2. Check transcription accuracy
3. VAD should filter some noise

### Scenario 5: Multiple Languages
1. Test 5-10 different language pairs
2. Verify translation quality
3. Check voice output matches target language

## Troubleshooting Tests

### Backend Not Starting
```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies
pip list | grep fastapi
pip list | grep faster-whisper

# Check port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Check logs
cat backend/logs/app.log
```

### Frontend Not Loading
```bash
# Check Node version
node --version  # Should be 20+

# Check dependencies
npm list

# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check port
netstat -ano | findstr :5173  # Windows
lsof -i :5173                 # Linux/Mac
```

### Ollama Issues
```bash
# Check if running
ollama list

# Check models
ollama list | grep qwen2

# Test connection
curl http://localhost:11434/api/tags

# Restart service
systemctl restart ollama  # Linux
brew services restart ollama  # Mac
# Just restart Ollama app on Windows
```

### Microphone Not Working
1. Check browser permissions
2. Test with: navigator.mediaDevices.getUserMedia({audio: true})
3. Try different browser
4. Check system audio settings

### Translation Quality Issues
1. Try different model (gemma2:9b for better quality)
2. Improve audio quality
3. Speak more clearly
4. Check if model supports language pair

## Performance Benchmarks

### Expected Performance

| Component | Time | Notes |
|-----------|------|-------|
| STT (Whisper base) | 200-500ms | Per 10s audio |
| Translation (Qwen2 7B) | 500-1500ms | Per sentence |
| TTS (Edge) | 300-500ms | Per sentence |
| **Total Pipeline** | **1-3s** | End-to-end |

### Model Comparison

| Model | Speed | Quality | Memory |
|-------|-------|---------|--------|
| Qwen3 1.7B | ⚡⚡⚡⚡⚡ | ⭐⭐ | 2GB |
| Llama 3.2 3B | ⚡⚡⚡⚡ | ⭐⭐⭐ | 3GB |
| Qwen2 7B | ⚡⚡⚡ | ⭐⭐⭐⭐ | 7GB |
| Gemma2 9B | ⚡⚡ | ⭐⭐⭐⭐⭐ | 9GB |

## Automated Testing

### GitHub Actions
Push code to trigger CI/CD:
```bash
git add .
git commit -m "Test deployment"
git push origin main
```

Check results at: `https://github.com/your-repo/actions`

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Set up hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Success Criteria

✅ **Backend Health Check**: Status 200, all services operational  
✅ **Model Loading**: At least one Ollama model available  
✅ **Audio Recording**: Microphone access granted, recording works  
✅ **Transcription**: Audio converted to text with correct language  
✅ **Translation**: Text translated to target language  
✅ **TTS**: Translated text converted to natural speech  
✅ **Total Latency**: < 5 seconds for 10s audio  
✅ **UI Responsive**: No lag, smooth interactions  
✅ **No Errors**: Clean logs, no exceptions  

## Reporting Issues

When reporting issues, include:
1. OS and versions (Python, Node, Ollama)
2. Backend logs (`backend/logs/app.log`)
3. Browser console output (F12)
4. Steps to reproduce
5. Expected vs actual behavior
6. Audio file (if relevant)

---

**Happy Testing! 🧪**
