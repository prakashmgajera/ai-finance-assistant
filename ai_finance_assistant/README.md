# AI Finance Assistant

## Overview
A multi-agent AI system to democratize financial education and guidance for beginners. Features personalized learning, real-time market data, and scalable financial guidance.

## Architecture
- **Multi-Agent System:** LangChain, LangGraph, CrewAI
- **LLMs:** OpenAI GPT, Google Gemini, Claude Sonnet
- **Vector DB:** ChromaDB, FAISS, Pinecone
- **Market Data:** Alpha Vantage, yFinance
- **Web UI:** Streamlit, Gradio, React

### Agents
1. Finance Q&A
2. Portfolio Analysis
3. Market Analysis
4. Goal Planning
5. News Synthesizer
6. Tax Education

## Directory Structure
```
ai_finance_assistant/
├── src/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── finance_qa.py
│   │   ├── portfolio.py
│   │   ├── market.py
│   │   ├── goal.py
│   │   ├── news.py
│   │   └── tax.py
│   ├── core/
│   │   ├── agent_manager.py
│   │   ├── workflow_router.py
│   │   └── state.py
│   ├── data/
│   │   ├── articles/
│   │   ├── glossary.yaml
│   │   └── sample_portfolios/
│   ├── rag/
│   │   ├── vector_db.py
│   │   ├── retrieval.py
│   │   ├── chunking.py
│   │   └── attribution.py
│   ├── web_app/
│   │   ├── app.py
│   │   ├── tabs/
│   │   └── session.py
│   ├── utils/
│   │   ├── cache.py
│   │   ├── error.py
│   │   └── logger.py
│   ├── workflow/
│   │   ├── graph.py
│   │   └── memory.py
├── tests/
│   ├── agents/
│   ├── core/
│   ├── rag/
│   ├── web_app/
│   ├── data/
│   └── workflow/
├── config.yaml
├── requirements.txt
├── README.md
├── docs/
│   ├── architecture.png
│   ├── agent_protocols.md
│   ├── rag_details.md
│   └── performance.md
├── deployment/
│   ├── Dockerfile
│   ├── sample_data/
│   └── benchmarks/
```

## Milestone Plan
1. Initial Research & Architecture Design
2. Knowledge Base Development
3. Core Agent Implementation
4. Advanced Agent Development
5. Workflow Orchestration
6. RAG System Implementation
7. User Interface Development
8. Real-time Data Integration
9. Testing & Quality Assurance
10. Documentation & Deployment
11. [Stretch] MCP Server Implementation

## Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure API keys in `config.yaml`.
3. Run the web app:
   ```bash
   streamlit run src/web_app/app.py
   ```

## Usage Examples
- Ask financial questions
- Analyze your portfolio
- Get real-time market data
- Plan financial goals

## Troubleshooting
- Check API keys and config
- Review logs in `logs/app.log`
- Ensure all dependencies are installed

## License
MIT
