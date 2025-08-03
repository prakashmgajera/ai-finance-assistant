
import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'src')))
from agents.vectorize_rag_retriever import VectorizeRAGRetriever

def test_vectorize_rag_retriever_success(monkeypatch):
    # Mock the environment variable for TOKEN
    monkeypatch.setenv("TOKEN", "dummy_token")
    # Mock the vectorize_client and its response
    class DummyDoc(dict):
        def get(self, k, default=None):
            return super().get(k, default)
    class DummyResponse:
        documents = [
            DummyDoc({"text": "Sample answer 1", "source_url": "https://example.com/1"}),
            DummyDoc({"text": "Sample answer 2", "source_url": "https://example.com/2"})
        ]
    class DummyPipelinesApi:
        def retrieve_documents(self, pipeline_id, data_id, req):
            return DummyResponse()
    class DummyApiClient:
        def __init__(self, *args, **kwargs):
            pass
    class DummyConfig:
        def __init__(self, **kwargs):
            pass
    import sys
    sys.modules["vectorize_client"] = type("vectorize_client", (), {
        "ApiClient": DummyApiClient,
        "Configuration": DummyConfig,
        "PipelinesApi": lambda api: DummyPipelinesApi(),
        "RetrieveDocumentsRequest": lambda **kwargs: kwargs
    })
    retriever = VectorizeRAGRetriever(token="dummy")
    results = retriever.retrieve("What is investing?")
    assert len(results) == 2
    assert results[0]["content"] == "Sample answer 1"
    assert results[0]["source_url"] == "https://example.com/1"
    assert results[1]["content"] == "Sample answer 2"
    assert results[1]["source_url"] == "https://example.com/2"

def test_vectorize_rag_retriever_error(monkeypatch):
    monkeypatch.setenv("TOKEN", "dummy_token")
    class DummyPipelinesApi:
        def retrieve_documents(self, pipeline_id, data_id, req):
            raise Exception("API error")
    class DummyApiClient:
        def __init__(self, *args, **kwargs):
            pass
    class DummyConfig:
        def __init__(self, **kwargs):
            pass
    import sys
    sys.modules["vectorize_client"] = type("vectorize_client", (), {
        "ApiClient": DummyApiClient,
        "Configuration": DummyConfig,
        "PipelinesApi": lambda api: DummyPipelinesApi(),
        "RetrieveDocumentsRequest": lambda **kwargs: kwargs
    })
    retriever = VectorizeRAGRetriever(token="dummy")
    results = retriever.retrieve("What is investing?")
    assert len(results) == 1
    assert results[0]["content"].startswith("Error retrieving documents:")
