from typing import TypedDict, Annotated, List, Dict, Any
import operator

class AgentState(TypedDict):
    """
    State dictionary that flows through the Swarm Graph.
    """
    topic: str
    target_count: int
    raw_urls: Annotated[List[str], operator.add]
    scraped_content: Annotated[List[Dict[str, Any]], operator.add]
    final_reports: Annotated[List[Dict[str, Any]], operator.add]
    errors: Annotated[List[str], operator.add]
