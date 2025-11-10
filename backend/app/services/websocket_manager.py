"""
WebSocket Manager for Real-Time Communication
Handles audio streaming and processing
"""

import base64
from typing import Dict, List, Optional
from fastapi import WebSocket
from loguru import logger
import asyncio


class WebSocketManager:
    """Manager for WebSocket connections"""
    
    def __init__(self):
        """Initialize WebSocket manager"""
        self.active_connections: List[WebSocket] = []
        self.connection_configs: Dict[WebSocket, Dict] = {}
        logger.info("WebSocket manager initialized")
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        
        # Default configuration
        self.connection_configs[websocket] = {
            "source_lang": "auto",
            "target_lang": "en",
            "model": None,
            "voice": None,
            "buffer_size": 4096
        }
        
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
        
        # Send welcome message
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "message": "WebSocket connection established"
        })
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        if websocket in self.connection_configs:
            del self.connection_configs[websocket]
        
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def update_config(self, websocket: WebSocket, config: Dict):
        """Update configuration for a connection"""
        if websocket in self.connection_configs:
            self.connection_configs[websocket].update(config)
            logger.info(f"Config updated: {config}")
            
            await websocket.send_json({
                "type": "config",
                "status": "updated",
                "config": self.connection_configs[websocket]
            })
    
    async def process_audio(
        self,
        websocket: WebSocket,
        audio_data: str,
        config: Optional[Dict] = None
    ) -> Dict:
        """
        Process audio data through the pipeline
        
        Args:
            websocket: WebSocket connection
            audio_data: Base64 encoded audio data
            config: Optional configuration override
        
        Returns:
            Processing result dictionary
        """
        try:
            # Get configuration
            ws_config = self.connection_configs.get(websocket, {})
            if config:
                ws_config.update(config)
            
            # Decode audio data
            audio_bytes = base64.b64decode(audio_data)
            
            # Import services (lazy import to avoid circular dependencies)
            from app.services.stt_service import STTService
            from app.services.translation_service import TranslationService
            from app.services.tts_service import TTSService
            
            # Get or create service instances
            # Note: In production, these should be injected from app state
            stt_service = STTService()
            translation_service = TranslationService()
            tts_service = TTSService()
            
            # 1. Transcribe
            logger.info("Processing audio chunk...")
            transcription = await stt_service.transcribe_audio_data(
                audio_bytes,
                language=ws_config.get("source_lang") if ws_config.get("source_lang") != "auto" else None
            )
            
            original_text = transcription["text"]
            source_lang = transcription["language"]
            
            # 2. Translate
            target_lang = ws_config.get("target_lang", "en")
            
            if source_lang != target_lang:
                translated_text = await translation_service.translate(
                    text=original_text,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    model=ws_config.get("model")
                )
            else:
                translated_text = original_text
            
            # 3. Synthesize
            audio_output = await tts_service.synthesize(
                text=translated_text,
                language=target_lang,
                voice=ws_config.get("voice")
            )
            
            # Encode audio output
            audio_output_b64 = base64.b64encode(audio_output).decode('utf-8')
            
            logger.info(f"✅ Pipeline complete: {source_lang} → {target_lang}")
            
            return {
                "type": "result",
                "status": "success",
                "data": {
                    "original_text": original_text,
                    "translated_text": translated_text,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "audio": audio_output_b64,
                    "duration": transcription["duration"]
                }
            }
            
        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            return {
                "type": "error",
                "status": "failed",
                "message": str(e)
            }
    
    async def broadcast(self, message: Dict):
        """Broadcast message to all connections"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Broadcast error: {e}")
    
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)
