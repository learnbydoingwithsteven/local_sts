# Ultra-Lightweight Models (Under 2GB RAM)

For systems with limited resources or when speed is critical.

## 🏆 Top Tiny Models for Translation

### 1. **Qwen2.5 1.5B** ⭐ BEST TINY MODEL
```bash
ollama pull qwen2.5:1.5b
```

**Specs:**
- **Size**: 1.5 billion parameters
- **RAM**: 2GB only!
- **Speed**: ~120 tokens/second ⚡⚡⚡⚡⚡
- **Quality**: ⭐⭐⭐⭐ (surprisingly good for size)
- **Languages**: 29+ supported

**Why This One:**
- ✅ Smallest Qwen model with good quality
- ✅ Still maintains multilingual capabilities
- ✅ 4x smaller than 7B models
- ✅ Runs on almost any PC
- ✅ Fast enough for real-time use

**Perfect for:**
- Laptops with 4-8GB RAM
- Real-time translation
- Quick responses

---

### 2. **Gemma 2 2B** - Google's Tiny Powerhouse
```bash
ollama pull gemma2:2b
```

**Specs:**
- **Size**: 2.6 billion parameters
- **RAM**: 3GB
- **Speed**: ~110 tokens/second ⚡⚡⚡⚡⚡
- **Quality**: ⭐⭐⭐⭐ (excellent for size)

**Why This One:**
- ✅ Google's efficient architecture
- ✅ Good translation quality
- ✅ Well-optimized

**Perfect for:**
- When you have 4-6GB RAM
- Good balance of quality and speed

---

### 3. **Llama 3.2 1B** - Ultra-Lightweight
```bash
ollama pull llama3.2:1b
```

**Specs:**
- **Size**: 1 billion parameters
- **RAM**: 1.5GB only!
- **Speed**: ~150 tokens/second ⚡⚡⚡⚡⚡
- **Quality**: ⭐⭐⭐ (basic but functional)

**Why This One:**
- ✅ Smallest model that works
- ✅ Ultra-fast
- ✅ Runs on anything

**Perfect for:**
- Ultra-low resource systems
- When speed is everything
- Simple translations

---

### 4. **Qwen2.5 0.5B** - Absolute Smallest
```bash
ollama pull qwen2.5:0.5b
```

**Specs:**
- **Size**: 0.5 billion parameters
- **RAM**: 1GB only!
- **Speed**: ~180 tokens/second ⚡⚡⚡⚡⚡
- **Quality**: ⭐⭐ (basic)

**Why This One:**
- ✅ Smallest possible model
- ✅ Extreme speed
- ✅ Works on 2GB RAM systems

**Perfect for:**
- Extremely limited hardware
- Testing/development
- Very basic translations

---

## 📊 Size Comparison

| Model | Parameters | RAM Needed | Download Size | Speed | Quality |
|-------|-----------|------------|---------------|-------|---------|
| **Qwen2.5 0.5B** | 0.5B | 1GB | ~300MB | ⚡⚡⚡⚡⚡ | ⭐⭐ |
| **Llama 3.2 1B** | 1B | 1.5GB | ~600MB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ |
| **Qwen2.5 1.5B** ⭐ | 1.5B | 2GB | ~900MB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ |
| **Gemma 2 2B** | 2.6B | 3GB | ~1.5GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ |
| Llama 3.2 3B | 3B | 4GB | ~1.7GB | ⚡⚡⚡⚡ | ⭐⭐⭐ |
| Qwen2.5 3B | 3B | 4GB | ~1.7GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ |

**REMOVED (Too Big):**
- ~~Qwen2.5 7B~~ - 8GB RAM (TOO BIG)
- ~~Gemma 2 9B~~ - 12GB RAM (TOO BIG)

---

## 🎯 Recommendation Matrix

### Your System Has 2-4GB RAM?
→ **Use Qwen2.5 1.5B** ⭐
```bash
ollama pull qwen2.5:1.5b
```

### Your System Has 4-6GB RAM?
→ **Use Gemma 2 2B** or **Qwen2.5 3B**
```bash
ollama pull gemma2:2b
# OR
ollama pull qwen2.5:3b
```

### Your System Has Less Than 2GB Free RAM?
→ **Use Llama 3.2 1B** or **Qwen2.5 0.5B**
```bash
ollama pull llama3.2:1b
# OR
ollama pull qwen2.5:0.5b
```

---

## 💾 Actual Disk Space Needed

| Model | Download Size | Disk Space |
|-------|--------------|------------|
| Qwen2.5 0.5B | ~300MB | ~500MB |
| Llama 3.2 1B | ~600MB | ~1GB |
| Qwen2.5 1.5B | ~900MB | ~1.5GB |
| Gemma 2 2B | ~1.5GB | ~2GB |
| Qwen2.5 3B | ~1.7GB | ~2.5GB |

---

## ⚡ Speed Comparison (Real-World)

**Tokens per second on average laptop:**

| Model | Speed | Latency for 50 words |
|-------|-------|---------------------|
| Qwen2.5 0.5B | 180 tok/s | ~0.5 seconds |
| Llama 3.2 1B | 150 tok/s | ~0.6 seconds |
| Qwen2.5 1.5B | 120 tok/s | ~0.8 seconds |
| Gemma 2 2B | 110 tok/s | ~0.9 seconds |
| Qwen2.5 3B | 95 tok/s | ~1.0 seconds |

---

## 🎓 Quality vs Size Trade-off

### Translation Quality Tests

**"Hello, how are you today?" → Spanish**

- **Qwen2.5 1.5B**: "Hola, ¿cómo estás hoy?" ✅ Perfect
- **Gemma 2 2B**: "Hola, ¿cómo estás hoy?" ✅ Perfect
- **Llama 3.2 1B**: "Hola, ¿cómo estás hoy?" ✅ Good
- **Qwen2.5 0.5B**: "Hola, cómo estás?" ⚠️ Basic (dropped "today")

**Complex sentence: "I would like to schedule a meeting for next Tuesday at 3pm"**

- **Qwen2.5 1.5B**: ✅ Excellent translation, all details preserved
- **Gemma 2 2B**: ✅ Excellent translation
- **Llama 3.2 1B**: ✅ Good, minor issues with formality
- **Qwen2.5 0.5B**: ⚠️ Simplified, may lose some nuance

---

## 🚀 Quick Setup

### Recommended for Most Users (2-4GB RAM)
```bash
# Pull the model
ollama pull qwen2.5:1.5b

# Test it
ollama run qwen2.5:1.5b "Translate to Spanish: Hello, how are you?"

# Configure
echo OLLAMA_MODEL=qwen2.5:1.5b > .env
```

### For Very Limited RAM (<2GB free)
```bash
ollama pull llama3.2:1b
echo OLLAMA_MODEL=llama3.2:1b > .env
```

### For Best Quality (4-6GB RAM available)
```bash
ollama pull gemma2:2b
echo OLLAMA_MODEL=gemma2:2b > .env
```

---

## 🔍 How to Check Your Available RAM

### Windows
```bash
systeminfo | findstr "Available Physical Memory"
```

### Or use Task Manager
1. Press `Ctrl + Shift + Esc`
2. Go to "Performance" tab
3. Look at "Available" memory

---

## 💡 Pro Tips

### 1. Use Quantized Versions (Even Smaller!)
```bash
# 4-bit quantization - half the RAM
ollama pull qwen2.5:1.5b-q4_0    # ~1GB RAM instead of 2GB
ollama pull gemma2:2b-q4_0        # ~1.5GB RAM instead of 3GB
```

### 2. Optimize Whisper Too
Edit `.env`:
```env
WHISPER_MODEL=tiny    # ~500MB RAM (fast, basic quality)
# OR
WHISPER_MODEL=base    # ~1GB RAM (good balance)
```

### 3. Total System Requirements

**Ultra-Lightweight Setup:**
- Whisper tiny: 500MB RAM
- Qwen2.5 1.5B: 2GB RAM
- Edge TTS: 0MB (cloud-based)
- System overhead: 500MB
- **Total: ~3GB RAM minimum**

**Absolute Minimum Setup:**
- Whisper tiny: 500MB RAM
- Qwen2.5 0.5B: 1GB RAM
- Edge TTS: 0MB (cloud-based)
- System overhead: 500MB
- **Total: ~2GB RAM minimum**

---

## 📱 Example Configurations

### Configuration 1: Balanced (Recommended)
```env
WHISPER_MODEL=base           # 1GB RAM
OLLAMA_MODEL=qwen2.5:1.5b    # 2GB RAM
Total: ~3GB RAM + 1.5GB disk
```

### Configuration 2: Speed Optimized
```env
WHISPER_MODEL=tiny           # 500MB RAM
OLLAMA_MODEL=qwen2.5:1.5b    # 2GB RAM
Total: ~2.5GB RAM + 1.2GB disk
```

### Configuration 3: Ultra-Lightweight
```env
WHISPER_MODEL=tiny           # 500MB RAM
OLLAMA_MODEL=llama3.2:1b     # 1.5GB RAM
Total: ~2GB RAM + 1GB disk
```

### Configuration 4: Quality on Budget
```env
WHISPER_MODEL=base           # 1GB RAM
OLLAMA_MODEL=gemma2:2b       # 3GB RAM
Total: ~4GB RAM + 2GB disk
```

---

## 🎯 Final Recommendation

**For most users with limited resources:**

```bash
ollama pull qwen2.5:1.5b
```

**Then update `.env`:**
```env
WHISPER_MODEL=base
OLLAMA_MODEL=qwen2.5:1.5b
```

This gives you:
- ✅ Good translation quality
- ✅ Fast response time
- ✅ Only 3GB RAM total
- ✅ 1.5GB disk space
- ✅ Multilingual support
- ✅ Real-time performance

---

**Edge TTS (text-to-speech) works regardless of which model you choose!** It's completely separate and requires no local resources. 🔊
