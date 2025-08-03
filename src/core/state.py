from typing import TypedDict, List, Optional, Dict, Any

class FinanceAgentState(TypedDict, total=False):
    user_query: str
    next_agent: Optional[str]
    agent_response: Optional[str]
    conversational_history: List[Dict[str, Any]]
    portfolio_data: Optional[Dict[str, Any]]
    market_data: Optional[Dict[str, Any]]
    goal_plan_data: Optional[Dict[str, Any]]
