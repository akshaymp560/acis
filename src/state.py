from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    # The primary research topic or directive submitted by the user
    research_topic: str
    
    # Raw strings and URLs scraped by the Researcher Agent
    scraped_raw_data: List[str]
    
    # Highly specific financial metrics structured by the Analyst
    structured_analytics: List[Dict[str, Any]]
    
    # The current running iteration version of the report document
    current_report_draft: str
    
    # Precise, bulleted diagnostic feedback messages passed from the Critic
    critic_feedback: List[str]
    
    # Essential for Rule 4: Loop Containment (Safety mechanism)
    loop_count: int