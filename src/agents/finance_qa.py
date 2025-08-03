from .base_agent import BaseAgent

class FinanceQnAAgent(BaseAgent):
    """
    Handles general financial education queries using RAG.
    """
    def __init__(self):
        super().__init__(name="Finance Q&A Agent")

    def process(self, query: str, context: dict = None) -> dict:
        # Integrate RAG pipeline here
        return {"response": "Finance Q&A response (stub)"}
