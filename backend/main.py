"""
Real-Time Speech Translation System - Main Application
FastAPI backend with Whisper STT, Ollama Translation, and Edge TTS
"""

import os
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from dotenv import load_dotenv
from loguru import logger

from app.services.stt_service import STTService
from app.services.translation_service import TranslationService
from app.services.tts_service_local import TTSService  # Using local TTS
from app.services.websocket_manager import WebSocketManager
from app.models.schemas import TranslationRequest, HealthResponse
from app.utils.audio_utils import validate_audio_file
from app.middleware.rate_limit import RateLimitMiddleware

# Load environment variables
load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logger.add("logs/app.log", rotation="500 MB", retention="10 days", level=LOG_LEVEL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("🚀 Starting Real-Time Speech Translation System")
    
    # Initialize services
    app.state.stt_service = STTService()
    app.state.translation_service = TranslationService()
    app.state.tts_service = TTSService()
    app.state.ws_manager = WebSocketManager()
    
    logger.info("✅ All services initialized successfully")
    
    yield
    
    # Cleanup
    logger.info("🛑 Shutting down services")


# Initialize FastAPI app
app = FastAPI(
    title="Real-Time Speech Translation API",
    description="Speech-to-Text-to-Speech translation using Whisper, Ollama, and Edge TTS",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting
app.add_middleware(RateLimitMiddleware)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with system status"""
    return HealthResponse(
        status="healthy",
        message="Real-Time Speech Translation System",
        version="1.0.0",
        services={
            "stt": "faster-whisper",
            "translation": "ollama",
            "tts": "edge-tts"
        }
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    # Check services without failing on Ollama timeout
    services = {
        "stt": "operational",
        "tts": "operational",
        "translation": "unknown"
    }
    
    try:
        # Try to check Ollama (with timeout tolerance)
        await app.state.translation_service.check_connection()
        services["translation"] = "operational"
    except Exception as e:
        logger.warning(f"Translation service check failed (continuing anyway): {e}")
        services["translation"] = "degraded"
    
    return HealthResponse(
        status="healthy",
        message="Core services operational",
        version="1.0.0",
        services=services
    )


@app.post("/api/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe audio file to text
    
    - **file**: Audio file (wav, mp3, m4a, etc.)
    
    Returns transcribed text and language
    """
    try:
        # Validate audio file
        await validate_audio_file(file)
        
        # Save temp file
        temp_path = Path(f"tmp/{file.filename}")
        temp_path.parent.mkdir(exist_ok=True)
        
        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)
        
        # Transcribe
        result = await app.state.stt_service.transcribe(str(temp_path))
        
        # Cleanup
        temp_path.unlink()
        
        return {
            "text": result["text"],
            "language": result["language"],
            "duration": result["duration"]
        }
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/translate")
async def translate_text(request: TranslationRequest):
    """
    Translate text from source to target language
    
    - **text**: Text to translate
    - **source_lang**: Source language code
    - **target_lang**: Target language code
    - **model**: Ollama model to use (optional)
    
    Returns translated text
    """
    try:
        translated = await app.state.translation_service.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            model=request.model
        )
        
        return {
            "translated_text": translated,
            "source_lang": request.source_lang,
            "target_lang": request.target_lang,
            "model": request.model or os.getenv("OLLAMA_MODEL", "qwen2:7b")
        }
        
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/speak")
async def text_to_speech(
    text: str,
    language: str = "en",
    voice: str = None
):
    """
    Convert text to speech
    
    - **text**: Text to convert
    - **language**: Language code
    - **voice**: Voice name (optional)
    
    Returns audio stream
    """
    try:
        audio_data = await app.state.tts_service.synthesize(
            text=text,
            language=language,
            voice=voice
        )
        
        return StreamingResponse(
            iter([audio_data]),
            media_type="audio/mpeg"
        )
        
    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/full-pipeline")
async def full_translation_pipeline(
    file: UploadFile = File(...),
    target_lang: str = "en",
    model: str = None,
    voice: str = None
):
    """
    Complete pipeline: STT → Translation → TTS
    
    - **file**: Audio file
    - **target_lang**: Target language
    - **model**: Translation model
    - **voice**: TTS voice
    
    Returns translated audio
    """
    try:
        # 1. Transcribe
        await validate_audio_file(file)
        temp_path = Path(f"tmp/{file.filename}")
        temp_path.parent.mkdir(exist_ok=True)
        
        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)
        
        stt_result = await app.state.stt_service.transcribe(str(temp_path))
        temp_path.unlink()
        
        # 2. Translate
        translated = await app.state.translation_service.translate(
            text=stt_result["text"],
            source_lang=stt_result["language"],
            target_lang=target_lang,
            model=model
        )
        
        # 3. Synthesize (with fallback if TTS fails)
        try:
            audio_data = await app.state.tts_service.synthesize(
                text=translated,
                language=target_lang,
                voice=voice
            )
        except Exception as tts_error:
            logger.warning(f"TTS failed, returning translation without audio: {tts_error}")
            audio_data = b""
        
        # Return empty audio if TTS produced nothing
        if not audio_data:
            logger.warning("No audio data, creating silent placeholder")
            # Return minimal valid MP3 (1 second silence)
            audio_data = b"\xff\xfb\x90\x00" * 100
        
        # URL-encode text for HTTP headers (to handle Unicode like Chinese)
        return StreamingResponse(
            iter([audio_data]),
            media_type="audio/wav",  # Local TTS outputs WAV
            headers={
                "X-Original-Text": quote(stt_result["text"]),
                "X-Translated-Text": quote(translated),
                "X-Source-Lang": stt_result["language"],
                "X-Target-Lang": target_lang,
                "X-TTS-Status": "ok" if len(audio_data) > 1000 else "failed"
            }
        )
        
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time translation
    
    Protocol:
    1. Client sends audio chunks
    2. Server transcribes + translates + synthesizes
    3. Server sends back audio chunks
    """
    await app.state.ws_manager.connect(websocket)
    
    try:
        while True:
            # Receive audio data
            data = await websocket.receive_json()
            
            if data.get("type") == "audio":
                # Process audio chunk
                result = await app.state.ws_manager.process_audio(
                    websocket=websocket,
                    audio_data=data.get("data"),
                    config=data.get("config", {})
                )
                
                # Send result
                await websocket.send_json(result)
            
            elif data.get("type") == "config":
                # Update configuration
                await app.state.ws_manager.update_config(
                    websocket=websocket,
                    config=data.get("config")
                )
            
    except WebSocketDisconnect:
        app.state.ws_manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        app.state.ws_manager.disconnect(websocket)


@app.get("/api/models")
async def list_available_models():
    """List available Ollama models"""
    try:
        models = await app.state.translation_service.list_models()
        return {"models": models}
    except Exception as e:
        logger.warning(f"Failed to list models (Ollama may not be running): {e}")
        # Return default model if Ollama is unavailable
        return {"models": [{"name": "qwen2.5:1.5b", "size": "986MB"}]}


@app.get("/api/languages")
async def list_supported_languages():
    """List supported languages"""
    return {
        "languages": {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi",
            "ru": "Russian",
            "tr": "Turkish",
            "vi": "Vietnamese",
            "th": "Thai"
        }
    }


@app.get("/api/voices")
async def list_available_voices(language: str = "en"):
    """List available TTS voices for language"""
    try:
        voices = await app.state.tts_service.list_voices(language)
        return {"voices": voices}
    except Exception as e:
        logger.error(f"Failed to list voices: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    WORKERS = int(os.getenv("WORKERS", 1))
    
    logger.info(f"🚀 Starting server on {HOST}:{PORT}")
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level=LOG_LEVEL.lower()
    )
