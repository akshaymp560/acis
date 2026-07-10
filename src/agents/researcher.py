from src.state import AgentState
from src.tools import execute_web_search

def researcher_node(state: AgentState) -> dict:
    """Agent 1: Executes web search and updates scraped data."""
    print("--- RESEARCHER AGENT ACTIVE ---")
    
    # 1. Read the objective from the shared state
    query = state["research_topic"]
    
    # 2. Trigger the external tool
    raw_data = execute_web_search(query)
    
    # 3. Return the exact state updates
    return {
        "scraped_raw_data": raw_data,
        "loop_count": state.get("loop_count", 0) + 1
    }