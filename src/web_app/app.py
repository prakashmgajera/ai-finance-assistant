import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st

st.set_page_config(page_title="AI Finance Assistant", layout="wide")

# Initialize session state for conversation memory and data
if "conversational_history" not in st.session_state:
    st.session_state["conversational_history"] = []
if "portfolio_data" not in st.session_state:
    st.session_state["portfolio_data"] = None
if "market_data" not in st.session_state:
    st.session_state["market_data"] = None
if "goal_plan_data" not in st.session_state:
    st.session_state["goal_plan_data"] = None


# Sidebar for navigation and LLM config
st.sidebar.title("Navigation")
tab = st.sidebar.radio("Go to", ["Chat", "Portfolio", "Market", "Goals"])

st.sidebar.markdown("---")

# LLM config
st.sidebar.subheader("LLM Configuration")
llm_type = st.sidebar.selectbox("Type of LLM", ["gemini", "openai"], index=0)
llm_api_key = st.sidebar.text_input("LLM API Key", type="password")

# Vectorize config
st.sidebar.subheader("Vectorize RAG Configuration")
vectorize_token = st.sidebar.text_input("Vectorize API Token", type="password")
if not vectorize_token:
    st.sidebar.warning("Vectorize API token required for RAG retrieval. Please enter your token.")
st.session_state["vectorize_token"] = vectorize_token

# Store LLM config in session state
st.session_state["llm_type"] = llm_type
st.session_state["llm_api_key"] = llm_api_key

# For production, mask API key and warn if missing
if not llm_api_key:
    st.sidebar.warning("API key required for LLM access. Please enter your key.")


from agents.vectorize_rag_retriever import FinanceQAAgent, VectorizeRAGRetriever
from agents.llm_backend import LLMBackend

# Setup FinanceQAAgent with user-provided model and key
llm_backend = LLMBackend(provider=llm_type, api_key=llm_api_key)
rag_retriever = VectorizeRAGRetriever(token=st.session_state.get("vectorize_token", ""))
finance_qa_agent = FinanceQAAgent(llm_backend, rag_retriever)

# Main UI Tabs
if tab == "Chat":
    st.title("💬 Finance Q&A Chat")
    user_query = st.text_input("Ask a finance or investment question:")
    if st.button("Send") and user_query:
        # Prepare state and get real response from FinanceQAAgent
        state = {
            "user_query": user_query,
            "conversational_history": st.session_state["conversational_history"]
        }
        result_state = finance_qa_agent.process_query(state)
        response = result_state["agent_response"]
        st.session_state["conversational_history"].append({"user": user_query, "agent": response})
    for entry in st.session_state["conversational_history"]:
        # Support both app and agent history formats
        if "user" in entry and "agent" in entry:
            st.markdown(f"**You:** {entry['user']}")
            st.markdown(f"**Assistant:** {entry['agent']}")
        elif "query" in entry and "response" in entry:
            st.markdown(f"**You:** {entry['query']}")
            # Show error if response contains error
            if entry["response"].startswith("Error:"):
                st.error(entry["response"])
            else:
                st.markdown(f"**Assistant:** {entry['response']}")
            # Optionally show sources if present
            if "sources" in entry and entry["sources"]:
                st.markdown("**Sources:**")
                for src in entry["sources"]:
                    st.markdown(f"- [{src}]({src})")

elif tab == "Portfolio":
    st.title("📊 Portfolio Analyzer")
    st.write("Upload your portfolio or view analysis here.")
    # Placeholder for portfolio data and visualizations
    st.info("Portfolio analysis features coming soon.")

elif tab == "Market":
    st.title("📈 Market Analyzer")
    st.write("Analyze stocks, ETFs, commodities, and more.")
    # Placeholder for market data and visualizations
    st.info("Market analysis features coming soon.")

elif tab == "Goals":
    st.title("🎯 Goal Projection")
    st.write("Set and track your financial goals.")
    # Placeholder for goal planning and projections
    st.info("Goal projection features coming soon.")

st.markdown("---")
st.caption("AI Finance Assistant • For educational purposes only. Sources are cited in agent responses.")
