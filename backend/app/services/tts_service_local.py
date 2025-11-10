"""
Text-to-Speech Service using Local TTS (pyttsx3)
Fully offline, no API dependencies
"""

import os
import tempfile
from typing import Optional
from pathlib import Path

import pyttsx3
from loguru import logger


class TTSService:
    """Text-to-Speech service using local TTS engine"""
    
    def __init__(self):
        """Initialize local TTS service"""
        try:
            self.engine = pyttsx3.init()
            
            # Configure default settings
            rate = self.engine.getProperty('rate')
            self.engine.setProperty('rate', rate - 20)  # Slightly slower
            
            volume = self.engine.getProperty('volume')
            self.engine.setProperty('volume', 1.0)  # Max volume
            
            # Get available voices
            self.voices = self.engine.getProperty('voices')
            
            # Set default voice (female if available)
            if len(self.voices) > 1:
                self.engine.setProperty('voice', self.voices[1].id)  # Usually female
            
            logger.info(f"✅ Local TTS initialized with {len(self.voices)} voices")
            
        except Exception as e:
            logger.error(f"Failed to initialize TTS: {e}")
            raise
    
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
            language: Language code (used for voice selection)
            voice: Voice name (optional)
            rate: Speech rate (optional)
            volume: Volume (optional)
        
        Returns:
            Audio data as bytes (WAV format)
        """
        if not text or not text.strip():
            logger.warning("Empty text, returning silence")
            return self._create_silence()
        
        try:
            logger.info(f"Synthesizing speech: {len(text)} chars")
            
            # Create temp file for audio
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            # Select voice based on language if needed
            if language and not voice:
                self._set_voice_for_language(language)
            
            # Generate speech
            self.engine.save_to_file(text, temp_path)
            self.engine.runAndWait()
            
            # Read audio data
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            # Clean up
            os.unlink(temp_path)
            
            logger.info(f"✅ Speech synthesized ({len(audio_data)} bytes)")
            
            return audio_data
            
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            # Return silence instead of crashing
            return self._create_silence()
    
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
        Synthesize text and save to file
        
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
        try:
            audio_data = await self.synthesize(text, language, voice, rate, volume)
            
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            
            logger.info(f"Audio saved to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to save audio: {e}")
            raise
    
    def _set_voice_for_language(self, language: str):
        """Set appropriate voice for language"""
        # Map language codes to voice preferences
        lang_map = {
            'en': 'english',
            'es': 'spanish',
            'fr': 'french',
            'de': 'german',
            'it': 'italian',
            'pt': 'portuguese',
            'zh': 'chinese',
            'ja': 'japanese',
            'ko': 'korean'
        }
        
        lang_keyword = lang_map.get(language, 'english').lower()
        
        # Try to find matching voice
        for voice in self.voices:
            if lang_keyword in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                logger.info(f"Selected voice: {voice.name}")
                return
        
        # Use default if no match
        logger.warning(f"No voice found for {language}, using default")
    
    def _create_silence(self) -> bytes:
        """Create 1 second of silence as WAV"""
        # WAV header for 1 second of silence (16-bit, 16kHz, mono)
        sample_rate = 16000
        duration = 1
        num_samples = sample_rate * duration
        
        # WAV header (44 bytes)
        header = bytearray()
        header.extend(b'RIFF')
        header.extend((36 + num_samples * 2).to_bytes(4, 'little'))
        header.extend(b'WAVE')
        header.extend(b'fmt ')
        header.extend((16).to_bytes(4, 'little'))
        header.extend((1).to_bytes(2, 'little'))  # PCM
        header.extend((1).to_bytes(2, 'little'))  # Mono
        header.extend(sample_rate.to_bytes(4, 'little'))
        header.extend((sample_rate * 2).to_bytes(4, 'little'))
        header.extend((2).to_bytes(2, 'little'))
        header.extend((16).to_bytes(2, 'little'))
        header.extend(b'data')
        header.extend((num_samples * 2).to_bytes(4, 'little'))
        
        # Silence data (all zeros)
        silence = bytes(num_samples * 2)
        
        return bytes(header) + silence
    
    def list_voices(self) -> list:
        """Get list of available voices"""
        return [
            {
                "id": voice.id,
                "name": voice.name,
                "languages": voice.languages if hasattr(voice, 'languages') else [],
                "gender": voice.gender if hasattr(voice, 'gender') else "unknown"
            }
            for voice in self.voices
        ]
    
    def get_recommended_voices(self, language: str = "en") -> list:
        """Get recommended voices for language"""
        all_voices = self.list_voices()
        
        # Filter by language if possible
        matching = [v for v in all_voices if language.lower() in str(v.get('languages', [])).lower()]
        
        if matching:
            return matching[:3]  # Top 3
        
        return all_voices[:3]  # Default top 3
