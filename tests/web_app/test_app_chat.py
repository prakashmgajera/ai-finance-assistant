import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import pytest
import streamlit
from agents.vectorize_rag_retriever import FinanceQAAgent, VectorizeRAGRetriever
from agents.llm_backend import LLMBackend

# Basic integration test for the chat logic
class DummySessionState(dict):
    pass

def test_streamlit_chat_flow():
    # Setup dummy session state
    session = DummySessionState()
    session["conversational_history"] = []
    llm = LLMBackend(provider="gemini", api_key="test")
    rag = VectorizeRAGRetriever(token="dummy")
    agent = FinanceQAAgent(llm, rag)
    user_query = "What is a bond?"
    state = {
        "user_query": user_query,
        "conversational_history": session["conversational_history"]
    }
    result_state = agent.process_query(state)
    response = result_state["agent_response"]
    # The agent appends a dict with keys: agent, query, response, sources
    entry = result_state["conversational_history"][0]
    assert entry["query"] == user_query
    assert "Sources:" in response
    assert entry["agent"] == "FinanceQA"
    assert entry["response"] == response
