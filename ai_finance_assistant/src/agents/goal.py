from .base_agent import BaseAgent

class GoalPlanningAgent(BaseAgent):
    """
    Assists with financial goal setting and planning.
    """
    def __init__(self):
        super().__init__(name="Goal Planning Agent")

    def process(self, query: str, context: dict = None) -> dict:
        # Goal planning logic here
        return {"response": "Goal planning response (stub)"}
