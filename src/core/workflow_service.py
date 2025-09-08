import time
from typing import Dict, Any

class WorkflowService:
    def __init__(self, workflow):
        self.workflow = workflow

    def run_workflow(self, question: str) -> Dict[str, Any]:
        start_time = time.time()
        
        inputs = {"question": question}
        final_state = self.workflow.invoke(inputs)
        
        end_time = time.time()
        
        # This is a simplified response, we will need to extract more details
        # from the final_state to populate the full ChatResponse
        return {
            "answer": final_state.get("generation"),
            "sources": [doc.metadata.get("source", "") for doc in final_state.get("documents", [])],
            "session_id": "some-session-id", # to be implemented
            "processing_time": end_time - start_time,
            "route_taken": "vectorstore" # to be implemented
        }
