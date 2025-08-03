class WorkflowRouter:
    """
    Handles workflow orchestration and agent routing (LangGraph integration).
    """
    def __init__(self, agent_manager):
        self.agent_manager = agent_manager

    def handle_query(self, query: str, context: dict = None) -> dict:
        """
        Entry point for user queries. Manages routing and state.
        """
        return self.agent_manager.route_query(query, context)
