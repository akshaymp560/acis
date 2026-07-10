from langgraph.graph import StateGraph, END
from src.state import AgentState

# Because of the __init__.py router you built, this single import grabs all 4 agents cleanly
from src.agents import researcher_node, analyst_node, writer_node, critic_node

# ==========================================
# 1. CONDITIONAL ROUTING LOGIC
# ==========================================

def route_workflow(state: AgentState) -> str:
    """
    Evaluates the graph state to determine the next execution node.
    This is the engine of the self-correcting loop.
    """
    # Safety Check: Rule 4 Loop Containment
    if state.get("loop_count", 0) >= 3:
        print("--- WARNING: LOOP LIMIT REACHED. FORCING END ---")
        return END
        
    # Check for Critic Rejections
    # If the feedback list has items, the Critic found a hallucination
    if len(state.get("critic_feedback", [])) > 0:
        print("--- CRITIC REJECTED DRAFT: ROUTING BACK TO WRITER ---")
        return "writer_agent"
        
    print("--- CRITIC APPROVED DRAFT: ROUTING TO COMPLETION ---")
    return END

# ==========================================
# 2. GRAPH COMPILATION
# ==========================================

def build_graph():
    """Assembles the nodes and edges into an executable state machine."""
    
    # Initialize the graph utilizing our unified state database
    builder = StateGraph(AgentState)

    # Register the structural processing points (Nodes)
    builder.add_node("researcher_agent", researcher_node)
    builder.add_node("analyst_agent", analyst_node)
    builder.add_node("writer_agent", writer_node)
    builder.add_node("critic_agent", critic_node)

    # Define the standard, deterministic sequential flow
    builder.add_edge("researcher_agent", "analyst_agent")
    builder.add_edge("analyst_agent", "writer_agent")
    builder.add_edge("writer_agent", "critic_agent")

    # Define the dynamic, self-correcting conditional flow
    builder.add_conditional_edges("critic_agent", route_workflow)

    # Set the operational entrance threshold
    builder.set_entry_point("researcher_agent")

    # Compile into an executable application
    return builder.compile()

# Export the compiled engine so app.py can run it
acis_engine = build_graph()