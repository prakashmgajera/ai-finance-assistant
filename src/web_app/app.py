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


# LLM config (OpenAI is default, selection removed from UI)

st.sidebar.subheader("LLM Configuration")
llm_type = "openai"
try:
    llm_api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    llm_api_key = os.getenv("OPENAI_API_KEY")




# Qdrant Cloud config


st.sidebar.subheader("Qdrant Cloud Configuration")
try:
    qdrant_api_key = st.secrets["QDRANT_API_KEY"]
except Exception:
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
st.session_state["qdrant_api_key"] = qdrant_api_key

# Store LLM config in session state

st.session_state["llm_type"] = llm_type
st.session_state["llm_api_key"] = llm_api_key

# For production, mask API key and warn if missing
if not llm_api_key:
    st.sidebar.warning("LLM API key required. Please set it in your system environment variables.")
if not qdrant_api_key:
    st.sidebar.warning("Qdrant API key required. Please set it in your system environment variables.")




from agents.llamaindex_rag_retriever import LlamaIndexRAGRetriever
from agents.llm_backend import LLMBackend

# Setup FinanceQAAgent with user-provided model and key
llm_backend = LLMBackend(provider=llm_type, api_key=llm_api_key)
qdrant_url = "https://6f1a0c83-2778-4e95-af4e-6b6506891a53.us-west-2-0.aws.cloud.qdrant.io"
rag_retriever = None
finance_qa_agent = None
if qdrant_api_key:
    rag_retriever = LlamaIndexRAGRetriever(qdrant_url=qdrant_url, qdrant_api_key=qdrant_api_key)
    from agents.vectorize_rag_retriever import FinanceQAAgent
    finance_qa_agent = FinanceQAAgent(llm_backend, rag_retriever)
else:
    st.sidebar.error("Please enter your Qdrant API key to enable retrieval.")

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
