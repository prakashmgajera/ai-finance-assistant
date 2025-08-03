from typing import Any, Dict
from src.core.state import FinanceAgentState

class RouterAgent:
    def __init__(self, agent_map: Dict[str, Any], vector_db):
        self.agent_map = agent_map
        self.vector_db = vector_db

    def route(self, state: FinanceAgentState) -> str:
        """
        Uses vector similarity to select the appropriate agent for the user query.
        """
        query = state["user_query"]
        # Vector matching logic (placeholder)
        matched_agent = self.vector_db.match_agent(query)
        state["next_agent"] = matched_agent
        return matched_agent
