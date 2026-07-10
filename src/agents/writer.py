from langchain_core.prompts import ChatPromptTemplate
from src.state import AgentState
from src.agents.base import get_llm

def writer_node(state: AgentState) -> dict:
    """Agent 3: Drafts the report based on structured analytics."""
    print("--- WRITER AGENT ACTIVE ---")
    
    # Standard LLM (no structured output needed for writing paragraphs)
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert equity research writer. Write a professional markdown report using ONLY the provided metrics. Do not hallucinate."),
        ("user", "Topic: {topic}\nMetrics: {metrics}\nCritic Feedback to fix: {feedback}")
    ])
    
    chain = prompt | llm
    
    # If the Critic rejected a previous draft, the Writer reads the feedback here
    feedback = state.get("critic_feedback", [])
    
    result = chain.invoke({
        "topic": state["research_topic"],
        "metrics": state["structured_analytics"],
        "feedback": feedback
    })
    
    return {"current_report_draft": result.content}