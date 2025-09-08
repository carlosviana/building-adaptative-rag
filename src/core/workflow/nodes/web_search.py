from typing import Any, Dict
from dotenv import load_dotenv
from langchain.schema import Document
import os
from tavily import TavilyClient
from src.core.workflow.state import GraphState

load_dotenv()

# Use tavily-python directly instead of langchain-tavily
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(state: GraphState) -> Dict[str, Any]:
    print("---WEB SEARCH---")
    question = state["question"]
    
    # Initialize documents - this was the missing part!
    documents = state.get("documents", [])  # Get existing documents or empty list
    
    # Use tavily-python directly
    tavily_results = tavily_client.search(query=question, max_results=3)
    joined_tavily_result = "\n".join(
        [result["content"] for result in tavily_results["results"]]
    )
    web_results = Document(page_content=joined_tavily_result)
    
    # Add web results to existing documents (or create new list if documents was empty)
    if documents:
        documents.append(web_results)
    else:
        documents = [web_results]
    
    return {"documents": documents, "question": question}