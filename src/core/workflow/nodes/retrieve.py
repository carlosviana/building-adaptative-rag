from typing import Any, Dict
from src.core.workflow.state import GraphState
from src.data.ingestion import retriever


def retrieve(state: GraphState) -> Dict[str, Any]:
    """Retrieve documents from vector store."""
    print("---RETRIEVE---")
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}