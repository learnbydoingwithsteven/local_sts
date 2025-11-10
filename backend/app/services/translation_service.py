"""
Translation Service using Ollama
Supports multiple small capable models
"""

import os
from typing import Optional, List, Dict
import asyncio

import ollama
from loguru import logger


class TranslationService:
    """Translation service using Ollama"""
    
    def __init__(self):
        """Initialize Ollama client"""
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.default_model = os.getenv("OLLAMA_MODEL", "qwen2:7b")
        
        # Initialize client
        self.client = ollama.AsyncClient(host=self.host)
        
        logger.info(f"Ollama client initialized: {self.host}")
        logger.info(f"Default model: {self.default_model}")
    
    async def check_connection(self) -> bool:
        """Check Ollama server connection"""
        try:
            models = await self.list_models()
            return len(models) > 0
        except Exception as e:
            logger.error(f"Ollama connection check failed: {e}")
            return False
    
    async def list_models(self) -> List[Dict]:
        """List available Ollama models"""
        try:
            response = await self.client.list()
            models = response.get('models', [])
            
            logger.info(f"Available models: {len(models)}")
            return models
            
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            raise
    
    async def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        model: Optional[str] = None
    ) -> str:
        """
        Translate text from source to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            model: Model name (uses default if None)
        
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return ""
        
        model_name = model or self.default_model
        
        # Create translation prompt
        prompt = self._create_translation_prompt(text, source_lang, target_lang)
        
        try:
            logger.info(f"Translating with {model_name}: {source_lang} → {target_lang}")
            
            # Call Ollama API
            response = await self.client.generate(
                model=model_name,
                prompt=prompt,
                options={
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "top_k": 40,
                    "num_predict": 512
                }
            )
            
            translated_text = response['response'].strip()
            
            # Clean up response (remove any explanations)
            translated_text = self._clean_translation(translated_text)
            
            logger.info(f"✅ Translation complete ({len(translated_text)} chars)")
            
            return translated_text
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            raise
    
    def _create_translation_prompt(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> str:
        """Create optimized translation prompt"""
        
        # Language name mapping
        lang_names = {
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
        
        source_name = lang_names.get(source_lang, source_lang.upper())
        target_name = lang_names.get(target_lang, target_lang.upper())
        
        prompt = f"""You are a professional translator. Translate the following text from {source_name} to {target_name}.

IMPORTANT RULES:
- Provide ONLY the translation
- Do NOT add explanations, notes, or comments
- Preserve the original meaning and tone
- Use natural, fluent language
- Maintain formatting if present

Text to translate:
{text}

Translation:"""
        
        return prompt
    
    def _clean_translation(self, text: str) -> str:
        """Clean translation output"""
        # Remove common prefixes
        prefixes = [
            "Translation:",
            "Here is the translation:",
            "The translation is:",
            "Translated text:",
        ]
        
        for prefix in prefixes:
            if text.lower().startswith(prefix.lower()):
                text = text[len(prefix):].strip()
        
        # Remove quotes if wrapped
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        if text.startswith("'") and text.endswith("'"):
            text = text[1:-1]
        
        return text.strip()
    
    async def translate_batch(
        self,
        texts: List[str],
        source_lang: str,
        target_lang: str,
        model: Optional[str] = None
    ) -> List[str]:
        """
        Translate multiple texts in parallel
        
        Args:
            texts: List of texts to translate
            source_lang: Source language
            target_lang: Target language
            model: Model name
        
        Returns:
            List of translated texts
        """
        tasks = [
            self.translate(text, source_lang, target_lang, model)
            for text in texts
        ]
        
        results = await asyncio.gather(*tasks)
        return results
    
    async def pull_model(self, model_name: str) -> None:
        """Pull a model from Ollama registry"""
        try:
            logger.info(f"Pulling model: {model_name}")
            
            response = await self.client.pull(model_name)
            
            logger.info(f"✅ Model pulled successfully: {model_name}")
            
        except Exception as e:
            logger.error(f"Failed to pull model: {e}")
            raise
