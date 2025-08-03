from typing import Any, Dict, List
from core.state import FinanceAgentState
from agents.llm_backend import LLMBackend

# LlamaIndex and Qdrant imports
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding

class LlamaIndexRAGRetriever:
    """
    Retriever using LlamaIndex and Qdrant for persistent vector search.
    """
    def __init__(self, qdrant_url: str = None, qdrant_api_key: str = None, collection_name: str = "finance_docs"):
        # Connect to Qdrant vector store (Cloud or local)
        if qdrant_url and qdrant_api_key:
            self.vector_store = QdrantVectorStore(
                url=qdrant_url,
                api_key=qdrant_api_key,
                collection_name=collection_name
            )
        else:
            self.vector_store = QdrantVectorStore(
                host="localhost",
                port=6333,
                collection_name=collection_name
            )
        self.index = VectorStoreIndex.from_vector_store(self.vector_store, embed_model=OpenAIEmbedding())

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        # Query the vector store
        results = self.index.query(query, top_k=top_k)
        docs = []
        for r in results:
            docs.append({
                "content": r.text,
                "source_url": r.metadata.get("source_url", "")
            })
        return docs

# Example usage in FinanceQAAgent (replace VectorizeRAGRetriever with LlamaIndexRAGRetriever)
# rag_retriever = LlamaIndexRAGRetriever(qdrant_host="localhost", qdrant_port=6333)
# agent = FinanceQAAgent(llm_backend, rag_retriever)
