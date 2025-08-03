import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import pytest
from agents.llm_backend import LLMBackend

class MockResponse:
    def __init__(self, ok, json_data):
        self.ok = ok
        self._json = json_data
    def json(self):
        return self._json

def test_query_gemini_success(monkeypatch):
    def mock_post(url, headers, params, json):
        return MockResponse(True, {"candidates": [{"content": {"parts": [{"text": "Gemini answer"}]}}]})
    monkeypatch.setattr("requests.post", mock_post)
    backend = LLMBackend(provider="gemini", api_key="test")
    result = backend.query("Test prompt")
    assert result == "Gemini answer"

def test_query_gemini_failure(monkeypatch):
    def mock_post(url, headers, params, json):
        return MockResponse(False, {})
    monkeypatch.setattr("requests.post", mock_post)
    backend = LLMBackend(provider="gemini", api_key="test")
    result = backend.query("Test prompt")
    assert result.startswith("Error:")

def test_query_openai_success(monkeypatch):
    def mock_post(url, headers, json):
        return MockResponse(True, {"choices": [{"message": {"content": "OpenAI answer"}}]})
    monkeypatch.setattr("requests.post", mock_post)
    backend = LLMBackend(provider="openai", api_key="test")
    result = backend.query("Test prompt")
    assert result == "OpenAI answer"

def test_query_openai_failure(monkeypatch):
    def mock_post(url, headers, json):
        return MockResponse(False, {})
    monkeypatch.setattr("requests.post", mock_post)
    backend = LLMBackend(provider="openai", api_key="test")
    result = backend.query("Test prompt")
    assert result.startswith("Error:")

def test_query_invalid_provider():
    backend = LLMBackend(provider="invalid", api_key="test")
    try:
        backend.query("Test prompt")
    except ValueError as e:
        assert "Unsupported provider" in str(e)
    else:
        assert False, "Should have raised ValueError"
