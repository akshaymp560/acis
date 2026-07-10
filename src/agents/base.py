from pydantic import BaseModel, Field
from typing import List
from langchain_groq import ChatGroq

# ==========================================
# 1. PYDANTIC SCHEMAS (The Guardrails)
# ==========================================

class Metric(BaseModel):
    """Sub-schema enforcing strict key-value pairs for extracted data."""
    metric_name: str = Field(description="The name of the metric or event (e.g., 'Acquisition Price', 'CEO Name')")
    metric_value: str = Field(description="The value or detail (e.g., '$550M', 'Tim Cook')")

class AnalystSchema(BaseModel):
    """The master form the Analyst must fill using the rigid Metric sub-schema."""
    metrics: List[Metric] = Field(description="List of extracted financial, corporate, and market metrics.")

class QualityEvaluationSchema(BaseModel):
    """The form the Critic must use to approve or reject reports."""
    status: str = Field(description="Must be exactly 'APPROVED' or 'REJECTED'")
    deficiencies: List[str] = Field(description="List of specific gaps, missing metrics, or inaccuracies found.")

# ==========================================
# 2. INFERENCE ENGINE 
# ==========================================

def get_llm():
    """Initializes the high-speed Llama 3 engine via Groq."""
    return ChatGroq(
        model_name="llama-3.3-70b-versatile", 
        temperature=0.1
    )
