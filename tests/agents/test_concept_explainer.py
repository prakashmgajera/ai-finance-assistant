
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import pytest
from agents.concept_explainer import FinanceQAAgent, SimpleRAGRetriever
from agents.llm_backend import LLMBackend
from core.state import FinanceAgentState

class MockLLMBackend(LLMBackend):
    def __init__(self, provider="mock", api_key=None):
        super().__init__(provider, api_key)
    def query(self, prompt: str) -> str:
        return f"Mocked LLM response for: {prompt}"

class MockRAGRetriever(SimpleRAGRetriever):
    def retrieve(self, query: str):
        return [{"content": f"Mocked source for {query}", "source_url": "https://mocksource.com"}]

def test_finance_qa_agent_basic():
    llm = MockLLMBackend()
    rag = MockRAGRetriever()
    agent = FinanceQAAgent(llm, rag)
    state = FinanceAgentState(user_query="What is an ETF?", conversational_history=[])
    result = agent.process_query(state)
    assert "Mocked LLM response for: What is an ETF?" in result["agent_response"]
    assert "https://mocksource.com" in result["agent_response"]
    assert len(result["conversational_history"]) == 1
    assert result["conversational_history"][0]["query"] == "What is an ETF?"

def test_finance_qa_agent_sources():
    llm = MockLLMBackend()
    rag = MockRAGRetriever()
    agent = FinanceQAAgent(llm, rag)
    state = FinanceAgentState(user_query="Explain stocks", conversational_history=[])
    result = agent.process_query(state)
    assert "Sources:" in result["agent_response"]
    assert "https://mocksource.com" in result["agent_response"]

def test_finance_qa_agent_history_accumulation():
    llm = MockLLMBackend()
    rag = MockRAGRetriever()
    agent = FinanceQAAgent(llm, rag)
    state = FinanceAgentState(user_query="First question", conversational_history=[])
    result1 = agent.process_query(state)
    state2 = FinanceAgentState(user_query="Second question", conversational_history=result1["conversational_history"])
    result2 = agent.process_query(state2)
    assert len(result2["conversational_history"]) == 2
    assert result2["conversational_history"][1]["query"] == "Second question"
