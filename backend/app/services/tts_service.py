"""
Text-to-Speech Service using Edge TTS
Fast and high-quality voice synthesis
"""

import os
from typing import Optional, List, Dict
import asyncio
from io import BytesIO

import edge_tts
from loguru import logger


class TTSService:
    """Text-to-Speech service using Edge TTS"""
    
    def __init__(self):
        """Initialize TTS service"""
        self.default_voice = os.getenv("TTS_VOICE", "en-US-AriaNeural")
        self.default_rate = os.getenv("TTS_RATE", "+0%")
        self.default_volume = os.getenv("TTS_VOLUME", "+0%")
        
        logger.info(f"TTS service initialized with voice: {self.default_voice}")
    
    async def synthesize(
        self,
        text: str,
        language: str = "en",
        voice: Optional[str] = None,
        rate: Optional[str] = None,
        volume: Optional[str] = None
    ) -> bytes:
        """
        Convert text to speech
        
        Args:
            text: Text to synthesize
            language: Language code
            voice: Voice name (auto-select if None)
            rate: Speech rate (+/-50%)
            volume: Volume (+/-50%)
        
        Returns:
            Audio data as bytes (MP3 format)
        """
        if not text or not text.strip():
            return b""
        
        # Select voice
        if not voice:
            voice = self._get_voice_for_language(language)
        
        rate = rate or self.default_rate
        volume = volume or self.default_volume
        
        try:
            logger.info(f"Synthesizing speech: {voice} ({len(text)} chars)")
            
            # Create TTS communicator
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=rate,
                volume=volume
            )
            
            # Collect audio chunks
            audio_chunks = []
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_chunks.append(chunk["data"])
            
            # Combine chunks
            audio_data = b"".join(audio_chunks)
            
            logger.info(f"✅ Speech synthesized ({len(audio_data)} bytes)")
            
            return audio_data
            
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            # Return empty audio instead of crashing
            # This allows translation to still work even if TTS fails
            logger.warning("Returning empty audio due to TTS error")
            return b""
    
    async def synthesize_to_file(
        self,
        text: str,
        output_path: str,
        language: str = "en",
        voice: Optional[str] = None,
        rate: Optional[str] = None,
        volume: Optional[str] = None
    ) -> str:
        """
        Synthesize speech and save to file
        
        Args:
            text: Text to synthesize
            output_path: Output file path
            language: Language code
            voice: Voice name
            rate: Speech rate
            volume: Volume
        
        Returns:
            Output file path
        """
        audio_data = await self.synthesize(text, language, voice, rate, volume)
        
        with open(output_path, "wb") as f:
            f.write(audio_data)
        
        logger.info(f"Audio saved to: {output_path}")
        
        return output_path
    
    async def list_voices(self, language: Optional[str] = None) -> List[Dict]:
        """
        List available voices
        
        Args:
            language: Filter by language code (optional)
        
        Returns:
            List of voice information
        """
        try:
            voices = await edge_tts.list_voices()
            
            # Filter by language if specified
            if language:
                voices = [v for v in voices if v["Locale"].startswith(language)]
            
            # Format voice info
            voice_list = []
            for voice in voices:
                voice_list.append({
                    "name": voice["ShortName"],
                    "gender": voice["Gender"],
                    "locale": voice["Locale"],
                    "language": voice["Locale"].split("-")[0],
                    "full_name": voice["FriendlyName"]
                })
            
            logger.info(f"Found {len(voice_list)} voices for language: {language or 'all'}")
            
            return voice_list
            
        except Exception as e:
            logger.error(f"Failed to list voices: {e}")
            raise
    
    def _get_voice_for_language(self, language: str) -> str:
        """Get recommended voice for language"""
        
        # Voice recommendations (high-quality neural voices)
        voice_map = {
            "en": "en-US-AriaNeural",
            "es": "es-ES-ElviraNeural",
            "fr": "fr-FR-DeniseNeural",
            "de": "de-DE-KatjaNeural",
            "it": "it-IT-ElsaNeural",
            "pt": "pt-BR-FranciscaNeural",
            "zh": "zh-CN-XiaoxiaoNeural",
            "ja": "ja-JP-NanamiNeural",
            "ko": "ko-KR-SunHiNeural",
            "ar": "ar-SA-ZariyahNeural",
            "hi": "hi-IN-SwaraNeural",
            "ru": "ru-RU-SvetlanaNeural",
            "tr": "tr-TR-EmelNeural",
            "vi": "vi-VN-HoaiMyNeural",
            "th": "th-TH-PremwadeeNeural"
        }
        
        return voice_map.get(language, self.default_voice)
    
    async def get_voice_info(self, voice_name: str) -> Optional[Dict]:
        """Get information about a specific voice"""
        voices = await edge_tts.list_voices()
        
        for voice in voices:
            if voice["ShortName"] == voice_name:
                return {
                    "name": voice["ShortName"],
                    "gender": voice["Gender"],
                    "locale": voice["Locale"],
                    "language": voice["Locale"].split("-")[0],
                    "full_name": voice["FriendlyName"],
                    "styles": voice.get("StyleList", []),
                    "roles": voice.get("RolePlayList", [])
                }
        
        return None
