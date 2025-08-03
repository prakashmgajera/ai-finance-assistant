from typing import Any, Dict, List, Optional
from core.state import FinanceAgentState
from agents.llm_backend import LLMBackend

class VectorizeRAGRetriever:
    _memory_cache = {}
    """
    Simple retriever that returns relevant URLs for finance concepts.
    """
    def __init__(self, token: str):
        import vectorize_client as v
        # You must set these IDs for your pipeline and data
        self.PIPELINE_ID = "dacc2def-253e-4fa3-b8fd-6e9e6825b9cd"
        self.DATA_ID = "aip000ea-3afc-45bc-a204-f306d6188a2b"
        self.api = v.ApiClient(v.Configuration(access_token=token, host="https://api.vectorize.io/v1"))
        self.pipelines = v.PipelinesApi(self.api)

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        # Check memory cache first
        if query in self._memory_cache:
            return self._memory_cache[query]
        import vectorize_client as v
        try:
            response = self.pipelines.retrieve_documents(
                self.PIPELINE_ID,
                self.DATA_ID,
                v.RetrieveDocumentsRequest(
                    question=query,
                    num_results=5,
                )
            )
            results = []
            for doc in response.documents:
                content = doc.get('text', '')
                url = doc.get('source_url', '')
                results.append({"content": content, "source_url": url})
            # Save to memory cache
            self._memory_cache[query] = results
            return results
        except Exception as e:
            return [{"content": f"Error retrieving documents: {e}", "source_url": ""}]
from agents.llamaindex_rag_retriever import LlamaIndexRAGRetriever

class FinanceQAAgent:
    """
    Answers finance and investment concept questions using LLM and RAG, cites sources.
    """
    def __init__(self, llm_backend: LLMBackend, rag_retriever: LlamaIndexRAGRetriever):
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
