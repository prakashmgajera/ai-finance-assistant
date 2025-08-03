import pytest
from unittest.mock import MagicMock
from agents.llamaindex_rag_retriever import LlamaIndexRAGRetriever
from qdrant_client import QdrantClient

@pytest.fixture
def retriever():
    mock_client = MagicMock(spec=QdrantClient)
    # Patch the retriever to use the mock client
    class MockLlamaIndexRAGRetriever(LlamaIndexRAGRetriever):
        def __init__(self):
            self.vector_store = MagicMock()
            self.index = MagicMock()
            # Mock index.query to return dummy results
            self.index.query = MagicMock(return_value=[
                MagicMock(text="Sample content", metadata={"source_url": "http://example.com"})
            ])
    return MockLlamaIndexRAGRetriever()

def test_retrieve_empty_query(retriever):
    results = retriever.retrieve("")
    assert isinstance(results, list)
    assert all("content" in r and "source_url" in r for r in results)

def test_retrieve_sample_query(retriever):
    results = retriever.retrieve("ETF basics")
    assert isinstance(results, list)
    assert all("content" in r and "source_url" in r for r in results)
