
from typing import Any, Dict, List, Optional
from core.state import FinanceAgentState
from agents.llm_backend import LLMBackend

class SimpleRAGRetriever:
    """
    Simple retriever that returns relevant URLs for finance concepts.
    """
    SOURCES = [
        "https://www.investopedia.com/",
        "https://www.bankrate.com/investing/",
        "https://www.nerdwallet.com/h/category/personal-finance",
        "https://smartasset.com/investing",
        "https://zerodha.com/varsity/"
    ]
    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        # In production, use embeddings/vector search. Here, return all sources.
        return [{"content": f"See these sources for '{query}'.", "source_url": url} for url in self.SOURCES]

class FinanceQAAgent:
    """
    Answers finance and investment concept questions using LLM and RAG, cites sources.
    """
    def __init__(self, llm_backend: LLMBackend, rag_retriever: SimpleRAGRetriever):
        self.llm_backend = llm_backend
        self.rag_retriever = rag_retriever

    def process_query(self, state: FinanceAgentState) -> FinanceAgentState:
        query = state["user_query"]
        # Get LLM answer
        llm_response = self.llm_backend.query(query)
        # Retrieve sources using RAG
        results = self.rag_retriever.retrieve(query)
        sources = [r["source_url"] for r in results]
        response = llm_response
        if sources:
            response += "\n\nSources:\n" + "\n".join(sources)
        # Update state
        state["agent_response"] = response
        state["conversational_history"].append({
            "agent": "FinanceQA",
            "query": query,
            "response": response,
            "sources": sources
        })
        return state
