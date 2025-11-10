"""
Pytest configuration and fixtures
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_ollama_client(monkeypatch):
    """Mock Ollama client for testing"""
    class MockOllamaClient:
        async def generate(self, *args, **kwargs):
            return {"response": "Mocked translation"}
        
        async def list(self, *args, **kwargs):
            return {"models": [{"name": "qwen2:7b"}]}
    
    return MockOllamaClient()
