"""
Speech-to-Text Service using OpenAI Whisper
"""

import os
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List
import io

import whisper
from loguru import logger


class STTService:
    """Speech-to-Text service using OpenAI Whisper"""
    
    def __init__(self):
        """Initialize OpenAI Whisper model"""
        model_name = os.getenv("WHISPER_MODEL", "base")
        
        logger.info(f"Initializing Whisper model: {model_name}")
        
        try:
            self.model = whisper.load_model(model_name)
            logger.info("✅ Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    async def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        task: str = "transcribe"
    ) -> Dict:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            language: Language code (auto-detect if None)
            task: 'transcribe' or 'translate'
        
        Returns:
            Dictionary with transcription results
        """
        try:
            logger.info(f"Transcribing audio file: {audio_path}")
            
            # Transcribe with OpenAI Whisper
            result = self.model.transcribe(
                str(audio_path),
                language=language,
                fp16=False  # Use FP32 on CPU
            )
            
            text = result["text"]
            detected_language = result.get("language", language or "en")
            
            logger.info(f"Transcription complete. Language: {detected_language}")
            
            return {
                "text": text.strip(),
                "language": detected_language,
                "confidence": 0.9  # OpenAI Whisper doesn't provide confidence
            }
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise
    
    async def transcribe_audio_data(
        self,
        audio_data: bytes,
        sample_rate: int = 16000,
        language: Optional[str] = None
    ) -> Dict:
        """
        Transcribe audio data (bytes) directly
        
        Args:
            audio_data: Audio bytes
            sample_rate: Sample rate
            language: Language code
        
        Returns:
            Dictionary with transcription results
        """
        try:
            # Save audio data to temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            # Transcribe using the temp file
            result = await self.transcribe(temp_path, language=language)
            
            # Clean up temp file
            os.unlink(temp_path)
            
            return result
            
        except Exception as e:
            logger.error(f"Audio data transcription failed: {e}")
            raise
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return [
            "en", "zh", "de", "es", "ru", "ko", "fr", "ja", "pt", "tr", "pl", "ca",
            "nl", "ar", "sv", "it", "id", "hi", "fi", "vi", "he", "uk", "el", "ms",
            "cs", "ro", "da", "hu", "ta", "no", "th", "ur", "hr", "bg", "lt", "la",
            "mi", "ml", "cy", "sk", "te", "fa", "lv", "bn", "sr", "az", "sl", "kn",
            "et", "mk", "br", "eu", "is", "hy", "ne", "mn", "bs", "kk", "sq", "sw",
            "gl", "mr", "pa", "si", "km", "sn", "yo", "so", "af", "oc", "ka", "be",
            "tg", "sd", "gu", "am", "yi", "lo", "uz", "fo", "ht", "ps", "tk", "nn",
            "mt", "sa", "lb", "my", "bo", "tl", "mg", "as", "tt", "haw", "ln", "ha",
            "ba", "jw", "su"
        ]
