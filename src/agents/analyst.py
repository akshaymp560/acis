from langchain_core.prompts import ChatPromptTemplate
from src.state import AgentState
from src.agents.base import get_llm, AnalystSchema

def analyst_node(state: AgentState) -> dict:
    """Agent 2: Extracts structured financial metrics from raw data."""
    print("--- DATA ANALYST AGENT ACTIVE ---")
    
    # Force the LLM to output the specific Analyst JSON schema
    llm = get_llm().with_structured_output(AnalystSchema)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract key corporate and financial metrics from the provided text. Return ONLY structured data."),
        ("user", "Raw Data: {data}")
    ])
    
    chain = prompt | llm
    
    # Execute inference
    result = chain.invoke({"data": str(state["scraped_raw_data"])})
    
    return {"structured_analytics": result.metrics}