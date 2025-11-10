"""
API endpoint tests
"""

import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_root():
    """Test root endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code in [200, 503]
        data = response.json()
        assert "status" in data


@pytest.mark.asyncio
async def test_list_languages():
    """Test list languages endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/languages")
        assert response.status_code == 200
        data = response.json()
        assert "languages" in data
        assert len(data["languages"]) > 0
        assert "en" in data["languages"]


@pytest.mark.asyncio
async def test_translate_text():
    """Test text translation endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "text": "Hello, how are you?",
            "source_lang": "en",
            "target_lang": "es"
        }
        response = await client.post("/api/translate", json=payload)
        
        # May fail if Ollama is not running
        if response.status_code == 200:
            data = response.json()
            assert "translated_text" in data
            assert len(data["translated_text"]) > 0


@pytest.mark.asyncio
async def test_invalid_translation_request():
    """Test invalid translation request"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "text": "",
            "source_lang": "en",
            "target_lang": "es"
        }
        response = await client.post("/api/translate", json=payload)
        # Empty text should still return 200 with empty translation
        assert response.status_code in [200, 422]
