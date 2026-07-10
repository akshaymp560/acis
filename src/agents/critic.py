from langchain_core.prompts import ChatPromptTemplate
from src.state import AgentState
from src.agents.base import get_llm, QualityEvaluationSchema

def critic_node(state: AgentState) -> dict:
    """Agent 4: Evaluates the draft against strict quality standards."""
    print("--- QUALITY CRITIC AGENT ACTIVE ---")
    
    # Force the LLM to output exactly 'APPROVED' or 'REJECTED'
    llm = get_llm().with_structured_output(QualityEvaluationSchema)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Evaluate the report draft against the original metrics. If a metric is wrong or missing, REJECT it with reasons. Otherwise, APPROVE."),
        ("user", "Original Metrics: {metrics}\nDraft Report: {draft}")
    ])
    
    chain = prompt | llm
    evaluation = chain.invoke({
        "metrics": state["structured_analytics"],
        "draft": state["current_report_draft"]
    })
    
    # Fetch current feedback ledger
    new_feedback = state.get("critic_feedback", [])
    
    # If hallucination detected, log the specific deficiency
    if evaluation.status == "REJECTED":
        new_feedback.extend(evaluation.deficiencies)
        
    return {
        "critic_feedback": new_feedback,
        "loop_count": state.get("loop_count", 0) + 1
    }