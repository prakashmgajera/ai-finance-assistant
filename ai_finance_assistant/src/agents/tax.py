from .base_agent import BaseAgent

class TaxEducationAgent(BaseAgent):
    """
    Explains tax concepts and account types.
    """
    def __init__(self):
        super().__init__(name="Tax Education Agent")

    def process(self, query: str, context: dict = None) -> dict:
        # Tax education logic here
        return {"response": "Tax education response (stub)"}
