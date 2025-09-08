from typing import List, TypedDict

class GraphState(TypedDict):
    """State object for workflow containing query, documents and control flags."""
    question: str   # user ticket question (description)
    generation: str   # LLM-generated response
    web_search: bool   # Control flag for web search
    documents: List[str]   # Retrieved documents context