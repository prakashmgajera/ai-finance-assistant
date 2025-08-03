from agents.base_agent import BaseAgent

class AgentManager:
    """
    Orchestrates agent selection and execution.
    """
    def __init__(self, agents: dict):
        self.agents = agents

    def route_query(self, query: str, context: dict = None) -> dict:
        """
        Routes query to appropriate agent(s) based on classification.
        """
        # Placeholder: implement query classification and routing logic
        # For now, route all queries to Finance Q&A Agent
        agent = self.agents.get('finance_qa')
        if agent:
            return agent.process(query, context)
        return {"error": "No suitable agent found."}
