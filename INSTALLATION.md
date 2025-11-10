# Installation Guide

Detailed installation instructions for all platforms.

## System Requirements

### Minimum
- **CPU**: 4 cores, 2.5 GHz
- **RAM**: 8 GB
- **Storage**: 10 GB free space
- **OS**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 12+

### Recommended
- **CPU**: 8 cores, 3.5 GHz
- **RAM**: 16 GB
- **Storage**: 20 GB SSD
- **GPU**: NVIDIA GPU with 8GB+ VRAM (for faster processing)

## Platform-Specific Installation

### Windows 10/11

#### 1. Install Python 3.11
```powershell
# Download from https://www.python.org/downloads/
# OR use winget:
winget install Python.Python.3.11

# Verify installation
python --version  # Should show 3.11.x
```

#### 2. Install Node.js 20
```powershell
# Download from https://nodejs.org/
# OR use winget:
winget install OpenJS.NodeJS.LTS

# Verify installation
node --version  # Should show 20.x.x
npm --version   # Should show 10.x.x
```

#### 3. Install Ollama
```powershell
# Download installer from https://ollama.ai/download/windows
# OR use winget:
winget install Ollama.Ollama

# Verify installation
ollama --version
ollama list  # Should show empty list initially
```

#### 4. Install FFmpeg (for audio processing)
```powershell
# Download from https://ffmpeg.org/download.html
# OR use Chocolatey:
choco install ffmpeg

# Verify installation
ffmpeg -version
```

#### 5. Clone/Download Project
```powershell
git clone https://github.com/your-repo/local_sts.git
cd local_sts
```

#### 6. Run Quick Start
```powershell
.\start.bat
```

### Linux (Ubuntu/Debian)

#### 1. Install Python 3.11
```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip
python3.11 --version
```

#### 2. Install Node.js 20
```bash
# Using NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node --version
npm --version
```

#### 3. Install Ollama
```bash
curl -fsSL https://ollama.ai/install.sh | sh

# Verify
ollama --version
systemctl status ollama
```

#### 4. Install System Dependencies
```bash
sudo apt install -y ffmpeg libsndfile1 libportaudio2
```

#### 5. Clone/Download Project
```bash
git clone https://github.com/your-repo/local_sts.git
cd local_sts
```

#### 6. Run Setup
```bash
chmod +x start.sh
./start.sh
```

### macOS

#### 1. Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Install Dependencies
```bash
# Python 3.11
brew install python@3.11
python3.11 --version

# Node.js 20
brew install node@20
node --version

# Ollama
brew install ollama
ollama --version

# FFmpeg
brew install ffmpeg
ffmpeg -version
```

#### 3. Start Ollama Service
```bash
brew services start ollama
ollama list
```

#### 4. Clone/Download Project
```bash
git clone https://github.com/your-repo/local_sts.git
cd local_sts
```

#### 5. Run Setup
```bash
chmod +x start.sh
./start.sh
```

## Manual Installation (All Platforms)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
## Windows:
venv\Scripts\activate
## Linux/Mac:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows

# Edit .env with your settings
# nano .env  # Linux/Mac
# notepad .env  # Windows
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows

# Edit if needed
```

### Pull Ollama Models

```bash
# Recommended model
ollama pull qwen2:7b

# Alternative models
ollama pull gemma2:9b    # Better quality
ollama pull llama3.2:3b  # Faster

# List installed models
ollama list
```

## Docker Installation

### 1. Install Docker

#### Windows
```powershell
# Download Docker Desktop from https://docker.com
# OR use winget:
winget install Docker.DockerDesktop
```

#### Linux
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

#### macOS
```bash
brew install --cask docker
```

### 2. Install Docker Compose
```bash
# Usually included with Docker Desktop
docker-compose --version
```

### 3. Run with Docker
```bash
cd local_sts

# Build and start all services
docker-compose up -d

# Pull models inside container
docker exec -it sts-ollama ollama pull qwen2:7b

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

## GPU Support (NVIDIA)

### Linux

```bash
# Install NVIDIA Docker runtime
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt update
sudo apt install -y nvidia-docker2
sudo systemctl restart docker

# Test GPU access
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### Update docker-compose.yml

Uncomment the GPU section in `docker-compose.yml`:
```yaml
services:
  ollama:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## Verification

### Check Backend
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}
```

### Check Frontend
```bash
curl http://localhost:5173
# Should return HTML
```

### Check Ollama
```bash
ollama list
# Should show installed models
```

### Run Tests
```bash
# Backend
cd backend
pytest tests/ -v

# Frontend
cd frontend
npm test
```

## Troubleshooting

### Python Version Issues
```bash
# Use specific Python version
python3.11 -m venv venv
```

### Permission Errors (Linux/Mac)
```bash
# Fix script permissions
chmod +x start.sh
chmod +x backend/main.py
```

### Port Conflicts
```bash
# Find process using port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Kill process
taskkill /PID <pid> /F        # Windows
kill -9 <pid>                 # Linux/Mac
```

### Ollama Connection Issues
```bash
# Check Ollama status
systemctl status ollama  # Linux
# OR
ollama serve             # Manual start

# Test connection
curl http://localhost:11434/api/tags
```

## Next Steps

1. **Configure**: Edit `.env` files for customization
2. **Test**: Run the application and test recording
3. **Deploy**: See README.md for production deployment
4. **Extend**: Add more models and languages

## Support

For issues:
1. Check logs in `backend/logs/app.log`
2. Review terminal output for errors
3. Verify all dependencies are installed
4. Check port availability
5. Consult README.md and API documentation
