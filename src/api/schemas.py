from pydantic import BaseModel

class ResearchRequest(BaseModel):
    """Enforces type-checking on incoming corporate target directives."""
    topic: str